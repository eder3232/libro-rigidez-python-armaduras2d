def rigidez_local(E, A, L):
    """Matriz de rigidez de la barra en sus ejes (2x2)."""
    return E * A / L * np.array([[1.0, -1.0],
                                 [-1.0, 1.0]])


def matriz_transformacion(c, s):
    """Matriz T (2 x 4) tal que u' = T u."""
    return np.array([[c, s, 0.0, 0.0],
                     [0.0, 0.0, c, s]])


def rigidez_barra(E, A, L, c, s):
    """Matriz de rigidez de la barra en ejes globales."""
    T = matriz_transformacion(c, s)
    return T.T @ rigidez_local(E, A, L) @ T
