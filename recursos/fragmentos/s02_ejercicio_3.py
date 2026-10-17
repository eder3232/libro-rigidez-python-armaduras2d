E = 2.0e8  # kN/m²
A = 0.0020  # m²
L = 5.0  # m
rigidez_axial = E * A / L
print(f"EA/L = {rigidez_axial:.0f} kN/m")
