# Ejemplo B. Unidades: kN y m
nodos_b = {
    1: {"x": 0.0, "y": 0.0},
    2: {"x": 3.0, "y": 0.0},
    3: {"x": 0.0, "y": 4.0},
    4: {"x": 3.0, "y": 4.0},
}

barras_b = {
    1: {"nodo_inicial": 1, "nodo_final": 2,
        "elasticidad": 2.0e8, "area": 0.0020},
    2: {"nodo_inicial": 2, "nodo_final": 4,
        "elasticidad": 2.0e8, "area": 0.0020},
    3: {"nodo_inicial": 3, "nodo_final": 4,
        "elasticidad": 2.0e8, "area": 0.0020},
    4: {"nodo_inicial": 1, "nodo_final": 3,
        "elasticidad": 2.0e8, "area": 0.0020},
    5: {"nodo_inicial": 1, "nodo_final": 4,
        "elasticidad": 2.0e8, "area": 0.0020},
    6: {"nodo_inicial": 2, "nodo_final": 3,
        "elasticidad": 2.0e8, "area": 0.0020},
}

apoyos_b = {
    1: {"x": True, "y": True},   # articulado
    2: {"x": False, "y": True},  # rodillo
}

cargas_b = {
    3: {"x": 30.0, "y": -40.0},
    4: {"x": 0.0, "y": -40.0},
}

inicial = barras_b[5]["nodo_inicial"]
final = barras_b[5]["nodo_final"]
print(f"Nodos: {len(nodos_b)}, barras: {len(barras_b)}")
print(f"Barra 5: del nodo {inicial} al nodo {final}")
