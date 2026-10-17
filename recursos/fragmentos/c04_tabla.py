print("Barra   L (m)       c       s")
for numero, g in geometria.items():
    L, c, s = g["longitud"], g["c"], g["s"]
    print(f"{numero:>5} {L:7.3f} {c:7.4f} {s:7.4f}")
