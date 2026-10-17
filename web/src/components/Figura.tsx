// Figura con una sola fuente: libro/figuras/<nombre>.tex, convertida a SVG por
// scripts/generar_figuras.py. Equivale a \figura{nombre} dentro de un figure.
import { existsSync } from "node:fs";
import path from "node:path";

export function Figura({
  nombre,
  numero,
  children,
}: {
  nombre: string;
  numero: string;
  children: React.ReactNode;
}) {
  const archivo = path.join(process.cwd(), "public", "figuras", `${nombre}.svg`);
  if (!existsSync(archivo)) {
    throw new Error(
      `No existe la figura '${nombre}'. Ejecute scripts/generar_figuras.py o revise el nombre.`,
    );
  }
  return (
    <figure className="figura">
      {/* eslint-disable-next-line @next/next/no-img-element -- SVG estático */}
      <img src={`/figuras/${nombre}.svg`} alt="" />
      <figcaption>
        <strong>Figura {numero}:</strong> {children}
      </figcaption>
    </figure>
  );
}
