// Cajas del libro: equivalen a los entornos semánticos de libro/estilo/armaduras.sty.
import type { ReactNode } from "react";

const URL_NOTEBOOKS =
  "https://github.com/eder3232/libro-rigidez-python-armaduras2d/blob/main/notebooks";

type Tono = "principal" | "traccion" | "acento" | "neutro";

function Caja({ titulo, tono, children }: { titulo: string; tono: Tono; children: ReactNode }) {
  return (
    <aside className={`caja caja-${tono}`}>
      <p className="caja-titulo">{titulo}</p>
      {children}
    </aside>
  );
}

export function Recuerda({ children }: { children: ReactNode }) {
  return <Caja titulo="Recuerda" tono="principal">{children}</Caja>;
}

export function Python({ children }: { children: ReactNode }) {
  return <Caja titulo="Python" tono="traccion">{children}</Caja>;
}

export function Cuidado({ children }: { children: ReactNode }) {
  return <Caja titulo="Cuidado" tono="acento">{children}</Caja>;
}

export function ParaSaberMas({ children }: { children: ReactNode }) {
  return <Caja titulo="Para saber más" tono="neutro">{children}</Caja>;
}

export function Objetivos({ children }: { children: ReactNode }) {
  return <Caja titulo="Al terminar este capítulo podremos" tono="principal">{children}</Caja>;
}

export function PuntoDeControl({ capitulo }: { capitulo: string }) {
  const notebook = `${URL_NOTEBOOKS}/control_cap${capitulo}.ipynb`;
  const colab = notebook.replace("https://github.com/", "https://colab.research.google.com/github/");
  return (
    <Caja titulo="Punto de control" tono="acento">
      <p>
        Si algo no funcionó o se omitió una parte, el notebook con todo el código hasta este
        capítulo permite continuar desde aquí.
      </p>
      <p className="caja-acciones">
        <a href={colab}>Abrir en Colab</a>
        <a href={notebook}>Ver el notebook</a>
      </p>
    </Caja>
  );
}

export function Estrategia({ children }: { children: ReactNode }) {
  return <Caja titulo="Estrategia de resolución" tono="acento">{children}</Caja>;
}

// Problema resuelto: banda de título a color, enunciado y solución.
export function ProblemaResuelto({
  numero,
  titulo,
  children,
}: {
  numero: string;
  titulo?: string;
  children: ReactNode;
}) {
  return (
    <section className="problema-resuelto">
      <p className="problema-resuelto-titulo">
        Problema resuelto {numero}
        {titulo ? ` · ${titulo}` : ""}
      </p>
      <div className="problema-resuelto-cuerpo">{children}</div>
    </section>
  );
}

export function Solucion() {
  return <p className="solucion">Solución</p>;
}

// Ecuación clave: resaltada con fondo de color.
export function EcuacionClave({ children }: { children: ReactNode }) {
  return <div className="ecuacion-clave">{children}</div>;
}

// Enlaces a los notebooks del capítulo, al inicio de cada capítulo de la web.
export function NotebooksDelCapitulo({ id, capitulo }: { id: string; capitulo: string }) {
  const colab = (archivo: string) =>
    `${URL_NOTEBOOKS}/${archivo}`.replace(
      "https://github.com/",
      "https://colab.research.google.com/github/",
    );
  return (
    <aside className="notebooks-capitulo">
      <span>Notebooks de este capítulo:</span>
      <a href={colab(`${id}.ipynb`)}>Lección</a>
      <a href={colab(`soluciones_cap${capitulo}.ipynb`)}>Soluciones</a>
      <a href={colab(`control_cap${capitulo}.ipynb`)}>Punto de control</a>
    </aside>
  );
}

// Nota breve: en el libro va al margen; en la web, en línea y atenuada.
export function Nota({ children }: { children: ReactNode }) {
  return <span className="nota">{children}</span>;
}

// El notebook final del estudiante. Equivale a \micalculadora en LaTeX.
export function MiCalculadora() {
  const notebook = `${URL_NOTEBOOKS}/mi_calculadora.ipynb`;
  const colab = notebook.replace("https://github.com/", "https://colab.research.google.com/github/");
  return (
    <Caja titulo="Mi calculadora de armaduras" tono="principal">
      <p>
        El notebook con la calculadora completa, organizado en Motor, Datos y Resultados, listo
        para copiar a nuestro Google Drive.
      </p>
      <p className="caja-acciones">
        <a href={colab}>Abrir en Colab</a>
        <a href={notebook}>Ver el notebook</a>
      </p>
    </Caja>
  );
}
