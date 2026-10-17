import { readFileSync } from "node:fs";
import path from "node:path";
import createMDX from "@next/mdx";
import type { NextConfig } from "next";

// La notación matemática tiene una sola fuente: el archivo de macros del libro.
// Cada línea "\newcommand{\nombre}[n]{definición}" se convierte en una macro de KaTeX.
function leerMacros(): Record<string, string> {
  const archivo = path.join(process.cwd(), "..", "libro", "estilo", "notacion.tex");
  const patron = /^\\newcommand\{(\\[A-Za-z]+)\}(?:\[\d\])?\{(.*)\}\s*$/;
  const macros: Record<string, string> = {};
  for (const linea of readFileSync(archivo, "utf-8").split(/\r?\n/)) {
    const coincidencia = linea.match(patron);
    if (coincidencia) macros[coincidencia[1]] = coincidencia[2];
  }
  return macros;
}

const nextConfig: NextConfig = {
  output: "export",
  pageExtensions: ["ts", "tsx", "mdx"],
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

const withMDX = createMDX({
  options: {
    remarkPlugins: ["remark-gfm", "remark-math"],
    rehypePlugins: [["rehype-katex", { macros: leerMacros(), strict: true }]],
  },
});

export default withMDX(nextConfig);
