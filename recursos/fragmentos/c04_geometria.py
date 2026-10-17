geometria = {}
for numero, barra in barras.items():
    inicial = nodos[barra["nodo_inicial"]]
    final = nodos[barra["nodo_final"]]
    dx = final["x"] - inicial["x"]
    dy = final["y"] - inicial["y"]
    L = math.sqrt(dx**2 + dy**2)
    geometria[numero] = {"longitud": L,
                         "c": dx / L, "s": dy / L}
