def indices(gdl):
    """Traduce grados de libertad (desde 1) a índices
    de NumPy (desde 0). Es el único lugar del libro donde
    se hace esta traducción."""
    resultado = []
    for g in gdl:
        resultado.append(g - 1)
    return resultado
