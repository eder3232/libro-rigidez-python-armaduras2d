def indeterminacion(nodos, barras, restringidos):
    """b + r - 2n: incógnitas menos ecuaciones."""
    b, r, n = len(barras), len(restringidos), len(nodos)
    return b + r - 2 * n
