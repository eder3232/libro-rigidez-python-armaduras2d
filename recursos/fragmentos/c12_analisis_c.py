resultados_c = analizar_armadura(nodos_c, barras_c,
                                 apoyos_c, cargas_c)
verificar_resultados(nodos_c, barras_c, resultados_c)
graficar_resultados(nodos_c, barras_c, resultados_c,
                    "Ejemplo C: puente Pratt",
                    decimales=0, tamano=7)
