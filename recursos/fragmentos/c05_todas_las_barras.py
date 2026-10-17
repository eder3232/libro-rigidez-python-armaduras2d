def calcular_rigideces(barras, geometria):
    """Matriz de rigidez global (4 x 4) de cada barra."""
    rigideces = {}
    for numero, barra in barras.items():
        g = geometria[numero]
        rigideces[numero] = rigidez_barra(
            barra["elasticidad"], barra["area"],
            g["longitud"], g["c"], g["s"])
    return rigideces


geometria = calcular_geometria(nodos, barras)
rigideces = calcular_rigideces(barras, geometria)
