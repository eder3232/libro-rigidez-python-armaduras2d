# %% [markdown]
# # Anexo D. Validación con OpenSees
#
# Analizamos los ejemplos B y C con OpenSees, un programa de análisis
# estructural de código abierto, y comparamos sus resultados con los de
# nuestra calculadora.

# %% tags=["validacion"]
# [inicio: d_opensees]
import openseespy.opensees as ops


def analizar_con_opensees(nodos, barras, apoyos, cargas):
    """Analiza la armadura con OpenSees. Recibe los mismos
    datos que analizar_armadura y devuelve U, R y N en
    el mismo formato, para compararlos."""
    ops.wipe()  # borra el modelo anterior
    ops.model("basic", "-ndm", 2, "-ndf", 2)
    for nodo, punto in nodos.items():
        ops.node(nodo, punto["x"], punto["y"])
    for nodo, apoyo in apoyos.items():
        ops.fix(nodo, int(apoyo["x"]), int(apoyo["y"]))
    for numero, barra in barras.items():
        # Un material elástico por barra, con su E
        ops.uniaxialMaterial("Elastic", numero,
                             barra["elasticidad"])
        ops.element("Truss", numero,
                    barra["nodo_inicial"],
                    barra["nodo_final"], barra["area"],
                    numero)
    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)
    for nodo, carga in cargas.items():
        ops.load(nodo, carga["x"], carga["y"])

    # Análisis estático y lineal, en un solo paso
    ops.system("BandSPD")
    ops.numberer("RCM")
    ops.constraints("Plain")
    ops.integrator("LoadControl", 1.0)
    ops.algorithm("Linear")
    ops.analysis("Static")
    ops.analyze(1)
    ops.reactions()

    # Los resultados, ordenados como los de la calculadora
    U = np.zeros(2 * len(nodos))
    for nodo in nodos:
        ix, iy = indices(gdl_del_nodo(nodo))
        U[ix], U[iy] = ops.nodeDisp(nodo)
    _, restringidos = clasificar_gdl(nodos, apoyos)
    R = []
    for g in restringidos:
        nodo = (g + 1) // 2
        direccion = 1 if g % 2 == 1 else 2  # x o y
        R.append(ops.nodeReaction(nodo, direccion))
    N = {}
    for numero in barras:
        fuerza = ops.eleResponse(numero, "axialForce")
        N[numero] = fuerza[0]
    return {"U": U, "R": np.array(R), "N": N,
            "restringidos": restringidos}
# [fin: d_opensees]

# %% tags=["validacion"]
# [inicio: d_comparar]
def comparar_resultados(nodos, calculadora, opensees,
                        tolerancia=1e-9):
    """Muestra los dos análisis lado a lado e indica si
    coinciden."""
    filas = []
    for nodo in nodos:
        for direccion, g in zip("xy", gdl_del_nodo(nodo)):
            i = indices([g])[0]
            filas.append([f"u{direccion} {nodo} (mm)",
                          calculadora["U"][i] * 1000,
                          opensees["U"][i] * 1000])
    restringidos = calculadora["restringidos"]
    for posicion, g in enumerate(restringidos):
        filas.append([f"R{g} (kN)",
                      calculadora["R"][posicion],
                      opensees["R"][posicion]])
    for numero in calculadora["N"]:
        filas.append([f"N{numero} (kN)",
                      calculadora["N"][numero],
                      opensees["N"][numero]])
    mostrar_tabla(["Resultado", "Calculadora",
                   "OpenSees"], filas, decimales=3,
                  ancho=13)
    diferencia = 0.0
    for _, valor_calculadora, valor_opensees in filas:
        diferencia = max(diferencia, abs(
            valor_calculadora - valor_opensees))
    if diferencia < tolerancia:
        print("\nLos dos análisis coinciden.")
    else:
        print(f"\nDifieren hasta en {diferencia:.3g}.")
# [fin: d_comparar]

# %% tags=["validacion"]
# [inicio: d_comparar_b]
resultados_b = analizar_armadura(nodos_b, barras_b,
                                 apoyos_b, cargas_b)
opensees_b = analizar_con_opensees(nodos_b, barras_b,
                                   apoyos_b, cargas_b)
comparar_resultados(nodos_b, resultados_b, opensees_b)
# [fin: d_comparar_b]

# %% tags=["validacion"]
resultados_c = analizar_armadura(nodos_c, barras_c,
                                 apoyos_c, cargas_c)
opensees_c = analizar_con_opensees(nodos_c, barras_c,
                                   apoyos_c, cargas_c)
comparar_resultados(nodos_c, resultados_c, opensees_c)


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


# Calculadora como d_*, OpenSees como ops_d_* (\valoropensees en el anexo D)
registrar_resultados("d_b", nodos_b, resultados_b)
registrar_resultados("d_c", nodos_c, resultados_c)
registrar_resultados("ops_d_b", nodos_b, opensees_b)
registrar_resultados("ops_d_c", nodos_c, opensees_c)

# %% tags=["libro"]
import graficos_libro as gl

# %% tags=["libro"]
# [inicio: d_b_deformada]
gl.figura_deformada(nodos_b, barras_b, apoyos_b, cargas_b,
                    resultados_b, opensees_b,
                    alto_maximo=2.6)
# [fin: d_b_deformada]

# %% tags=["libro"]
# [inicio: d_b_axiales]
gl.figura_axiales(nodos_b, barras_b, apoyos_b, cargas_b,
                  opensees_b, posicion=0.3,
                  alto_maximo=2.6)
# [fin: d_b_axiales]

# %% tags=["libro"]
# [inicio: d_c_deformada]
gl.figura_deformada(nodos_c, barras_c, apoyos_c, cargas_c,
                    resultados_c, opensees_c,
                    fraccion=0.25, numeros=False,
                    cargas_colgadas=True, tamano=7.5,
                    margenes=(30, 30, 50, 16))
# [fin: d_c_deformada]

# %% tags=["libro"]
# [inicio: d_c_axiales]
gl.figura_axiales(nodos_c, barras_c, apoyos_c, cargas_c,
                  opensees_c, posicion=0.5, decimales=1,
                  cargas_colgadas=True, tamano=7,
                  grosor_maximo=5.5)
# [fin: d_c_axiales]

# %% tags=["libro"]
ejemplos = [("Ejemplo B", resultados_b, opensees_b),
            ("Ejemplo C", resultados_c, opensees_c)]

# %% tags=["libro"]
# [inicio: d_diferencias]
gl.figura_diferencias(ejemplos)
# [fin: d_diferencias]

# %% tags=["libro"]
# [inicio: d_paridad]
gl.figura_paridad(ejemplos)
# [fin: d_paridad]
