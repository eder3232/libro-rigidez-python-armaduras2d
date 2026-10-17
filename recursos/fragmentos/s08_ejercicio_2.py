cargas_2 = {
    2: {"x": 15.0, "y": 0.0},
    3: {"x": 20.0, "y": -50.0},
}
F_2 = ensamblar_cargas(nodos, cargas_2)
print(" gdl  F (kN)")
mostrar_vector(F_2, list(range(1, 7)))
print(" gdl  F_l (kN)")
mostrar_vector(F_2[indices(libres)], libres)
