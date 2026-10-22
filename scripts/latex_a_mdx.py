"""Convierte los capítulos LaTeX del libro a MDX para la web.

La prosa tiene una sola fuente: libro/capitulos/*.tex. Este script traduce los
comandos semánticos del libro (libro/estilo/armaduras.sty) a los componentes
equivalentes de la web y escribe web/contenido/capNN_nombre.mdx. Las
soluciones de los ejercicios se toman del anexo de soluciones y se colocan,
plegadas, debajo de cada ejercicio.

- \\soloweb{...}: contenido que solo aparece en la web (por ejemplo, una
  animación); se copia tal cual al MDX.
- \\sololibro{...}: contenido que solo aparece en el libro impreso.

La numeración de figuras, ecuaciones y capítulos se lee de los archivos .aux
de la última compilación del libro: compilar antes con latexmk.

Cualquier comando que el script no conozca produce un error, para que nada se
pierda en silencio.

Uso: uv run python scripts/latex_a_mdx.py [capNN_nombre ...]
"""

import hashlib
import re
import shutil
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comun import RAIZ

LIBRO = RAIZ / "libro"
CAPITULOS = LIBRO / "capitulos"
ANEXOS = LIBRO / "anexos"
SOLUCIONES = ANEXOS / "anexoF_soluciones.tex"
# Las soluciones (anexo F) no tienen página propia en la web: se pliegan debajo
# de cada ejercicio.
ANEXOS_WEB = [a for a in ANEXOS.glob("anexo*.tex") if a != SOLUCIONES]
COMPILACION = LIBRO / "build"
DESTINO = RAIZ / "web" / "contenido"
NOTEBOOKS = RAIZ / "notebooks"
CAPTURAS = RAIZ / "capturas"

NBSP = "\u00a0"
ESPACIO_FINO = "\u202f"


class ErrorDeConversion(Exception):
    pass


# ---------------------------------------------------------------------------
# Lectura de LaTeX
# ---------------------------------------------------------------------------


def quitar_comentarios(texto):
    # \py{...} es literal (minted): un % dentro de él no inicia un comentario.
    patron = r"\\py\{(?:[^{}\n]|\{[^{}\n]*\})*\}|(?<!\\)%.*"

    def reemplazar(coincidencia):
        texto_hallado = coincidencia.group(0)
        return texto_hallado if texto_hallado.startswith("\\py{") else ""

    return "\n".join(re.sub(patron, reemplazar, linea) for linea in texto.splitlines())


def leer_argumento(texto, pos):
    """Lee {...} desde pos (saltando espacios) y devuelve (contenido, fin)."""
    while pos < len(texto) and texto[pos] in " \n":
        pos += 1
    if pos >= len(texto) or texto[pos] != "{":
        raise ErrorDeConversion(f"se esperaba '{{' en: {texto[pos : pos + 40]!r}")
    nivel, inicio = 0, pos
    while pos < len(texto):
        caracter = texto[pos]
        if caracter == "\\":
            pos += 2
            continue
        if caracter == "{":
            nivel += 1
        elif caracter == "}":
            nivel -= 1
            if nivel == 0:
                return texto[inicio + 1 : pos], pos + 1
        pos += 1
    raise ErrorDeConversion(f"llave sin cerrar en: {texto[inicio : inicio + 40]!r}")


def leer_opcional(texto, pos):
    """Lee [...] si existe en pos y devuelve (contenido o None, fin)."""
    if pos < len(texto) and texto[pos] == "[":
        fin = texto.index("]", pos)
        return texto[pos + 1 : fin], fin + 1
    return None, pos


def buscar_fin_de_entorno(texto, nombre, pos):
    """Devuelve (inicio_de_\\end, fin) del entorno que empieza antes de pos."""
    patron = re.compile(r"\\(begin|end)\{" + re.escape(nombre) + r"\}")
    nivel = 1
    for coincidencia in patron.finditer(texto, pos):
        nivel += 1 if coincidencia.group(1) == "begin" else -1
        if nivel == 0:
            return coincidencia.start(), coincidencia.end()
    raise ErrorDeConversion(f"falta \\end{{{nombre}}}")


