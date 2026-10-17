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
