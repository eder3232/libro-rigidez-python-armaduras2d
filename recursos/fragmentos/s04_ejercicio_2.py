gamma = 78.5  # peso específico del acero, en kN/m³
peso_total = 0.0
for numero, barra in barras.items():
    L = geometria[numero]["longitud"]
    peso_total += gamma * barra["area"] * L
print(f"Peso propio: {peso_total:.3f} kN")