def dividir_items(texto):
    """Divide el contenido de una lista en sus \\item de primer nivel."""
    items, nivel, actual = [], 0, None
    for token in re.split(r"(\\item\b|\\begin\{[^}]+\}|\\end\{[^}]+\})", texto):
        if token == "\\item" and nivel == 0:
            if actual is not None:
                items.append(actual)
            actual = ""
            continue
        if token.startswith("\\begin{"):
            nivel += 1
        elif token.startswith("\\end{"):
            nivel -= 1
        if actual is not None:
            actual += token
    if actual is not None:
        items.append(actual)
    return items


# ---------------------------------------------------------------------------
# Números y unidades (siunitx)
# ---------------------------------------------------------------------------

PREFIJOS = {"kilo": "k", "giga": "G", "mega": "M", "centi": "c", "milli": "m"}
UNIDADES = {"metre": "m", "newton": "N", "pascal": "Pa", "percent": "%"}
SUPERINDICES = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def unidad(texto, en_matematica):
    """Traduce una unidad de siunitx, por ejemplo \\kilo\\newton\\per\\metre."""
    partes, prefijo = [], ""
    for nombre in re.findall(r"\\([A-Za-z]+)", texto):
        if nombre in PREFIJOS:
            prefijo = PREFIJOS[nombre]
        elif nombre in UNIDADES:
            partes.append(prefijo + UNIDADES[nombre])
            prefijo = ""
        elif nombre in ("squared", "cubed"):
            potencia = "2" if nombre == "squared" else "3"
            partes[-1] += (
                f"^{potencia}" if en_matematica else potencia.translate(SUPERINDICES)
            )
        elif nombre == "per":
            partes.append("/")
        else:
            raise ErrorDeConversion(f"unidad desconocida: \\{nombre}")
    resultado = "".join(partes)
    if en_matematica:
        return r"\mathrm{" + resultado + "}"
    return resultado


def numero(texto, en_matematica):
    texto = texto.strip()
    if "e" in texto:
        mantisa, exponente = texto.split("e")
        if en_matematica:
            return rf"{mantisa}\times10^{{{int(exponente)}}}"
        return f"{mantisa}{NBSP}×{NBSP}10" + str(int(exponente)).translate(SUPERINDICES)
    entero = texto.lstrip("-")
    if entero.isdigit() and len(entero) >= 5:
        separador = r"\," if en_matematica else ESPACIO_FINO
        grupos = []
        while entero:
            grupos.insert(0, entero[-3:])
            entero = entero[:-3]
        texto = ("-" if texto.startswith("-") else "") + separador.join(grupos)
    if texto.startswith("-") and not en_matematica:
        texto = "−" + texto[1:]
    return texto


# ---------------------------------------------------------------------------
# Conversión
# ---------------------------------------------------------------------------

NOMBRES_DE_REFERENCIA = {
    "fig": "figura",
    "tab": "tabla",
    "eq": "ecuación",
    "cap": "capítulo",
    "sec": "apartado",
    "ej": "ejercicio",
}

CAJAS = {
    "recuerda": "Recuerda",
    "python": "Python",
    "cuidado": "Cuidado",
    "parasabermas": "ParaSaberMas",
    "estrategia": "Estrategia",
}

SIMBOLOS = {"dots": "…", "ldots": "…", "textendash": "–", "textemdash": "—"}

COMANDOS_IGNORADOS = {
    "label",
    "centering",
    "par",
    "medskip",
    "smallskip",
    "bigskip",
    "noindent",
    "pendiente",
    "sololibro",
    "FloatBarrier",
    "index",
}


