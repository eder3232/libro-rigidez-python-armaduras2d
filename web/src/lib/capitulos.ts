// Capítulos disponibles en contenido/ (un archivo capNN_nombre.mdx por capítulo).
import { readdirSync } from "node:fs";
import path from "node:path";

const CARPETA = path.join(process.cwd(), "contenido");
const PATRON = /^cap(\d{2})_[a-z0-9_]+\.mdx$/;

// Metadatos que cada capítulo exporta con `export const metadatos = {...}`.
export type Metadatos = {
  numero: number;
  titulo: string;
  // Commit del .tex con el que se sincronizó (docs/04-sincronizacion.md)
  sincronizado_con: string;
};

export function idsDeCapitulos(): string[] {
  return readdirSync(CARPETA)
    .filter((archivo) => PATRON.test(archivo))
    .sort()
    .map((archivo) => archivo.replace(/\.mdx$/, ""));
}

export async function cargarCapitulo(id: string) {
  const modulo = await import(`../../contenido/${id}.mdx`);
  return {
    Contenido: modulo.default as React.ComponentType,
    metadatos: modulo.metadatos as Metadatos,
  };
}
