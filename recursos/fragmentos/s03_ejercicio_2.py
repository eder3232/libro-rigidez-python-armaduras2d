# Armadura de cubierta. Unidades: kN y m
nodos_cubierta = {
    1: {"x": 0.0, "y": 0.0},
    2: {"x": 4.0, "y": 0.0},
    3: {"x": 8.0, "y": 0.0},
    4: {"x": 4.0, "y": 1.5},
}

barras_cubierta = {
    1: {"nodo_inicial": 1, "nodo_final": 2,
        "elasticidad": 2.0e8, "area": 0.0015},
    2: {"nodo_inicial": 2, "nodo_final": 3,
        "elasticidad": 2.0e8, "area": 0.0015},
    3: {"nodo_inicial": 1, "nodo_final": 4,
        "elasticidad": 2.0e8, "area": 0.0015},
    4: {"nodo_inicial": 4, "nodo_final": 3,
        "elasticidad": 2.0e8, "area": 0.0015},
    5: {"nodo_inicial": 2, "nodo_final": 4,
        "elasticidad": 2.0e8, "area": 0.0010},
}

apoyos_cubierta = {
    1: {"x": True, "y": True},   # articulado
    3: {"x": False, "y": True},  # rodillo
}

cargas_cubierta = {
    4: {"x": 0.0, "y": -30.0},
}

print(f"Nodos: {len(nodos_cubierta)}")
print(f"Barras: {len(barras_cubierta)}")
