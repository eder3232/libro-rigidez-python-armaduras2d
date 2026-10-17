resultados = analizar_armadura(nodos, barras, apoyos,
                               cargas)
print(list(resultados.keys()))
for numero, fuerza in resultados["N"].items():
    print(f"Barra {numero}: N = {fuerza:.2f} kN")
