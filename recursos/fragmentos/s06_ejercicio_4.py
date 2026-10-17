nueva_numeracion = libres + restringidos
for nuevo, original in enumerate(nueva_numeracion, 1):
    print(f"GDL {original} → {nuevo}")
