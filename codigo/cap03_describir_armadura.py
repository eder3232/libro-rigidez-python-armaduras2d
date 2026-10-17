# %% [markdown]
# # Capítulo 3. Describir una armadura
#
# Este notebook acompaña al capítulo 3 del libro *Análisis matricial de
# armaduras con Python*. Construimos el modelo de datos del ejemplo A:
# nodos, barras, apoyos y cargas.

# %% [markdown]
# ## 3.2 Listas

# %% tags=["exploracion"]
# [inicio: c03_lista]
coordenadas_nodo_3 = [3.0, 4.0]
coordenadas_nodo_3
# [fin: c03_lista]

# %% tags=["exploracion"]
# [inicio: c03_indices]
coordenadas_nodo_3[0], coordenadas_nodo_3[1]
# [fin: c03_indices]

# %% tags=["exploracion"]
# [inicio: c03_areas]
# Áreas de las barras 1, 2 y 3, en m²
areas = [0.0020, 0.0020, 0.0015]
areas[2]
# [fin: c03_areas]

# %% tags=["exploracion"]
# [inicio: c03_append]
areas.append(0.0030)
len(areas), areas
# [fin: c03_append]

# %% [markdown]
# ## 3.3 Diccionarios

# %% tags=["exploracion"]
# [inicio: c03_diccionario]
nodo_3 = {"x": 3.0, "y": 4.0}
nodo_3["y"]
# [fin: c03_diccionario]

# %% tags=["exploracion"]
# [inicio: c03_claves_numericas]
# Las claves son los números de barra, empezando en 1
areas = {1: 0.0020, 2: 0.0020, 3: 0.0015}
areas[3]
# [fin: c03_claves_numericas]

# %% [markdown]
# ## 3.4 El modelo del ejemplo A

# %% tags=["acumulable"]
# [inicio: c03_nodos]
# Ejemplo A. Unidades: kN y m
nodos = {
    1: {"x": 0.0, "y": 0.0},
    2: {"x": 6.0, "y": 0.0},
    3: {"x": 3.0, "y": 4.0},
}
# [fin: c03_nodos]

# %% tags=["acumulable"]
# [inicio: c03_barras]
# E en kN/m² (acero) y área en m²
barras = {
    1: {"nodo_inicial": 1, "nodo_final": 2,
        "elasticidad": 2.0e8, "area": 0.0020},
    2: {"nodo_inicial": 2, "nodo_final": 3,
        "elasticidad": 2.0e8, "area": 0.0020},
    3: {"nodo_inicial": 1, "nodo_final": 3,
        "elasticidad": 2.0e8, "area": 0.0020},
}
# [fin: c03_barras]

# %% tags=["acumulable"]
# [inicio: c03_apoyos]
# True: el desplazamiento en esa dirección está impedido
apoyos = {
    1: {"x": True, "y": True},   # articulado
    2: {"x": False, "y": True},  # rodillo
}
# [fin: c03_apoyos]

# %% tags=["acumulable"]
# [inicio: c03_cargas]
# Cargas en kN, positivas en el sentido de los ejes
cargas = {
    3: {"x": 20.0, "y": -50.0},
}
# [fin: c03_cargas]

# %% [markdown]
# ## 3.5 Consultar el modelo

# %% tags=["exploracion"]
# [inicio: c03_consulta]
barras[2]["nodo_inicial"], barras[2]["nodo_final"]
# [fin: c03_consulta]

# %% tags=["exploracion"]
# [inicio: c03_consulta_encadenada]
inicial = barras[2]["nodo_inicial"]
nodos[inicial]["x"], nodos[inicial]["y"]
# [fin: c03_consulta_encadenada]

# %% tags=["exploracion"]
# [inicio: c03_in]
3 in apoyos, 3 in cargas
# [fin: c03_in]

# %% tags=["exploracion"]
# [inicio: c03_get]
print(apoyos.get(3))
print(apoyos.get(3, "sin apoyo"))
# [fin: c03_get]

