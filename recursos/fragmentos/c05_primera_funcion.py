def rigidez_axial(E, A, L):
    """Rigidez axial EA/L de una barra, en kN/m."""
    return E * A / L


rigidez_axial(2.0e8, 0.0020, 5.0)
