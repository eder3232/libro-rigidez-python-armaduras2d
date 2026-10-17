// Ejercicios con su solución plegable (decisión D15).
import type { ReactNode } from "react";

export function Ejercicio({ numero, children }: { numero: string; children: ReactNode }) {
  return (
    <div className="ejercicio">
      <p className="ejercicio-numero">Ejercicio {numero}</p>
      {children}
    </div>
  );
}

export function SolucionDelEjercicio({ children }: { children: ReactNode }) {
  return (
    <details className="solucion-ejercicio">
      <summary>Ver la solución</summary>
      {children}
    </details>
  );
}