class Convertidor:
    def __init__(self, capitulo, etiquetas, soluciones, ids_de_capitulos, valores=None):
        self.capitulo = capitulo
        self.etiquetas = etiquetas
        self.soluciones = soluciones
        self.ids_de_capitulos = ids_de_capitulos
        self.valores = valores or {}
        self.seccion = 0
        self.problema = 0

    # --- bloques -----------------------------------------------------------

    def bloques(self, texto):
        """Convierte texto que puede contener entornos."""
        salida, pos = [], 0
        for coincidencia in re.finditer(r"\\begin\{([^}]+)\}", texto):
            if coincidencia.start() < pos:
                continue
            salida.append(self.en_linea(texto[pos : coincidencia.start()]))
            nombre = coincidencia.group(1)
            inicio_fin, fin = buscar_fin_de_entorno(texto, nombre, coincidencia.end())
            contenido = texto[coincidencia.end() : inicio_fin]
            salida.append(self.entorno(nombre, contenido))
            pos = fin
        salida.append(self.en_linea(texto[pos:]))
        return "".join(salida)

    def bloque(self, texto):
        return f"\n\n{texto.strip()}\n\n"

    def entorno(self, nombre, contenido):
        if nombre in CAJAS:
            return self.bloque(
                f"<{CAJAS[nombre]}>\n\n{self.bloques(contenido).strip()}\n\n</{CAJAS[nombre]}>"
            )
        if nombre == "objetivos":
            lista = self.lista(contenido, "-")
            return self.bloque(f"<Objetivos>\n\n{lista}\n\n</Objetivos>")
        if nombre in ("itemize", "enumerate"):
            return self.bloque(
                self.lista(contenido, "-" if nombre == "itemize" else "1.")
            )
        if nombre == "description":
            return self.bloque(self.descripcion(contenido))
        if nombre == "problemaresuelto":
            titulo, resto = leer_opcional(contenido, 0)
            self.problema += 1
            atributo = f' titulo="{self.en_linea(titulo).strip()}"' if titulo else ""
            cuerpo = self.bloques(contenido[resto:]).strip()
            return self.bloque(
                f'<ProblemaResuelto numero="{self.capitulo}.{self.problema}"{atributo}>'
                f"\n\n{cuerpo}\n\n</ProblemaResuelto>"
            )
        if nombre == "ecuacionclave":
            return self.bloque(
                "<EcuacionClave>\n\n$$\n\\begin{aligned}\n"
                + self.matematica(contenido).strip()
                + "\n\\end{aligned}\n$$\n\n</EcuacionClave>"
            )
        if nombre == "align":
            # Cada línea numerada se convierte en una ecuación con su número
            ecuaciones = []
            for linea in re.split(r"\\\\", contenido):
                if not linea.strip():
                    continue
                etiqueta = re.search(r"\\label\{([^}]+)\}", linea)
                formula = re.sub(r"\\label\{[^}]+\}", "", linea).replace("&", "")
                formula = self.matematica(formula).strip()
                if etiqueta:
                    formula += rf" \tag{{{self.numero_de(etiqueta.group(1))}}}"
                ecuaciones.append(f"$$\n{formula}\n$$")
            return self.bloque("\n\n".join(ecuaciones))
        if nombre == "equation":
            etiqueta = re.search(r"\\label\{([^}]+)\}", contenido)
            formula = self.matematica(
                re.sub(r"\\label\{[^}]+\}", "", contenido)
            ).strip()
            if etiqueta:
                formula += rf" \tag{{{self.numero_de(etiqueta.group(1))}}}"
            return self.bloque(f"$$\n{formula}\n$$")
        if nombre == "figure":
            return self.figura(contenido)
        if nombre == "table":
            return self.tabla(contenido)
        if nombre == "center":
            return self.bloques(contenido)
        if nombre in ("codigo", "consola"):
            # Texto literal: se copia tal cual en un bloque de código.
            lenguaje = "python" if nombre == "codigo" else "text"
            literal = textwrap.dedent(contenido.strip("\n")).rstrip()
            return self.bloque(f"```{lenguaje}\n{literal}\n```")
        if nombre == "ejercicio":
            clave, resto = leer_argumento(contenido, 0)
            if clave not in self.soluciones:
                raise ErrorDeConversion(f"el ejercicio {clave} no tiene solución")
            enunciado = self.bloques(contenido[resto:]).strip()
            solucion = self.bloques(self.soluciones[clave]).strip()
            return self.bloque(
                f'<Ejercicio numero="{clave}">\n\n{enunciado}\n\n'
                f"<SolucionDelEjercicio>\n\n{solucion}\n\n</SolucionDelEjercicio>"
                "\n\n</Ejercicio>"
            )
        raise ErrorDeConversion(f"entorno desconocido: {nombre}")

    def lista(self, contenido, marca):
        items = []
        for numero_item, item in enumerate(dividir_items(contenido), 1):
            texto = self.bloques(item).strip()
            if "\n\n" not in texto:
                texto = re.sub(r"\s*\n\s*", " ", texto)
            vineta = f"{numero_item}." if marca == "1." else marca
            items.append(f"{vineta} {texto}")
        return "\n".join(items)

    def descripcion(self, contenido):
        items = []
        for item in dividir_items(contenido):
            termino, resto = leer_opcional(item.lstrip(), 0)
            texto = re.sub(
                r"\s*\n\s*", " ", self.bloques(item.lstrip()[resto:]).strip()
            )
            items.append(f"- **{self.en_linea(termino).strip()}** {texto}")
        return "\n".join(items)

    def figura(self, contenido):
        etiqueta = re.search(r"\\label\{([^}]+)\}", contenido).group(1)
        inicio = contenido.index("\\caption")
        leyenda, _ = leer_argumento(contenido, inicio + len("\\caption"))
        texto = re.sub(r"\s*\n\s*", " ", self.en_linea(leyenda).strip())
        if "\\captura" in contenido:
            # Captura de pantalla: la imagen, o un recuadro mientras falte
            archivo, pos = leer_argumento(contenido, contenido.index("\\captura") + 8)
            descripcion, _ = leer_argumento(contenido, pos)
            descripcion = re.sub(r"\s+", " ", self.en_linea(descripcion)).strip()
            descripcion = descripcion.replace('"', "'")
            return self.bloque(
                f'<Captura archivo="{archivo}" numero="{self.numero_de(etiqueta)}"'
                f' descripcion="{descripcion}">\n{texto}\n</Captura>'
            )
        if grafico := re.search(r"\\grafico\{([^}]+)\}", contenido):
            # Gráfico generado por el código, con su número y su leyenda
            return self.bloque(
                f'<Grafico nombre="{grafico.group(1)}" '
                f'numero="{self.numero_de(etiqueta)}">\n{texto}\n</Grafico>'
            )
        nombre = re.search(r"\\figura\{([^}]+)\}", contenido).group(1)
        return self.bloque(
            f'<Figura nombre="{nombre}" numero="{self.numero_de(etiqueta)}">\n'
            f"{texto}\n</Figura>"
        )

    def tabla(self, contenido):
        etiqueta = re.search(r"\\label\{([^}]+)\}", contenido).group(1)
        inicio = contenido.index("\\caption")
        leyenda, _ = leer_argumento(contenido, inicio + len("\\caption"))
        partes = [
            f"**Tabla {self.numero_de(etiqueta)}:** "
            + re.sub(r"\s*\n\s*", " ", self.en_linea(leyenda).strip())
        ]
        for coincidencia in re.finditer(r"\\begin\{tabular\}", contenido):
            columnas, pos = leer_argumento(contenido, coincidencia.end())
            fin, _ = buscar_fin_de_entorno(contenido, "tabular", pos)
            partes.append(self.tabular(columnas, contenido[pos:fin]))
        return self.bloque("\n\n".join(partes))

    def tabular(self, columnas, contenido):
        alineaciones = {"c": ":---:", "l": ":---", "r": "---:", "S": "---:"}
        formato = [alineaciones[c] for c in re.sub(r"@\{\}|\[[^]]*\]", "", columnas)]
        contenido = re.sub(r"\\(toprule|midrule|bottomrule)", "", contenido)
        filas = []
        for fila in re.split(r"\\\\", contenido):
            if not fila.strip():
                continue
            celdas = re.split(r"(?<!\\)&", fila)
            filas.append(
                "| "
                + " | ".join(
                    re.sub(r"\s+", " ", self.en_linea(c).strip()).strip("{}")
                    for c in celdas
                )
                + " |"
            )
        filas.insert(1, "| " + " | ".join(formato) + " |")
        return "\n".join(filas)

    # --- texto en línea ----------------------------------------------------

    def en_linea(self, texto):
        """Convierte texto sin entornos: comandos, matemática y símbolos."""
        piezas = re.split(
            r"(\$\$.*?\$\$|\$[^$]*\$|\\\[.*?\\\])", texto, flags=re.DOTALL
        )
        salida = []
        for indice, pieza in enumerate(piezas):
            if indice % 2:
                if pieza.startswith("\\["):
                    salida.append(
                        "\n\n$$\n" + self.matematica(pieza[2:-2]).strip() + "\n$$\n\n"
                    )
                else:
                    # En una sola línea: un salto seguido de "- " o "1. "
                    # se leería en Markdown como el inicio de una lista.
                    pieza = re.sub(r"\s*\n\s*", " ", pieza)
                    salida.append(self.matematica(pieza))
            else:
                salida.append(self.texto(pieza))
        return "".join(salida)

    def matematica(self, texto):
        """La matemática pasa a KaTeX; solo se traducen los comandos de siunitx."""

        def reemplazar(patron, funcion, texto):
            resultado, pos = [], 0
            for coincidencia in re.finditer(patron, texto):
                if coincidencia.start() < pos:
                    continue
                resultado.append(texto[pos : coincidencia.start()])
                reemplazo, pos = funcion(texto, coincidencia.end())
                resultado.append(reemplazo)
            resultado.append(texto[pos:])
            return "".join(resultado)

        def si_completo(texto, pos):
            valor, pos = leer_argumento(texto, pos)
            unidades, pos = leer_argumento(texto, pos)
            return numero(valor, True) + r"\," + unidad(unidades, True), pos

        def si_unidad(texto, pos):
            unidades, pos = leer_argumento(texto, pos)
            return unidad(unidades, True), pos

        def angulo(texto, pos):
            valor, pos = leer_argumento(texto, pos)
            return numero(valor, True) + r"^\circ", pos

        texto = reemplazar(r"\\SI(?![A-Za-z])", si_completo, texto)
        texto = reemplazar(r"\\si(?![A-Za-z])", si_unidad, texto)

        def valor(texto, pos):
            nombre, pos = leer_argumento(texto, pos)
            return numero(self.valor_de(nombre), True), pos

        texto = reemplazar(r"\\valor(?![A-Za-z])", valor, texto)
        return reemplazar(r"\\ang(?![A-Za-z])", angulo, texto)

    def valor_de(self, nombre):
        if nombre not in self.valores:
            raise ErrorDeConversion(
                f"valor desconocido: {nombre} (¿se ejecutó generar_salidas.py?)"
            )
        return self.valores[nombre]

    def texto(self, texto):
        salida, pos = [], 0
        for coincidencia in re.finditer(r"\\([A-Za-z]+)(\*?)|\\([,%&$#_{} ])|~", texto):
            if coincidencia.start() < pos:
                continue
            salida.append(self.simbolos(texto[pos : coincidencia.start()]))
            pos = coincidencia.end()
            if coincidencia.group(0) == "~":
                salida.append(NBSP)
                continue
            if coincidencia.group(3):
                simbolo = coincidencia.group(3)
                salida.append(ESPACIO_FINO if simbolo == "," else simbolo)
                continue
            reemplazo, pos = self.comando(
                coincidencia.group(1), bool(coincidencia.group(2)), texto, pos
            )
            salida.append(reemplazo)
        salida.append(self.simbolos(texto[pos:]))
        return "".join(salida)

    def simbolos(self, texto):
        if "{" in texto or "}" in texto:
            raise ErrorDeConversion(f"llave suelta en el texto: {texto.strip()[:60]!r}")
        return texto.replace("---", "—").replace("--", "–")

    def comando(self, nombre, con_asterisco, texto, pos):
        """Traduce un comando; devuelve (texto convertido, nueva posición)."""

        def argumento():
            nonlocal pos
            valor, pos = leer_argumento(texto, pos)
            return valor

        if nombre in COMANDOS_IGNORADOS:
            if nombre in ("label", "pendiente", "sololibro", "index"):
                argumento()
            return "", pos
        if nombre == "soloweb":
            return self.bloque(argumento()), pos
        if nombre == "section":
            titulo = self.en_linea(argumento()).strip()
            if con_asterisco:
                return self.bloque(f"## {titulo}"), pos
            self.seccion += 1
            return self.bloque(f"## {self.capitulo}.{self.seccion} {titulo}"), pos
        if nombre == "subsection":
            return self.bloque(f"### {self.en_linea(argumento()).strip()}"), pos
        if nombre in ("fragmento", "salida", "grafico"):
            componente = {
                "fragmento": "Fragmento",
                "salida": "Salida",
                "grafico": "Grafico",
            }
            return self.bloque(f'<{componente[nombre]} nombre="{argumento()}" />'), pos
        if nombre == "solucion":
            return self.bloque("<Solucion />"), pos
        if nombre == "repasoyresumen":
            return self.bloque("## Repaso y resumen del capítulo"), pos
        if nombre == "ejercicios":
            return self.bloque("## Ejercicios"), pos
        if nombre == "puntodecontrol":
            return self.bloque(f'<PuntoDeControl capitulo="{argumento()}" />'), pos
        if nombre == "micalculadora":
            return self.bloque("<MiCalculadora />"), pos
        if nombre == "validacionopensees":
            return self.bloque("<ValidacionOpenSees />"), pos
        if nombre == "py" or nombre == "texttt":
            return f"`{argumento()}`", pos
        if nombre == "emph":
            return f"*{self.en_linea(argumento())}*", pos
        if nombre == "textbf" or nombre == "textsf":
            return f"**{self.en_linea(argumento())}**", pos
        if nombre == "termino":
            espanol = self.en_linea(argumento())
            ingles = re.sub(r"\s+", " ", self.en_linea(argumento()))
            return f"*{espanol}* (*{ingles}*)", pos
        if nombre == "concepto":
            return f"*{self.en_linea(argumento())}*", pos
        if nombre == "enquote":
            return f"«{self.en_linea(argumento())}»", pos
        if nombre == "url":
            direccion = argumento()
            visible = re.sub(r"^https?://", "", direccion)
            return f"[{visible}]({direccion})", pos
        if nombre == "nota":
            return f" <Nota>{self.en_linea(argumento()).strip()}</Nota>", pos
        if nombre == "SI":
            valor, unidades = argumento(), argumento()
            return numero(valor, False) + NBSP + unidad(unidades, False), pos
        if nombre == "si":
            return unidad(argumento(), False), pos
        if nombre == "ang":
            return numero(argumento(), False) + "°", pos
        if nombre == "ref":
            return self.numero_de(argumento()), pos
        if nombre == "cref":
            return self.referencia(argumento()), pos
        if nombre == "valor":
            return numero(self.valor_de(argumento()), False), pos
        if nombre == "valoropensees":
            return numero(self.valor_de(f"ops_{argumento()}"), False), pos
        if nombre == "eqref":
            return f"({self.numero_de(argumento())})", pos
        if nombre in SIMBOLOS:
            return SIMBOLOS[nombre], pos
        if nombre == "textcite":
            detalle, pos = leer_opcional(texto, pos)
            return cita_textual(argumento(), detalle), pos
        raise ErrorDeConversion(f"comando desconocido: \\{nombre}")

    def numero_de(self, etiqueta):
        if etiqueta not in self.etiquetas:
            raise ErrorDeConversion(
                f"etiqueta desconocida: {etiqueta} (¿se compiló el libro con latexmk?)"
            )
        return self.etiquetas[etiqueta]

    def referencia(self, etiqueta):
        tipo = etiqueta.split(":")[0]
        texto = f"{NOMBRES_DE_REFERENCIA[tipo]}{NBSP}{self.numero_de(etiqueta)}"
        if tipo == "eq":
            texto = f"ecuación{NBSP}({self.numero_de(etiqueta)})"
        if tipo == "cap" and etiqueta in self.ids_de_capitulos:
            return f"[{texto}](/capitulos/{self.ids_de_capitulos[etiqueta]})"
        return texto


