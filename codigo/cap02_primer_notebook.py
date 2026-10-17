# %% [markdown]
# # Capítulo 2. Nuestro primer notebook
#
# Este notebook acompaña al capítulo 2 del libro *Análisis matricial de
# armaduras con Python*. Lo recomendable es escribir el código en **su propio
# notebook** de Google Drive, siguiendo el texto del libro; este notebook sirve
# como referencia o para recuperarse si algo no funcionó.

# %% [markdown]
# ## 2.2 Nuestro primer notebook

# %% tags=["exploracion"]
# [inicio: c02_primera_celda]
print("Hola, armaduras")
# [fin: c02_primera_celda]

# %% tags=["exploracion"]
# [inicio: c02_operaciones]
2 + 3 * 4
# [fin: c02_operaciones]

# %% [markdown]
# ## 2.3 Variables y operaciones

# %% tags=["exploracion"]
# [inicio: c02_variables]
# Coordenadas (en m) del nodo inicial i y del nodo final j
x_i = 0.0
y_i = 0.0
x_j = 3.0
y_j = 4.0
# [fin: c02_variables]

# %% tags=["exploracion"]
# [inicio: c02_diferencias]
dx = x_j - x_i
dy = y_j - y_i
dx, dy
# [fin: c02_diferencias]

# %% tags=["exploracion"]
# [inicio: c02_potencia]
dx**2 + dy**2
# [fin: c02_potencia]

# %% tags=["exploracion"]
# [inicio: c02_notacion_cientifica]
E = 2.0e8  # módulo de elasticidad del acero, en kN/m²
A = 0.0020  # área de la sección, en m²
E * A
# [fin: c02_notacion_cientifica]

# %% [markdown]
# ## 2.4 El módulo `math`

# %% tags=["acumulable"]
# [inicio: c02_import_math]
import math
# [fin: c02_import_math]

# %% tags=["exploracion"]
# [inicio: c02_longitud]
L = math.sqrt(dx**2 + dy**2)
L
# [fin: c02_longitud]

# %% tags=["exploracion"]
# [inicio: c02_cosenos]
c = dx / L
s = dy / L
c, s
# [fin: c02_cosenos]

# %% tags=["exploracion"]
# [inicio: c02_angulo]
theta = math.degrees(math.atan2(dy, dx))
theta
# [fin: c02_angulo]

# %% [markdown]
# ## 2.5 Mostrar resultados con `print` y f-strings

# %% tags=["exploracion"]
# [inicio: c02_fstring]
print(f"Longitud: L = {L:.3f} m")
print(f"Cosenos directores: c = {c:.4f}, s = {s:.4f}")
print(f"Ángulo: θ = {theta:.2f}°")
# [fin: c02_fstring]

# %% [markdown]
# ## 2.6 La geometría de una barra en Python
#
# Problema resuelto 2.1: la barra 2 del ejemplo A.

# %% tags=["exploracion"]
# [inicio: c02_problema_resuelto]
# Barra 2 del ejemplo A: del nodo 2 al nodo 3
x_i, y_i = 6.0, 0.0
x_j, y_j = 3.0, 4.0

dx = x_j - x_i
dy = y_j - y_i
L = math.sqrt(dx**2 + dy**2)
c = dx / L
s = dy / L
theta = math.degrees(math.atan2(dy, dx))

print(f"L = {L:.3f} m")
print(f"c = {c:.4f}, s = {s:.4f}")
print(f"θ = {theta:.2f}°")
# [fin: c02_problema_resuelto]

# %% tags=["exploracion"]
# [inicio: c02_atan_cuidado]
math.degrees(math.atan(dy / dx))
# [fin: c02_atan_cuidado]

# %% [markdown]
# ## Ejercicios
#
# Resuelva cada ejercicio en su notebook. Después escriba su resultado en la
# celda de verificación correspondiente y ejecútela.

# %% tags=["exploracion"]
# Ejercicio 2.1: longitud de la barra 1 del ejemplo A, en metros
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif math.isclose(respuesta, 6.0, rel_tol=1e-3):
    print("Correcto.")
else:
    print("Todavía no. Revise las coordenadas de los nodos 1 y 2.")

# %% tags=["exploracion"]
# Ejercicio 2.2: ángulo θ de la barra de cubierta, en grados
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif math.isclose(respuesta, 18.435, rel_tol=1e-3):
    print("Correcto.")
else:
    print("Todavía no. ¿Usó math.atan2 y convirtió el resultado a grados?")

# %% tags=["exploracion"]
# Ejercicio 2.3: rigidez axial EA/L de la barra 3 del ejemplo A, en kN/m
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif math.isclose(respuesta, 80_000, rel_tol=1e-3):
    print("Correcto.")
else:
    print("Todavía no. Revise las unidades: E en kN/m², A en m² y L en m.")

# %% tags=["exploracion"]
# Ejercicio 2.5: ángulo θ de la barra vertical, en grados
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif math.isclose(respuesta, -90.0, rel_tol=1e-3):
    print("Correcto.")
else:
    print("Todavía no. La barra apunta hacia abajo: ¿qué signo tiene dy?")
