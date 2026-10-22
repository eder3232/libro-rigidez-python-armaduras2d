resultados_b = analizar_armadura(nodos_b, barras_b,
                                 apoyos_b, cargas_b)
opensees_b = analizar_con_opensees(nodos_b, barras_b,
                                   apoyos_b, cargas_b)
comparar_resultados(nodos_b, resultados_b, opensees_b)
