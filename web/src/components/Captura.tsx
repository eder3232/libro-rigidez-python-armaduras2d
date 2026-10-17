// Captura de pantalla: capturas/<archivo>.png en la raíz del repositorio, que
// scripts/latex_a_mdx.py copia a public/capturas. Equivale a \captura dentro de
// un figure. Mientras la imagen no exista, un recuadro indica cuál debe ir.
import { existsSync } from "node:fs";
import path from "node:path";

export function Captura({
  archivo,
  numero,
  descripcion,
  children,
}: {
  archivo: string;
  numero: string;
  descripcion: string;
  children: React.ReactNode;
}) {
  const existe = existsSync(path.join(process.cwd(), "public", "capturas", `${archivo}.png`));
  return (
    <figure className="figura">
      {existe ? (
        // eslint-disable-next-line @next/next/no-img-element -- imagen estática
        <img src={`/capturas/${archivo}.png`} alt={descripcion} />
      ) : (
        <div className="captura-pendiente">
          Aquí debe ir la captura <code>{archivo}.png</code>:<br />
          {descripcion}
        </div>
      )}
      <figcaption>
        <strong>Figura {numero}:</strong> {children}
      </figcaption>
    </figure>
  );
}
