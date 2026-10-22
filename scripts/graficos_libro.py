"""Figuras de validación del anexo D, con el aspecto de los esquemas del libro.

Solo las usa el libro (celdas "libro" de codigo/anexoD_validacion.py): no
forman parte de los notebooks. Los símbolos (apoyos, cargas, nodos) imitan a
los de libro/estilo/simbolos.tex y se miden en puntos tipográficos, de modo
que tienen el mismo tamaño en todas las figuras, sea cual sea la armadura.

La tipografía la fija configurar_graficos() de generar_salidas.py.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.lines import Line2D

# Paleta del libro (libro/estilo/base.sty)
PRINCIPAL = "#1F4E79"
ACENTO = "#C8641E"
TEXTO_SUAVE = "#5A5A5A"
TRACCION = "#0072B2"
COMPRESION = "#D55E00"
NEUTRO = "#8C8C8C"
TINTA = "#333333"  # black!80 de los esquemas TikZ
GUIA = "#9A9A9A"  # ejes y líneas de referencia

ANCHO_TEXTO = 4.5  # pulgadas: el ancho de los gráficos del libro
PT = 1 / 72  # un punto, en pulgadas
DISCONTINUA = (0, (4, 2.5))
SUPERINDICES = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def kn(valor, decimales=2):
    """Un número con el signo menos tipográfico, como en el texto."""
    return f"{round(valor, decimales) + 0.0:.{decimales}f}".replace("-", "−")


def cientifico(numero):
    """Un número pequeño como 3 × 10⁻¹⁴, o 0 si es nulo."""
    if numero == 0:
        return "0"
    exponente = int(np.floor(np.log10(numero)))
    mantisa = round(numero / 10**exponente)
    if mantisa == 10:
        mantisa, exponente = 1, exponente + 1
    return f"{mantisa} × 10{str(exponente).translate(SUPERINDICES)}"


class Lienzo:
    """Una figura con una armadura dibujada a escala real (aspect = 1).

    Las coordenadas se dan en metros; los tamaños de los símbolos, en puntos.
    Los márgenes (en puntos: izquierdo, derecho, inferior, superior) dejan
    espacio a apoyos, cargas y rótulos. La armadura ocupa el ancho dado, salvo
    que así supere el alto máximo: entonces se reduce el ancho.
    """

    def __init__(self, puntos, ancho=ANCHO_TEXTO, alto_maximo=3.0,
                 margenes=(30, 30, 30, 30)):
        izquierdo, derecho, inferior, superior = margenes
        xs = [p[0] for p in puntos]
        ys = [p[1] for p in puntos]
        luz = max(xs) - min(xs)
        alto = max(ys) - min(ys)
        # Metros del dibujo por pulgada de papel
        self.escala = max(
            luz / (ancho - (izquierdo + derecho) * PT),
            alto / (alto_maximo - (inferior + superior) * PT),
        )
        ancho = luz / self.escala + (izquierdo + derecho) * PT
        altura = alto / self.escala + (inferior + superior) * PT
        self.fig = plt.figure(figsize=(ancho, altura))
        self.fig.patch.set_alpha(0)
        self.ax = self.fig.add_axes((0, 0, 1, 1))
        self.ax.set_xlim(min(xs) - self.pt(izquierdo), max(xs) + self.pt(derecho))
        self.ax.set_ylim(min(ys) - self.pt(inferior), max(ys) + self.pt(superior))
        self.ax.set_aspect("equal")
        self.ax.axis("off")

    def pt(self, puntos):
        """Convierte una longitud en puntos a metros del dibujo."""
        return puntos * PT * self.escala

    def barra(self, i, j, **estilo):
        estilo = {"color": TINTA, "linewidth": 1.6, "solid_capstyle": "round"} | estilo
        self.ax.plot([i[0], j[0]], [i[1], j[1]], **estilo)

    def nodo(self, punto, radio=2.6):
        self.ax.add_patch(
            patches.Circle(punto, self.pt(radio), facecolor="white", edgecolor=TINTA,
                           linewidth=1, zorder=6)
        )

    def apoyo(self, punto, rodillo=False):
        """Apoyo articulado o de rodillo bajo el punto, como en simbolos.tex.

        Devuelve la altura del borde inferior del apoyo.
        """
        x, y = punto
        medio, alto = self.pt(6.2), self.pt(8 if rodillo else 9)
        self.ax.add_patch(
            patches.Polygon([(x, y), (x - medio, y - alto), (x + medio, y - alto)],
                            facecolor="#EBEBEB", edgecolor=TINTA, linewidth=0.9,
                            zorder=4)
        )
        base = y - alto
        if rodillo:
            radio = self.pt(1.4)
            for dx in (-3.7, 0, 3.7):
                self.ax.add_patch(
                    patches.Circle((x + self.pt(dx), base - radio), radio,
                                   facecolor="white", edgecolor=TINTA, linewidth=0.7,
                                   zorder=4)
                )
            base -= 2 * radio
        ancho, grueso = self.pt(9.6), self.pt(3.4)
        self.ax.add_patch(
            patches.Rectangle((x - ancho, base - grueso), 2 * ancho, grueso,
                              facecolor="none", edgecolor=GUIA, hatch="//////",
                              linewidth=0, zorder=3)
        )
        self.ax.plot([x - ancho, x + ancho], [base, base], color=TINTA, linewidth=0.9,
                     zorder=4)
        return base - grueso

    def flecha(self, punto, direccion, texto, color, largo=24, sale=False,
               separacion=4, tamano=8.5):
        """Flecha de una fuerza, con su rótulo en el extremo libre.

        Por defecto la punta llega al punto (la fuerza empuja); con sale=True la
        flecha parte del punto (la fuerza tira, como una carga colgada).
        """
        sentido = np.asarray(direccion, float) / np.hypot(*direccion)
        punto = np.asarray(punto, float)
        if sale:
            inicio = punto + self.pt(separacion) * sentido
            fin = inicio + self.pt(largo) * sentido
            libre, hacia_rotulo = fin, sentido
        else:
            fin = punto - self.pt(separacion) * sentido
            inicio = fin - self.pt(largo) * sentido
            libre, hacia_rotulo = inicio, -sentido
        self.ax.annotate(
            "", xy=fin, xytext=inicio,
            arrowprops={"arrowstyle": "-|>,head_length=0.55,head_width=0.22",
                        "color": color, "linewidth": 1.2, "shrinkA": 0, "shrinkB": 0},
            annotation_clip=False, zorder=5,
        )
        if texto:
            # El rótulo se aparta de la flecha, en su misma dirección
            dx, dy = hacia_rotulo
            ha = "center" if abs(dx) < 0.5 else ("left" if dx > 0 else "right")
            va = "center" if abs(dy) < 0.5 else ("bottom" if dy > 0 else "top")
            self.ax.text(*(libre + self.pt(2) * hacia_rotulo), texto, color=color,
                         fontsize=tamano, ha=ha, va=va, zorder=7)

    def rotulo(self, punto, texto, color=TINTA, tamano=8.5):
        self.ax.text(*punto, texto, color=color, fontsize=tamano, ha="center",
                     va="center", zorder=7,
                     bbox={"boxstyle": "round,pad=0.15,rounding_size=0.2",
                           "facecolor": "white", "edgecolor": "none"})

    def leyenda(self, elementos, titulo=None, tamano=8.5, largo=2.4, columnas=None):
        """Leyenda debajo del dibujo, para no tapar las barras."""
        self.ax.legend(
            handles=elementos, loc="upper center", bbox_to_anchor=(0.5, 0),
            ncol=columnas or len(elementos), frameon=False, fontsize=tamano,
            title=titulo, title_fontsize=tamano, handlelength=largo,
            columnspacing=1.4,
        )


def _coordenadas(nodos):
    return {n: (p["x"], p["y"]) for n, p in nodos.items()}


def _desplazados(nodos, U, escala):
    return {
        n: (p["x"] + escala * U[2 * n - 2], p["y"] + escala * U[2 * n - 1])
        for n, p in nodos.items()
    }


def _escala(nodos, U, fraccion):
    """Escala para que el mayor desplazamiento dibujado sea una fracción de la
    altura de la armadura (la luz, si es plana), redondeada a 1, 2 o 5 × 10ⁿ."""
    xy = np.array(list(_coordenadas(nodos).values()))
    luz, alto = np.ptp(xy, axis=0)
    escala = fraccion * (alto or luz) / np.abs(U).max()
    potencia = 10 ** np.floor(np.log10(escala))
    return max(m for m in (1, 2, 5) if m * potencia <= escala) * potencia


def _apoyos(lienzo, nodos, apoyos):
    xy = _coordenadas(nodos)
    return {n: lienzo.apoyo(xy[n], rodillo=not a["x"]) for n, a in apoyos.items()}


def _cargas(lienzo, puntos, cargas, colgadas, tamano):
    """Las cargas de los nodos, una flecha por componente.

    colgadas: las cargas verticales hacia abajo salen del nodo hacia abajo,
    como un peso colgado, en lugar de llegar a él desde arriba.
    """
    for nodo, carga in cargas.items():
        for componente, direccion in (("x", (1, 0)), ("y", (0, 1))):
            valor = carga[componente]
            if valor:
                sentido = np.sign(valor) * np.array(direccion)
                sale = colgadas and componente == "y" and valor < 0
                lienzo.flecha(puntos[nodo], sentido, f"{abs(valor):g} kN", ACENTO,
                              sale=sale, tamano=tamano)


# ---------------------------------------------------------------------------
# Deformada y fuerzas axiales
# ---------------------------------------------------------------------------


def figura_deformada(nodos, barras, apoyos, cargas, calculadora, opensees,
                     ancho=ANCHO_TEXTO, alto_maximo=3.0, fraccion=0.15, numeros=True,
                     cargas_colgadas=False, tamano=8.5, margenes=(40, 40, 26, 40)):
    """Deformadas de OpenSees y de la calculadora, superpuestas.

    OpenSees se dibuja con un trazo grueso y translúcido, y la calculadora con
    uno fino encima: si coinciden, el trazo fino corre dentro del grueso.
    """
    U_calc, U_ops = calculadora["U"], opensees["U"]
    escala = _escala(nodos, U_ops, fraccion)
    original = _coordenadas(nodos)
    def_ops = _desplazados(nodos, U_ops, escala)
    def_calc = _desplazados(nodos, U_calc, escala)

    lienzo = Lienzo(list(original.values()) + list(def_ops.values()), ancho,
                    alto_maximo, margenes)
    for barra in barras.values():
        i, j = barra["nodo_inicial"], barra["nodo_final"]
        lienzo.barra(original[i], original[j], color=NEUTRO, linewidth=0.9,
                     linestyle=DISCONTINUA, zorder=1)
        lienzo.barra(def_ops[i], def_ops[j], color=PRINCIPAL, linewidth=6.5,
                     alpha=0.25, zorder=2)
        lienzo.barra(def_calc[i], def_calc[j], color=ACENTO, linewidth=1.3, zorder=3)
    for punto in original.values():
        lienzo.ax.plot(*punto, "o", color=NEUTRO, markersize=2.6, zorder=2)
    for punto in def_calc.values():
        lienzo.ax.plot(*punto, "o", color=ACENTO, markersize=3, zorder=4)
    _apoyos(lienzo, nodos, apoyos)
    # Las cargas acompañan a los nodos en su posición deformada
    _cargas(lienzo, def_ops, cargas, cargas_colgadas, tamano)

    if numeros:
        centro = np.mean([p[0] for p in original.values()])
        for nodo, (x, y) in def_ops.items():
            lado = -1 if original[nodo][0] < centro else 1
            lienzo.ax.text(x + lienzo.pt(8) * lado, y + lienzo.pt(5), str(nodo),
                           color=PRINCIPAL, fontsize=tamano, fontweight="bold",
                           ha="center", va="center", zorder=7)

    # El nodo que más se desplaza, con los dos valores, en la leyenda
    magnitud = {n: np.hypot(U_ops[2 * n - 2], U_ops[2 * n - 1]) for n in nodos}
    nodo = max(magnitud, key=magnitud.get)
    u_calc = 1000 * np.hypot(U_calc[2 * nodo - 2], U_calc[2 * nodo - 1])
    u_ops = 1000 * magnitud[nodo]
    lienzo.ax.add_patch(
        patches.Circle(def_ops[nodo], lienzo.pt(7), facecolor="none",
                       edgecolor=PRINCIPAL, linewidth=0.8, zorder=5)
    )
    lienzo.leyenda(
        [
            Line2D([], [], color=NEUTRO, linewidth=0.9, linestyle=DISCONTINUA,
                   label="Original"),
            Line2D([], [], color=PRINCIPAL, linewidth=6.5, alpha=0.25,
                   label="OpenSees"),
            Line2D([], [], color=ACENTO, linewidth=1.3, marker="o", markersize=3,
                   label="Calculadora"),
        ],
        titulo=(f"Desplazamientos ampliados ×{escala:g}. Nodo {nodo} (circulado):\n"
                f"{u_calc:.3f} mm en la calculadora y {u_ops:.3f} mm en OpenSees"),
        tamano=tamano,
    )
    lienzo.ax.get_legend().get_title().set_linespacing(1.4)
    return lienzo.fig


def figura_axiales(nodos, barras, apoyos, cargas, opensees, ancho=ANCHO_TEXTO,
                   alto_maximo=3.0, posicion=0.4, decimales=2, cargas_colgadas=False,
                   tamano=8.5, grosor_maximo=7.0, margenes=(46, 46, 46, 40)):
    """Diagrama de fuerzas axiales de OpenSees, con apoyos, cargas y reacciones.

    El grosor de cada barra es proporcional a su fuerza. Los valores van al
    40 % de cada barra (posicion), para que no se tapen los de dos diagonales
    que se cruzan, como en dibujar_fuerzas del capítulo 11.
    """
    N = opensees["N"]
    xy = _coordenadas(nodos)
    lienzo = Lienzo(list(xy.values()), ancho, alto_maximo, margenes)
    maxima = max(abs(f) for f in N.values())
    nula = 1e-6 * maxima
    for numero, barra in barras.items():
        i, j = xy[barra["nodo_inicial"]], xy[barra["nodo_final"]]
        fuerza = N[numero]
        if abs(fuerza) < nula:
            lienzo.barra(i, j, color=NEUTRO, linewidth=1, linestyle=DISCONTINUA,
                         zorder=2)
            color, texto = TEXTO_SUAVE, "0"
        else:
            color = TRACCION if fuerza > 0 else COMPRESION
            grosor = 1.4 + (grosor_maximo - 1.4) * abs(fuerza) / maxima
            lienzo.barra(i, j, color=color, linewidth=grosor, zorder=2)
            texto = kn(fuerza, decimales)
        punto = np.asarray(i) + posicion * (np.asarray(j) - np.asarray(i))
        lienzo.rotulo(punto, texto, color=color, tamano=tamano)
    for punto in xy.values():
        lienzo.nodo(punto)
    bases = _apoyos(lienzo, nodos, apoyos)
    _cargas(lienzo, xy, cargas, cargas_colgadas, tamano)

    # Reacciones, siempre por fuera de la armadura: la vertical, bajo el apoyo;
    # la horizontal, al costado del apoyo que da hacia afuera.
    centro = np.mean([p[0] for p in xy.values()])
    for posicion_r, g in enumerate(opensees["restringidos"]):
        valor = opensees["R"][posicion_r]
        if abs(valor) < nula:
            continue
        nodo = (g + 1) // 2
        x, y = xy[nodo]
        texto = f"{abs(valor):.{decimales}f} kN"
        if g % 2 == 1:
            afuera = -1 if x < centro else 1
            sentido = (np.sign(valor), 0)
            lienzo.flecha((x + afuera * lienzo.pt(8), y - lienzo.pt(5)), sentido,
                          texto, PRINCIPAL, largo=20, separacion=0,
                          sale=np.sign(valor) == afuera, tamano=tamano)
        else:
            base = (x, bases[nodo] - lienzo.pt(2))
            lienzo.flecha(base, (0, np.sign(valor)), texto, PRINCIPAL, largo=20,
                          separacion=0, sale=valor < 0, tamano=tamano)

    elementos = [
        Line2D([], [], color=TRACCION, linewidth=3.5, label="Tracción"),
        Line2D([], [], color=COMPRESION, linewidth=3.5, label="Compresión"),
    ]
    if any(abs(f) < nula for f in N.values()):
        elementos.append(Line2D([], [], color=NEUTRO, linewidth=1,
                                linestyle=DISCONTINUA, label="Sin fuerza"))
    elementos += [
        Line2D([], [], color=ACENTO, linewidth=1.2, marker=">", markersize=4,
               markevery=[1], label="Carga"),
        Line2D([], [], color=PRINCIPAL, linewidth=1.2, marker=">", markersize=4,
               markevery=[1], label="Reacción"),
    ]
    lienzo.leyenda(elementos, titulo="Fuerzas axiales de OpenSees, en kN",
                   tamano=tamano, largo=1.8)
    return lienzo.fig


# ---------------------------------------------------------------------------
# Todas las comparaciones
# ---------------------------------------------------------------------------


def _grupos(ejemplos):
    """Agrupa todos los resultados por ejemplo y tipo.

    ejemplos: [(nombre, resultados de la calculadora, de OpenSees)]. Devuelve
    [(nombre, tipo, unidad, valores de la calculadora, de OpenSees)].
    """
    grupos = []
    for nombre, calculadora, opensees in ejemplos:
        grupos.append((nombre, "Desplazamientos", "mm",
                       1000 * np.asarray(calculadora["U"]),
                       1000 * np.asarray(opensees["U"])))
        grupos.append((nombre, "Reacciones", "kN",
                       np.asarray(calculadora["R"]), np.asarray(opensees["R"])))
        barras = list(calculadora["N"])
        grupos.append((nombre, "Fuerzas", "kN",
                       np.array([calculadora["N"][b] for b in barras]),
                       np.array([opensees["N"][b] for b in barras])))
    return grupos


ABREVIATURAS = {"Desplazamientos": "Despl.", "Reacciones": "Reacc.", "Fuerzas": "Fuerzas"}


def _colores(grupos):
    nombres = list(dict.fromkeys(g[0] for g in grupos))
    return {n: [PRINCIPAL, ACENTO][k % 2] for k, n in enumerate(nombres)}


def _estilo_ejes(ax, tamano=7.5):
    ax.set_facecolor("none")
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GUIA)
    ax.tick_params(labelsize=tamano, colors=TEXTO_SUAVE, length=2.5, pad=2)


def figura_diferencias(ejemplos, tolerancia=0.01):
    """Diferencia relativa de cada resultado, en escala logarítmica.

    Cada diferencia se divide por el mayor valor de su grupo: así no se divide
    por cero en los apoyos, y todas quedan en la misma escala que la tolerancia
    de la validación. Las diferencias exactamente nulas se dibujan abajo, con
    un círculo vacío.
    """
    grupos = _grupos(ejemplos)
    colores = _colores(grupos)
    piso, techo = 1e-19, 10
    fig, ax = plt.subplots(figsize=(ANCHO_TEXTO, 2.6))
    fig.patch.set_alpha(0)
    _estilo_ejes(ax)
    ax.set_yscale("log")
    ax.set_ylim(piso / 4, techo)

    # Por encima de la tolerancia, la validación fallaría
    ax.axhspan(tolerancia, techo, color=COMPRESION, alpha=0.07, linewidth=0)
    ax.axhline(tolerancia, color=COMPRESION, linewidth=0.8)
    eps = np.finfo(float).eps
    ax.axhline(eps, color=GUIA, linewidth=0.8, linestyle=DISCONTINUA)
    ax.text(1.015, tolerancia, "tolerancia\n(1 %)", transform=ax.get_yaxis_transform(),
            ha="left", va="center", fontsize=7.5, color=COMPRESION, linespacing=1.15)
    ax.text(1.015, eps, "precisión de\nla máquina", transform=ax.get_yaxis_transform(),
            ha="left", va="center", fontsize=7.5, color=TEXTO_SUAVE, linespacing=1.15)
    ax.text(1.015, piso, "iguales", transform=ax.get_yaxis_transform(), ha="left",
            va="center", fontsize=7.5, color=TEXTO_SUAVE)

    for k, (nombre, tipo, _, calc, ops) in enumerate(grupos):
        diferencia = np.abs(calc - ops) / np.abs(ops).max()
        # Los puntos se reparten a lo ancho de su columna, sin azar
        x = k + np.linspace(-0.32, 0.32, len(calc)) if len(calc) > 1 else np.array([k])
        nulas = diferencia == 0
        color = colores[nombre]
        ax.plot(x[~nulas], diferencia[~nulas], "o", color=color, markersize=3.4,
                alpha=0.9, markeredgewidth=0)
        ax.plot(x[nulas], np.full(nulas.sum(), piso), "o", markerfacecolor="white",
                markeredgecolor=color, markersize=3.4, markeredgewidth=0.8)
        ax.text(k, -0.04, f"{ABREVIATURAS[tipo]}\n({len(calc)})",
                transform=ax.get_xaxis_transform(),
                ha="center", va="top", fontsize=7, color=TEXTO_SUAVE, linespacing=1.2)
    por_ejemplo = len(grupos) // len(colores)
    for k, (nombre, color) in enumerate(colores.items()):
        centro = k * por_ejemplo + (por_ejemplo - 1) / 2
        ax.text(centro, 1.02, nombre, transform=ax.get_xaxis_transform(), ha="center",
                va="bottom", fontsize=8.5, color=color, fontweight="bold")
        if k:
            ax.axvline(k * por_ejemplo - 0.5, color="#DDDDDD", linewidth=0.7, zorder=0)

    ax.set_xlim(-0.6, len(grupos) - 0.4)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.set_yticks([1e-16, 1e-12, 1e-8, 1e-4, 1])
    ax.set_yticklabels(["10⁻¹⁶", "10⁻¹²", "10⁻⁸", "10⁻⁴", "1"])
    ax.minorticks_off()
    ax.set_ylabel("Diferencia relativa", fontsize=8, color=TEXTO_SUAVE)
    fig.tight_layout()
    return fig


def figura_paridad(ejemplos):
    """OpenSees frente a la calculadora: si coinciden, sobre la recta y = x."""
    grupos = _grupos(ejemplos)
    colores = _colores(grupos)
    marcas = dict(zip(colores, "os"))
    fig, ejes = plt.subplots(1, 3, figsize=(ANCHO_TEXTO, 1.95))
    fig.patch.set_alpha(0)
    for ax, tipo in zip(ejes, ["Desplazamientos", "Reacciones", "Fuerzas"]):
        _estilo_ejes(ax, tamano=7)
        datos = [g for g in grupos if g[1] == tipo]
        unidad = datos[0][2]
        todos = np.concatenate([np.concatenate([g[3], g[4]]) for g in datos])
        margen = 0.1 * np.ptp(todos)
        limites = (todos.min() - margen, todos.max() + margen)
        ax.plot(limites, limites, color=GUIA, linewidth=0.8, linestyle=DISCONTINUA,
                zorder=1)
        diferencia = 0.0
        for nombre, _, _, calc, ops in datos:
            ax.plot(calc, ops, marcas[nombre], markerfacecolor="none",
                    markeredgecolor=colores[nombre], markersize=4.2,
                    markeredgewidth=0.9, label=nombre, zorder=2)
            diferencia = max(diferencia, np.abs(calc - ops).max())
        ax.set_xlim(limites)
        ax.set_ylim(limites)
        ax.set_aspect("equal")
        ax.set_title(f"{tipo} ({unidad})", fontsize=8, color=TINTA, pad=4)
        ax.text(0.04, 0.97, f"máx. dif.:\n{cientifico(diferencia)} {unidad}",
                transform=ax.transAxes, ha="left", va="top", fontsize=6.8,
                color=TEXTO_SUAVE, linespacing=1.25)
        ax.locator_params(nbins=4)
        ax.set_xlabel("Calculadora", fontsize=7.5, color=TEXTO_SUAVE, labelpad=2)
    ejes[0].set_ylabel("OpenSees", fontsize=7.5, color=TEXTO_SUAVE, labelpad=2)
    asas, etiquetas = ejes[0].get_legend_handles_labels()
    fig.legend(asas, etiquetas, loc="lower center", ncol=2, frameon=False, fontsize=8,
               bbox_to_anchor=(0.5, -0.07), columnspacing=2.5)
    fig.tight_layout(w_pad=1.2)
    return fig
