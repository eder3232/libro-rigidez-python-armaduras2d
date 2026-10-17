def verificar_resultados(nodos, barras, resultados,
                         tolerancia=1e-6):
    """Equilibrio global y de cada nodo. Devuelve True
    si ambos se cumplen dentro de la tolerancia."""
    F, R = resultados["F"], resultados["R"]
    restringidos = resultados["restringidos"]
    suma_x, suma_y, momento = comprobar_equilibrio(
        nodos, F, R, restringidos)
    global_ok = max(abs(suma_x), abs(suma_y),
                    abs(momento)) < tolerancia
    nodal_ok = equilibrio_nodal(
        nodos, barras, resultados["geometria"],
        resultados["N"], F, R, restringidos) < tolerancia
    for nombre, correcto in (("global", global_ok),
                             ("nodal", nodal_ok)):
        if correcto:
            print(f"Equilibrio {nombre}: correcto")
        else:
            print(f"Equilibrio {nombre}: ERROR")
    return global_ok and nodal_ok
