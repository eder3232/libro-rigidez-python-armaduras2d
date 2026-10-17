import type { MDXComponents } from "mdx/types";
import {
  Cuidado,
  EcuacionClave,
  Estrategia,
  NotebooksDelCapitulo,
  Objetivos,
  ParaSaberMas,
  ProblemaResuelto,
  PuntoDeControl,
  Python,
  Recuerda,
  Solucion,
} from "@/components/cajas";
import { Ejercicio, SolucionDelEjercicio } from "@/components/ejercicios";
import { Figura } from "@/components/Figura";
import { Fragmento } from "@/components/Fragmento";
import { Grafico } from "@/components/Grafico";
import { Salida } from "@/components/Salida";

// Componentes disponibles en todos los capítulos sin importarlos.
const componentes: MDXComponents = {
  Recuerda,
  Python,
  Cuidado,
  ParaSaberMas,
  Objetivos,
  PuntoDeControl,
  NotebooksDelCapitulo,
  Estrategia,
  ProblemaResuelto,
  Solucion,
  EcuacionClave,
  Figura,
  Fragmento,
  Salida,
  Grafico,
  Ejercicio,
  SolucionDelEjercicio,
};

export function useMDXComponents(): MDXComponents {
  return componentes;
}