# ---------------------------------------------------------------------------
# Archivos
# ---------------------------------------------------------------------------


def leer_etiquetas():
    etiquetas = {}
    archivos = list(COMPILACION.rglob("*.aux"))
    if not archivos:
        raise ErrorDeConversion("no hay archivos .aux: compilar el libro con latexmk")
    for archivo in archivos:
        texto = archivo.read_text(encoding="utf-8", errors="replace")
        for clave, valor in re.findall(r"\\newlabel\{([^}@]+)\}\{\{([^}]*)\}", texto):
            etiquetas[clave] = valor
    return etiquetas


def cita_textual(clave, detalle=None):
    """Cita autor-año como \\textcite de biblatex: «Kassimali (2012, cap. 3)»."""
    texto = (LIBRO / "bibliografia.bib").read_text(encoding="utf-8")
    entrada = re.search(r"@\w+\{" + re.escape(clave) + r",(.*?)\n\}", texto, re.DOTALL)
    if not entrada:
        raise ErrorDeConversion(f"referencia desconocida: {clave}")
    campos = dict(
        re.findall(r"(\w+)\s*=\s*\{(.*?)\},?\s*$", entrada.group(1), re.MULTILINE)
    )
    apellidos = [
        autor.split(",")[0].strip() for autor in campos["author"].split(" and ")
    ]
    if len(apellidos) == 1:
        autores = apellidos[0]
    elif len(apellidos) == 2:
        autores = f"{apellidos[0]} y {apellidos[1]}"
    else:
        autores = f"{apellidos[0]} et al."
    detalle = f", {detalle.replace('~', NBSP)}" if detalle else ""
    return f"{autores} ({campos['year']}{detalle})"


