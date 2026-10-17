barras_sin_1 = {2: barras[2], 3: barras[3]}
K_sin_1 = ensamblar_rigidez(nodos, barras_sin_1,
                            rigideces)
K_ll_sin_1, K_lr_sin_1, _, _ = particionar(
    K_sin_1, libres, restringidos)
try:
    resolver_desplazamientos(K_ll_sin_1, K_lr_sin_1,
                             F_l, U_r)
except ValueError as error:
    print(f"No se puede resolver. {error}")
