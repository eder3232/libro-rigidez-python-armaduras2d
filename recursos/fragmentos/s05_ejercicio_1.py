def peso_barra(A, L, gamma=78.5):
    """Peso propio de una barra, en kN."""
    return gamma * A * L


peso_total = 0.0
for numero, barra in barras.items():
    L = geometria[numero]["longitud"]
    peso_total += peso_barra(barra["area"], L)
print(f"Peso propio: {peso_total:.3f} kN")
