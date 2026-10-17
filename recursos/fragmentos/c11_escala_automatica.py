def escala_automatica(nodos, U, fraccion=0.1):
    """Escala para que el mayor desplazamiento dibujado
    sea una fracción del tamaño de la armadura."""
    xs = []
    ys = []
    for punto in nodos.values():
        xs.append(punto["x"])
        ys.append(punto["y"])
    tamano = max(max(xs) - min(xs), max(ys) - min(ys))
    return fraccion * tamano / np.abs(U).max()
