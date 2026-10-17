for numero, barra in barras_b.items():
    print(f"Barra {numero}: {gdl_de_barra(barra)}")

libres_b, restringidos_b = clasificar_gdl(
    nodos_b, apoyos_b)
print(f"Libres:       {libres_b}")
print(f"Restringidos: {restringidos_b}")

grado_b = indeterminacion(nodos_b, barras_b,
                          restringidos_b)
print(f"Grado de indeterminación: {grado_b}")