def leer_valores():
    """Valores calculados por el código ({nombre: número}), de recursos/."""
    archivo = RAIZ / "recursos" / "valores.tex"
    if not archivo.exists():
        return {}
    patron = r"\\csname valor@([a-z0-9_]+)\\endcsname\{([^}]*)\}"
    return dict(re.findall(patron, archivo.read_text(encoding="utf-8")))


def leer_soluciones():
    """Devuelve {clave: texto LaTeX} de cada \\soluciondel del anexo."""
    texto = quitar_comentarios(SOLUCIONES.read_text(encoding="utf-8"))
    soluciones = {}
    partes = re.split(r"\\soluciondel\{([^}]+)\}", texto)
    for clave, contenido in zip(partes[1::2], partes[2::2], strict=True):
        soluciones[clave] = re.split(r"\\section\*", contenido)[0]
    return soluciones


def archivo_de(id_capitulo):
    carpeta = ANEXOS if id_capitulo.startswith("anexo") else CAPITULOS
    return carpeta / f"{id_capitulo}.tex"


def ids_de_capitulos():
    ids = {}
    for archivo in [*CAPITULOS.glob("cap*.tex"), *ANEXOS_WEB]:
        etiqueta = re.search(
            r"\\label\{(cap:[^}]+)\}", archivo.read_text(encoding="utf-8")
        )
        if etiqueta:
            ids[etiqueta.group(1)] = archivo.stem
    return ids


