# %% [markdown]
# # Soluciones del capítulo 12

# %% [markdown]
# ## Ejercicio 12.1

# %%
# [inicio: s12_ejercicio_1]
resultados_c = analizar_armadura(nodos_c, barras_c,
                                 apoyos_c, cargas_c)
iy = indices([8])[0]  # gdl 8: nodo 4, dirección y
flecha = -resultados_c["U"][iy] * 1000
print(f"Flecha en el centro: {flecha:.2f} mm")
print(f"Luz / flecha: {18000 / flecha:.0f}")
# [fin: s12_ejercicio_1]

# %% [markdown]
# ## Ejercicio 12.2

# %%
# [inicio: s12_ejercicio_2]
nodos_cubierta = {
    1: {"x": 0.0, "y": 0.0},
    2: {"x": 4.0, "y": 0.0},
    3: {"x": 8.0, "y": 0.0},
    4: {"x": 4.0, "y": 1.5},
}
barras_cubierta = {
    1: barra(1, 2, 0.0015), 2: barra(2, 3, 0.0015),
    3: barra(1, 4, 0.0015), 4: barra(4, 3, 0.0015),
    5: barra(2, 4, 0.0010),
}
apoyos_cubierta = {
    1: {"x": True, "y": True},
    3: {"x": False, "y": True},
}
cargas_cubierta = {4: {"x": 0.0, "y": -30.0}}

resultados = analizar_armadura(
    nodos_cubierta, barras_cubierta, apoyos_cubierta,
    cargas_cubierta)
verificar_resultados(nodos_cubierta, barras_cubierta,
                     resultados)
mostrar_resultados(nodos_cubierta, barras_cubierta,
                   resultados)
# [fin: s12_ejercicio_2]

# %% [markdown]
# ## Ejercicio 12.3

# %%
# [inicio: s12_ejercicio_3]
# Viento: 10 kN horizontales en cada nodo superior
cargas_viento = {}
for nodo in range(2, 7):
    cargas_viento[nodo] = {"x": 0.0, "y": -25.0}
for nodo in range(8, 13):
    cargas_viento[nodo] = {"x": 10.0, "y": 0.0}

resultados_v = analizar_armadura(nodos_c, barras_c,
                                 apoyos_c, cargas_viento)
verificar_resultados(nodos_c, barras_c, resultados_v)
graficar_resultados(nodos_c, barras_c, resultados_v,
                    "Ejemplo C con viento", decimales=0,
                    tamano=7)
# [fin: s12_ejercicio_3]

# %% [markdown]
# ## Ejercicio 12.4

# %%
# [inicio: s12_ejercicio_4]
# Sin las diagonales 18 y 19, el tramo izquierdo
# queda formado por rectángulos sin arriostrar
barras_sin_diagonales = {}
for numero, datos in barras_c.items():
    if numero not in (18, 19):
        barras_sin_diagonales[numero] = datos

try:
    analizar_armadura(nodos_c, barras_sin_diagonales,
                      apoyos_c, cargas_c)
except ValueError as error:
    print(f"No se puede analizar. {error}")
# [fin: s12_ejercicio_4]
