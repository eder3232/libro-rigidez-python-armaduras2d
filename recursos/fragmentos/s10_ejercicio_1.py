sigma_maxima = 0.0
for numero, fuerza in N.items():
    sigma = abs(fuerza) / barras[numero]["area"] / 1000
    sigma_maxima = max(sigma_maxima, sigma)
print(f"Mayor esfuerzo: {sigma_maxima:.2f} MPa")
fraccion = sigma_maxima / 250  # fy = 250 MPa
print(f"Fracción de la fluencia: {fraccion:.1%}")
