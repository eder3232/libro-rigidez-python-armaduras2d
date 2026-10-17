// Cajas del libro: equivalen a los entornos semánticos de libro/estilo/armaduras.sty.
import type { ReactNode } from "react";

const URL_NOTEBOOKS =
  "https://github.com/USUARIO/libro-rigidez-python-armaduras2d/blob/main/notebooks";

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
