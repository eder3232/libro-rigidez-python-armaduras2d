def comparar_resultados(nodos, calculadora, opensees,
                        tolerancia=1e-9):
    """Muestra los dos análisis lado a lado e indica si
    coinciden."""
    filas = []
    for nodo in nodos:
        for direccion, g in zip("xy", gdl_del_nodo(nodo)):
            i = indices([g])[0]
            filas.append([f"u{direccion} {nodo} (mm)",
                          calculadora["U"][i] * 1000,
                          opensees["U"][i] * 1000])
    restringidos = calculadora["restringidos"]
    for posicion, g in enumerate(restringidos):
        filas.append([f"R{g} (kN)",
                      calculadora["R"][posicion],
                      opensees["R"][posicion]])
    for numero in calculadora["N"]:
        filas.append([f"N{numero} (kN)",
                      calculadora["N"][numero],
                      opensees["N"][numero]])
    mostrar_tabla(["Resultado", "Calculadora",
                   "OpenSees"], filas, decimales=3,
                  ancho=13)
    diferencia = 0.0
    for _, valor_calculadora, valor_opensees in filas:
        diferencia = max(diferencia, abs(
            valor_calculadora - valor_opensees))
    if diferencia < tolerancia:
        print("\nLos dos análisis coinciden.")
    else:
        print(f"\nDifieren hasta en {diferencia:.3g}.")
