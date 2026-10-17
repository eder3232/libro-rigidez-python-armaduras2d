# Libro web

Versión web del libro, hecha con Next.js (exportación estática).

```bash
pnpm install
pnpm dev      # servidor de desarrollo en http://localhost:3000
pnpm build    # genera el sitio estático en out/
```

- `contenido/`: un archivo `capNN_nombre.mdx` por capítulo, adaptado desde `libro/capitulos/` (ver `docs/04-sincronizacion.md`).
- `src/components/`: cajas y fragmentos de código, equivalentes a los comandos de `libro/estilo/armaduras.sty`.
- `/muestra`: muestra de diseño, equivalente a `libro/muestra.tex`.
- Las macros matemáticas se leen de `libro/estilo/notacion.tex` al compilar.
- Las fuentes de `src/fuentes/` son las mismas del PDF, con licencia SIL OFL.
