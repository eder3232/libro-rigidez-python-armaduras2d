# %% [markdown]
# # Anexo D. Validación con software comercial
#
# Registra los resultados de la calculadora para los ejemplos B y C, que el
# anexo D compara con los de un programa comercial. Se ejecuta después de
# todos los capítulos, con la calculadora completa.


# %% tags=["libro"]
def registrar_resultados(prefijo, nodos, resultados):
    """Registra desplazamientos (mm), reacciones y fuerzas (kN)."""
    U = resultados["U"]
    for nodo in nodos:
        ix, iy = indices(gdl_del_nodo(nodo))
        valor_libro(f"{prefijo}_ux_{nodo}", U[ix] * 1000, 3)
        valor_libro(f"{prefijo}_uy_{nodo}", U[iy] * 1000, 3)
    for posicion, g in enumerate(resultados["restringidos"]):
        valor_libro(f"{prefijo}_r_{g}", resultados["R"][posicion], 2)
    for numero, fuerza in resultados["N"].items():
        valor_libro(f"{prefijo}_n_{numero}", fuerza, 2)


registrar_resultados(
    "d_b", nodos_b,
    analizar_armadura(nodos_b, barras_b, apoyos_b, cargas_b))
registrar_resultados(
    "d_c", nodos_c,
    analizar_armadura(nodos_c, barras_c, apoyos_c, cargas_c))