# %% tags=["exploracion"]
# [inicio: c03_len]
print(f"Nodos: {len(nodos)}, barras: {len(barras)}")
# [fin: c03_len]

# %% [markdown]
# ## 3.6 Ver la armadura

# %% tags=["acumulable"]
# [inicio: c03_import_plt]
import matplotlib.pyplot as plt
# [fin: c03_import_plt]

# %% tags=["exploracion"]
# [inicio: c03_dibujo]
n1, n2, n3 = nodos[1], nodos[2], nodos[3]

fig, ax = plt.subplots()
# Barra 1: del nodo 1 al nodo 2
ax.plot([n1["x"], n2["x"]], [n1["y"], n2["y"]], "k-o")
# Barra 2: del nodo 2 al nodo 3
ax.plot([n2["x"], n3["x"]], [n2["y"], n3["y"]], "k-o")
# Barra 3: del nodo 1 al nodo 3
ax.plot([n1["x"], n3["x"]], [n1["y"], n3["y"]], "k-o")
ax.set_aspect("equal")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_title("Ejemplo A")
plt.show()
# [fin: c03_dibujo]

# %% [markdown]
# ## Problema resuelto 3.1: el modelo del ejemplo B

# %% tags=["exploracion"]
# [inicio: c03_problema_resuelto]
# Ejemplo B. Unidades: kN y m
nodos_b = {
    1: {"x": 0.0, "y": 0.0},
    2: {"x": 3.0, "y": 0.0},
    3: {"x": 0.0, "y": 4.0},
    4: {"x": 3.0, "y": 4.0},
}

barras_b = {
    1: {"nodo_inicial": 1, "nodo_final": 2,
        "elasticidad": 2.0e8, "area": 0.0020},
    2: {"nodo_inicial": 2, "nodo_final": 4,
        "elasticidad": 2.0e8, "area": 0.0020},
    3: {"nodo_inicial": 3, "nodo_final": 4,
        "elasticidad": 2.0e8, "area": 0.0020},
    4: {"nodo_inicial": 1, "nodo_final": 3,
        "elasticidad": 2.0e8, "area": 0.0020},
    5: {"nodo_inicial": 1, "nodo_final": 4,
        "elasticidad": 2.0e8, "area": 0.0020},
    6: {"nodo_inicial": 2, "nodo_final": 3,
        "elasticidad": 2.0e8, "area": 0.0020},
}

apoyos_b = {
    1: {"x": True, "y": True},   # articulado
    2: {"x": False, "y": True},  # rodillo
}

cargas_b = {
    3: {"x": 30.0, "y": -40.0},
    4: {"x": 0.0, "y": -40.0},
}

inicial = barras_b[5]["nodo_inicial"]
final = barras_b[5]["nodo_final"]
print(f"Nodos: {len(nodos_b)}, barras: {len(barras_b)}")
print(f"Barra 5: del nodo {inicial} al nodo {final}")
# [fin: c03_problema_resuelto]

# %% [markdown]
# ## Ejercicios
#
# Resuelva cada ejercicio en su notebook y después ejecute la celda de
# verificación correspondiente.

# %% tags=["exploracion"]
# Ejercicio 3.1: longitud de la barra 3 del ejemplo A, en m
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif abs(respuesta - 5.0) < 1e-3:
    print("Correcto.")
else:
    print("Todavía no. ¿Tomó las coordenadas de los nodos 1 y 3?")

# %% tags=["exploracion"]
# Ejercicio 3.2: verifica los diccionarios de la armadura de cubierta
try:
    correcto = (
        len(nodos_cubierta) == 4
        and len(barras_cubierta) == 5
        and apoyos_cubierta[3] == {"x": False, "y": True}
        and cargas_cubierta[4]["y"] == -30.0
    )
except NameError:
    print("Defina nodos_cubierta, barras_cubierta, apoyos_cubierta "
          "y cargas_cubierta, y vuelva a ejecutar la celda.")
else:
    if correcto:
        print("Correcto.")
    else:
        print("Todavía no. Revise la cantidad de nodos y barras, "
              "el rodillo del nodo 3 y la carga del nodo 4.")
