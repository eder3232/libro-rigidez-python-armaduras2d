g = geometria[2]
EA_L = 2.0e8 * 0.0020 / g["longitud"]
c, s = g["c"], g["s"]
print(f"EA/L = {EA_L:.0f} kN/m, c = {c:.1f}, s = {s:.1f}")
print(f"EA/L·c²  = {EA_L * c**2:9.1f}")
print(f"EA/L·cs  = {EA_L * c * s:9.1f}")
print(f"EA/L·s²  = {EA_L * s**2:9.1f}")
rigideces[2]
