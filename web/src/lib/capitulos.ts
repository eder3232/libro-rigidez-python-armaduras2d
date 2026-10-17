// Capítulos disponibles en contenido/: un archivo capNN_nombre.mdx por capítulo
// (cap00 es el prefacio) y uno anexoX_nombre.mdx por anexo.
import { readdirSync } from "node:fs";
import path from "node:path";

const CARPETA = path.join(process.cwd(), "contenido");
const PATRON = /^(cap\d{2}|anexo[A-Z])_[a-z0-9_]+\.mdx$/;

// Metadatos que cada capítulo exporta con `export const metadatos = {...}`.
export type Metadatos = {
  // 0 en el prefacio, un entero en los capítulos y una letra en los anexos
  numero: number | string;
  titulo: string;
  // Commit del .tex con el que se sincronizó (docs/04-sincronizacion.md)
  sincronizado_con: string;
};

export function idsDeCapitulos(): string[] {
  // Primero los capítulos y después los anexos, cada grupo en orden.
  const orden = (archivo: string) => (archivo.startsWith("anexo") ? `1${archivo}` : `0${archivo}`);
  return readdirSync(CARPETA)
    .filter((archivo) => PATRON.test(archivo))
    .sort((a, b) => orden(a).localeCompare(orden(b)))
    .map((archivo) => archivo.replace(/\.mdx$/, ""));
}

// Rótulo que precede al título: "Capítulo 3", "Anexo A" o nada en el prefacio.
export function rotulo(numero: Metadatos["numero"]): string {
  if (typeof numero === "string") return `Anexo ${numero}`;
  return numero > 0 ? `Capítulo ${numero}` : "";
}

export async function cargarCapitulo(id: string) {
  const modulo = await import(`../../contenido/${id}.mdx`);
  return {
    Contenido: modulo.default as React.ComponentType,
    metadatos: modulo.metadatos as Metadatos,
  };
}
