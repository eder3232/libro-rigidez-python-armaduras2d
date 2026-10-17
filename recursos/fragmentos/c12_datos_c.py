# Ejemplo C: puente peatonal tipo Pratt, 6 paneles de
# 3 m (luz de 18 m) y 3 m de altura. Unidades: kN y m

# Nodos: cordón inferior (1 a 7) y superior (8 a 12)
nodos_c = {}
for k in range(7):
    nodos_c[k + 1] = {"x": 3.0 * k, "y": 0.0}
for k in range(5):
    nodos_c[k + 8] = {"x": 3.0 * (k + 1), "y": 3.0}


def barra(i, j, area, elasticidad=2.0e8):
    """Datos de una barra del nodo i al nodo j."""
    return {"nodo_inicial": i, "nodo_final": j,
            "elasticidad": elasticidad, "area": area}


A_CORDON = 0.0030  # m², cordones y diagonales extremas
A_ALMA = 0.0015    # m², montantes y diagonales

barras_c = {
    # Cordón inferior
    1: barra(1, 2, A_CORDON), 2: barra(2, 3, A_CORDON),
    3: barra(3, 4, A_CORDON), 4: barra(4, 5, A_CORDON),
    5: barra(5, 6, A_CORDON), 6: barra(6, 7, A_CORDON),
    # Cordón superior
    7: barra(8, 9, A_CORDON), 8: barra(9, 10, A_CORDON),
    9: barra(10, 11, A_CORDON),
    10: barra(11, 12, A_CORDON),
    # Diagonales extremas
    11: barra(1, 8, A_CORDON), 12: barra(12, 7, A_CORDON),
    # Montantes
    13: barra(2, 8, A_ALMA), 14: barra(3, 9, A_ALMA),
    15: barra(4, 10, A_ALMA), 16: barra(5, 11, A_ALMA),
    17: barra(6, 12, A_ALMA),
    # Diagonales, descendiendo hacia el centro
    18: barra(8, 3, A_ALMA), 19: barra(9, 4, A_ALMA),
    20: barra(11, 4, A_ALMA), 21: barra(12, 5, A_ALMA),
}

apoyos_c = {
    1: {"x": True, "y": True},   # articulado
    7: {"x": False, "y": True},  # rodillo
}

# 25 kN en cada nodo interior del cordón inferior
cargas_c = {}
for nodo in range(2, 7):
    cargas_c[nodo] = {"x": 0.0, "y": -25.0}
