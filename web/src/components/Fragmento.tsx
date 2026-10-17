// Fragmento de código con una sola fuente en codigo/, extraído por
// scripts/extraer_fragmentos.py. Equivale a \fragmento{nombre} en LaTeX.
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";

const CARPETA = path.join(process.cwd(), "..", "recursos", "fragmentos");

export function Fragmento({ nombre }: { nombre: string }) {
  const archivo = path.join(CARPETA, `${nombre}.py`);
  if (!existsSync(archivo)) {
    throw new Error(
      `No existe el fragmento '${nombre}'. Ejecute scripts/extraer_fragmentos.py o revise el nombre.`,
    );
  }
  return (
    <pre>
      <code className="language-python">{readFileSync(archivo, "utf-8")}</code>
    </pre>
  );
}
