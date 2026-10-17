import Link from "next/link";
import { cargarCapitulo, idsDeCapitulos } from "@/lib/capitulos";

export default async function Portada() {
  const capitulos = await Promise.all(
    idsDeCapitulos().map(async (id) => ({ id, ...(await cargarCapitulo(id)).metadatos })),
  );
  return (
    <div className="prosa">
      <h1>Análisis matricial de armaduras con Python</h1>
      <p className="capitulo-numero">
        Aprende el método de rigidez construyendo tu propia calculadora
      </p>
      <h2>Contenido</h2>
      <ol className="indice">
        {capitulos.map((capitulo) => (
          <li key={capitulo.id}>
            <span>{capitulo.numero === 0 ? "" : capitulo.numero}</span>
            <Link href={`/capitulos/${capitulo.id}`}>{capitulo.titulo}</Link>
          </li>
        ))}
      </ol>
    </div>
  );
}