def huella(archivo):
    """Huella del contenido del .tex: cambia si y solo si el capítulo cambia."""
    contenido = archivo.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha1(contenido).hexdigest()[:10]


def convertir(id_capitulo):
    archivo = archivo_de(id_capitulo)
    texto = quitar_comentarios(archivo.read_text(encoding="utf-8"))
    etiquetas = leer_etiquetas()
    cabecera = re.search(r"\\chapter\{(.*?)\}\\label\{(cap:[^}]+)\}", texto)
    if cabecera:
        numero_capitulo = etiquetas[cabecera.group(2)]
        nombre_destino = id_capitulo
    else:
        # Capítulo sin número (\addchap), como el prefacio: va primero en la web.
        cabecera = re.search(r"\\addchap\{(.*?)\}", texto)
        numero_capitulo = "0"
        nombre_destino = f"cap00_{id_capitulo}"
    convertidor = Convertidor(
        numero_capitulo,
        etiquetas,
        leer_soluciones(),
        ids_de_capitulos(),
        leer_valores(),
    )
    cuerpo = convertidor.bloques(texto[cabecera.end() :])
    cuerpo = re.sub(r"[ \t]+\n", "\n", cuerpo)
    cuerpo = re.sub(r"\n{3,}", "\n\n", cuerpo).strip()
    titulo = cabecera.group(1).replace('"', '\\"')
    # Los capítulos sin código (como el 1) no tienen notebooks que enlazar.
    notebooks = ""
    if (NOTEBOOKS / f"{id_capitulo}.ipynb").exists():
        notebooks = (
            f'<NotebooksDelCapitulo id="{id_capitulo}"'
            f' capitulo="{int(numero_capitulo):02d}" />\n\n'
        )
    # Los capítulos se numeran con enteros; los anexos, con letras.
    if numero_capitulo.isdigit():
        numero = int(numero_capitulo)
    else:
        numero = f'"{numero_capitulo}"'
    origen = archivo.relative_to(RAIZ).as_posix()
    mdx = (
        "export const metadatos = {\n"
        f"  numero: {numero},\n"
        f'  titulo: "{titulo}",\n'
        f'  sincronizado_con: "{huella(archivo)}",\n'
        "};\n\n"
        f"{{/* Generado por scripts/latex_a_mdx.py desde {origen}."
        " No editar a mano. */}\n\n"
        f"{notebooks}{cuerpo}\n"
    )
    destino = DESTINO / f"{nombre_destino}.mdx"
    destino.write_text(mdx, encoding="utf-8", newline="\n")
    return destino


def todos_los_capitulos():
    capitulos = sorted(archivo.stem for archivo in CAPITULOS.glob("cap*.tex"))
    anexos = sorted(archivo.stem for archivo in ANEXOS_WEB)
    return ["prefacio", *capitulos, *anexos]


def copiar_capturas():
    """Copia capturas/*.png a la web; la carpeta del libro es la fuente única."""
    destino = RAIZ / "web" / "public" / "capturas"
    destino.mkdir(parents=True, exist_ok=True)
    vigentes = set()
    for captura in sorted(CAPTURAS.glob("*.png")):
        shutil.copy2(captura, destino / captura.name)
        vigentes.add(captura.name)
    for vieja in destino.glob("*.png"):
        if vieja.name not in vigentes:
            vieja.unlink()


if __name__ == "__main__":
    copiar_capturas()
    for id_capitulo in sys.argv[1:] or todos_los_capitulos():
        print(f"generado: {convertir(id_capitulo).relative_to(RAIZ)}")
