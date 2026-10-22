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
