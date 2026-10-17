// Gráfico que dibuja un fragmento, generado por scripts/generar_salidas.py.
// Equivale a \grafico{nombre} en LaTeX.
import { existsSync } from "node:fs";
import path from "node:path";

export function Grafico({ nombre }: { nombre: string }) {
  const archivo = path.join(process.cwd(), "public", "graficos", `${nombre}.svg`);
  if (!existsSync(archivo)) {
    throw new Error(
      `No existe el gráfico '${nombre}'. Ejecute scripts/generar_salidas.py o revise el nombre.`,
    );
  }
  return (
    <figure className="grafico">
      {/* eslint-disable-next-line @next/next/no-img-element -- SVG estático */}
      <img src={`/graficos/${nombre}.svg`} alt="" />
    </figure>
  );
}
