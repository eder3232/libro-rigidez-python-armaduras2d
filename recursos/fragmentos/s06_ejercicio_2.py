apoyos_articulados = {
    1: {"x": True, "y": True},
    2: {"x": True, "y": True},
}
libres_2, restringidos_2 = clasificar_gdl(
    nodos, apoyos_articulados)
print(f"Libres:       {libres_2}")
print(f"Restringidos: {restringidos_2}")
grado = indeterminacion(nodos, barras, restringidos_2)
print(f"Grado de indeterminación: {grado}")
