// Gráfico que dibuja un fragmento, generado por scripts/generar_salidas.py.
// Equivale a \grafico{nombre} en LaTeX; con número y leyenda, a un \grafico
// dentro de un figure.
import { existsSync } from "node:fs";
import path from "node:path";

export function Grafico({
  nombre,
  numero,
  children,
}: {
  nombre: string;
  numero?: string;
  children?: React.ReactNode;
}) {
  const archivo = path.join(process.cwd(), "public", "graficos", `${nombre}.svg`);
  if (!existsSync(archivo)) {
    throw new Error(
      `No existe el gráfico '${nombre}'. Ejecute scripts/generar_salidas.py o revise el nombre.`,
    );
  }
  return (
    <figure className={numero ? "figura" : "grafico"}>
      {/* eslint-disable-next-line @next/next/no-img-element -- SVG estático */}
      <img src={`/graficos/${nombre}.svg`} alt="" />
      {numero && (
        <figcaption>
          <strong>Figura {numero}:</strong> {children}
        </figcaption>
      )}
    </figure>
  );
}
