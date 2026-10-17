grado = indeterminacion(nodos, barras, restringidos)
if grado < 0:
    print(f"Inestable: faltan {-grado} barras o apoyos")
elif grado == 0:
    print("Estáticamente determinada (isostática)")
else:
    print(f"Hiperestática de grado {grado}")
