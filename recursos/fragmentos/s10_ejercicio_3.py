barras_dobles = {}
for numero, barra in barras.items():
    copia = dict(barra)
    copia["area"] = 2 * barra["area"]
    barras_dobles[numero] = copia

geometria_d = calcular_geometria(nodos, barras_dobles)
rigideces_d = calcular_rigideces(barras_dobles,
                                 geometria_d)
K_d = ensamblar_rigidez(nodos, barras_dobles,
                        rigideces_d)
K_ll_d, K_lr_d, _, _ = particionar(K_d, libres,
                                   restringidos)
U_d = np.zeros(6)
U_d[indices(libres)] = resolver_desplazamientos(
    K_ll_d, K_lr_d, F_l, U_r)
N_d = fuerzas_axiales(barras_dobles, geometria_d, U_d)
print(f"Desplazamientos a la mitad: "
      f"{np.allclose(U_d, U / 2)}")
filas = []
for numero in barras:
    filas.append([str(numero), N[numero], N_d[numero]])
mostrar_tabla(["Barra", "N (kN)", "N, 2A (kN)"], filas)
