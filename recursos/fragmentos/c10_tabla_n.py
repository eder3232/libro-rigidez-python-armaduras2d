filas = []
for numero, fuerza in N.items():
    sigma = fuerza / barras[numero]["area"] / 1000  # MPa
    filas.append([str(numero), fuerza, sigma,
                  clasificar_fuerza(fuerza)])
mostrar_tabla(["Barra", "N (kN)", "σ (MPa)", "Estado"],
              filas)
