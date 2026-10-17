// Salida de un fragmento, generada por scripts/generar_salidas.py.
// Equivale a \salida{nombre} en LaTeX.
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";

const CARPETA = path.join(process.cwd(), "..", "recursos", "salidas");

export function Salida({ nombre }: { nombre: string }) {
  const archivo = path.join(CARPETA, `${nombre}.txt`);
  if (!existsSync(archivo)) {
    throw new Error(
      `No existe la salida '${nombre}'. Ejecute scripts/generar_salidas.py o revise el nombre.`,
    );
  }
  return <pre className="salida">{readFileSync(archivo, "utf-8")}</pre>;
}
