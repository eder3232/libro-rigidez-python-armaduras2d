def clasificar_fuerza(N, tolerancia=1e-6):
    """Tracción, compresión o sin fuerza."""
    if N > tolerancia:
        return "tracción"
    elif N < -tolerancia:
        return "compresión"
    else:
        return "sin fuerza"
