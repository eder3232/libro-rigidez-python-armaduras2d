g = geometria[3]
c, s = g["c"], g["s"]
# El nodo final se mueve 1 mm perpendicular a la barra
perpendicular = 0.001 * np.array([0.0, 0.0, -s, c])
rigideces[3] @ perpendicular
