# Traslación de la barra 2 como cuerpo rígido: 1 mm en x
traslacion = np.array([0.001, 0.0, 0.001, 0.0])
rigideces[2] @ traslacion
