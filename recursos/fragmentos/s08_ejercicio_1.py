F_b = ensamblar_cargas(nodos_b, cargas_b)
print(f"Ejemplo B, en x: {F_b[0::2].sum():7.2f} kN")
print(f"Ejemplo B, en y: {F_b[1::2].sum():7.2f} kN")
