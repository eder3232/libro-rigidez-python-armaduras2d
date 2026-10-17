# %% [markdown]
# # Soluciones del capítulo 2

# %% [markdown]
# ## Ejercicio 2.1

# %%
# [inicio: s02_ejercicio_1]
# Barra 1 del ejemplo A: de (0, 0) a (6, 0)
dx = 6.0 - 0.0
dy = 0.0 - 0.0
L = math.sqrt(dx**2 + dy**2)
c = dx / L
s = dy / L
print(f"L = {L:.3f} m")
print(f"c = {c:.4f}, s = {s:.4f}")
# [fin: s02_ejercicio_1]

# %% [markdown]
# ## Ejercicio 2.2

# %%
# [inicio: s02_ejercicio_2]
# Barra de cubierta: de (0, 0) a (4.5, 1.5)
dx = 4.5 - 0.0
dy = 1.5 - 0.0
L = math.sqrt(dx**2 + dy**2)
c = dx / L
s = dy / L
theta = math.degrees(math.atan2(dy, dx))
print(f"L = {L:.3f} m")
print(f"c = {c:.4f}, s = {s:.4f}")
print(f"θ = {theta:.2f}°")
# [fin: s02_ejercicio_2]

# %% [markdown]
# ## Ejercicio 2.3

# %%
# [inicio: s02_ejercicio_3]
E = 2.0e8  # kN/m²
A = 0.0020  # m²
L = 5.0  # m
rigidez_axial = E * A / L
print(f"EA/L = {rigidez_axial:.0f} kN/m")
# [fin: s02_ejercicio_3]

# %% [markdown]
# ## Ejercicio 2.4

# %%
# [inicio: s02_ejercicio_4]
# Barra de (6, 0) a (0, 3): hacia la izquierda y arriba
dx = 0.0 - 6.0
dy = 3.0 - 0.0
con_atan = math.degrees(math.atan(dy / dx))
con_atan2 = math.degrees(math.atan2(dy, dx))
print(f"Con atan:  θ = {con_atan:.2f}°")
print(f"Con atan2: θ = {con_atan2:.2f}°")
# [fin: s02_ejercicio_4]

# %% [markdown]
# ## Ejercicio 2.5

# %%
# [inicio: s02_ejercicio_5]
# Barra vertical: de (2, 3) a (2, -1)
dx = 2.0 - 2.0
dy = -1.0 - 3.0
L = math.sqrt(dx**2 + dy**2)
c = dx / L
s = dy / L
theta = math.degrees(math.atan2(dy, dx))
print(f"L = {L:.3f} m")
print(f"c = {c:.4f}, s = {s:.4f}")
print(f"θ = {theta:.2f}°")
# [fin: s02_ejercicio_5]
