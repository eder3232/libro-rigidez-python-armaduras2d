import type { MDXComponents } from "mdx/types";
import {
  Cuidado,
  EcuacionClave,
  Estrategia,
  Objetivos,
  ParaSaberMas,
  ProblemaResuelto,
  PuntoDeControl,
  Python,
  Recuerda,
  Solucion,
} from "@/components/cajas";
import { Fragmento } from "@/components/Fragmento";
import { Salida } from "@/components/Salida";

// Componentes disponibles en todos los capítulos sin importarlos.
const componentes: MDXComponents = {
  Recuerda,
  Python,
  Cuidado,
  ParaSaberMas,
  Objetivos,
  PuntoDeControl,
  Estrategia,
  ProblemaResuelto,
  Solucion,
  EcuacionClave,
  Fragmento,
  Salida,
};

export function useMDXComponents(): MDXComponents {
  return componentes;
}
