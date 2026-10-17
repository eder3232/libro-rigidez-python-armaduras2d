# Barra 3 del ejemplo A: c = 0.6, s = 0.8
T = np.array([[0.6, 0.8, 0.0, 0.0],
              [0.0, 0.0, 0.6, 0.8]])
# El nodo final se mueve 3 mm en x y 4 mm en y
u = np.array([0.0, 0.0, 3.0, 4.0])
print(T.shape, u.shape, T.T.shape)
T @ u
