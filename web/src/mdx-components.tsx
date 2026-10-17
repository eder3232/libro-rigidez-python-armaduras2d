import type { MDXComponents } from "mdx/types";
import {
  Cuidado,
  Objetivos,
  ParaSaberMas,
  PuntoDeControl,
  Python,
  Recuerda,
} from "@/components/cajas";
import { Fragmento } from "@/components/Fragmento";

// Componentes disponibles en todos los capítulos sin importarlos.
const componentes: MDXComponents = {
  Recuerda,
  Python,
  Cuidado,
  ParaSaberMas,
  Objetivos,
  PuntoDeControl,
  Fragmento,
};

export function useMDXComponents(): MDXComponents {
  return componentes;
}
