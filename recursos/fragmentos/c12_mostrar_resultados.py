def mostrar_resultados(nodos, barras, resultados):
    """Tablas de desplazamientos, reacciones y fuerzas."""
    U = resultados["U"]
    R = resultados["R"]
    N = resultados["N"]
    print("Desplazamientos de los nodos (mm)")
    filas = []
    for nodo in nodos:
        ix, iy = indices(gdl_del_nodo(nodo))
        filas.append([str(nodo), U[ix] * 1000,
                      U[iy] * 1000])
    mostrar_tabla(["Nodo", "ux", "uy"], filas,
                  decimales=3)

    print("\nReacciones (kN)")
    filas = []
    restringidos = resultados["restringidos"]
    for posicion, g in enumerate(restringidos):
        nodo = (g + 1) // 2
        if g % 2 == 1:
            direccion = "x"
        else:
            direccion = "y"
        filas.append([str(nodo), direccion, R[posicion]])
    mostrar_tabla(["Nodo", "Dirección", "R"], filas)

    print("\nFuerzas axiales")
    filas = []
    for numero, fuerza in N.items():
        sigma = fuerza / barras[numero]["area"] / 1000
        filas.append([str(numero), fuerza, sigma,
                      clasificar_fuerza(fuerza)])
    encabezados = ["Barra", "N (kN)", "σ (MPa)", "Estado"]
    mostrar_tabla(encabezados, filas)
