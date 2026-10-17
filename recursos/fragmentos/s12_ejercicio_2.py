nodos_cubierta = {
    1: {"x": 0.0, "y": 0.0},
    2: {"x": 4.0, "y": 0.0},
    3: {"x": 8.0, "y": 0.0},
    4: {"x": 4.0, "y": 1.5},
}
barras_cubierta = {
    1: barra(1, 2, 0.0015), 2: barra(2, 3, 0.0015),
    3: barra(1, 4, 0.0015), 4: barra(4, 3, 0.0015),
    5: barra(2, 4, 0.0010),
}
apoyos_cubierta = {
    1: {"x": True, "y": True},
    3: {"x": False, "y": True},
}
cargas_cubierta = {4: {"x": 0.0, "y": -30.0}}

resultados = analizar_armadura(
    nodos_cubierta, barras_cubierta, apoyos_cubierta,
    cargas_cubierta)
verificar_resultados(nodos_cubierta, barras_cubierta,
                     resultados)
mostrar_resultados(nodos_cubierta, barras_cubierta,
                   resultados)
