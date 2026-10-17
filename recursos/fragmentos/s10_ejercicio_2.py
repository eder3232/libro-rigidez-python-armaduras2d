apoyos_2 = {
    1: {"x": True, "y": True},
    2: {"x": True, "y": True},
}
libres_2, restringidos_2 = clasificar_gdl(nodos, apoyos_2)
K_ll_2, K_lr_2, _, _ = particionar(K_global, libres_2,
                                   restringidos_2)
U_2 = np.zeros(6)
U_2[indices(libres_2)] = resolver_desplazamientos(
    K_ll_2, K_lr_2, F[indices(libres_2)],
    np.zeros(len(restringidos_2)))
N_2 = fuerzas_axiales(barras, geometria, U_2)
filas = []
for numero in barras:
    filas.append([str(numero), N[numero], N_2[numero]])
mostrar_tabla(["Barra", "Rodillo", "Articulado"], filas)
