import type { Metadata } from "next";
import { cargarCapitulo, idsDeCapitulos } from "@/lib/capitulos";

export const dynamicParams = false;

export function generateStaticParams() {
  return idsDeCapitulos().map((id) => ({ id }));
}

export async function generateMetadata({
  params,
}: PageProps<"/capitulos/[id]">): Promise<Metadata> {
  const { id } = await params;
  const { metadatos } = await cargarCapitulo(id);
  // El número 0 corresponde al prefacio, que no tiene número de capítulo.
  if (metadatos.numero === 0) return { title: metadatos.titulo };
  return { title: `${metadatos.numero}. ${metadatos.titulo}` };
}

export default async function Capitulo({ params }: PageProps<"/capitulos/[id]">) {
  const { id } = await params;
  const { Contenido, metadatos } = await cargarCapitulo(id);
  return (
    <article className="prosa">
      {metadatos.numero > 0 && <p className="capitulo-numero">Capítulo {metadatos.numero}</p>}
      <h1>{metadatos.titulo}</h1>
      <Contenido />
    </article>
  );
}
