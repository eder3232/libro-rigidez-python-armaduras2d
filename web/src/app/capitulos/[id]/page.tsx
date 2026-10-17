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
  return { title: `${metadatos.numero}. ${metadatos.titulo}` };
}

export default async function Capitulo({ params }: PageProps<"/capitulos/[id]">) {
  const { id } = await params;
  const { Contenido, metadatos } = await cargarCapitulo(id);
  return (
    <article className="prosa">
      <p className="capitulo-numero">Capítulo {metadatos.numero}</p>
      <h1>{metadatos.titulo}</h1>
      <Contenido />
    </article>
  );
}
