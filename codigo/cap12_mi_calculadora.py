# %% [markdown]
# # Capítulo 12. Mi calculadora de armaduras
#
# Este notebook acompaña al capítulo 12 del libro *Análisis matricial de
# armaduras con Python*. Reunimos todas las funciones en una calculadora
# completa y la aplicamos a una armadura de puente.

# %% [markdown]
# ## 12.2 Una función que lo hace todo

# %% tags=["acumulable"]
# [inicio: c12_analizar]
def analizar_armadura(nodos, barras, apoyos, cargas):
    """Análisis completo de una armadura plana.

    Devuelve un diccionario con los resultados."""
    geometria = calcular_geometria(nodos, barras)
    rigideces = calcular_rigideces(barras, geometria)
    K = ensamblar_rigidez(nodos, barras, rigideces)
    F = ensamblar_cargas(nodos, cargas)
    libres, restringidos = clasificar_gdl(nodos, apoyos)
    K_ll, K_lr, K_rl, K_rr = particionar(K, libres,
                                         restringidos)
    U_r = np.zeros(len(restringidos))
    U_l = resolver_desplazamientos(
        K_ll, K_lr, F[indices(libres)], U_r)
    U = np.zeros(2 * len(nodos))
    U[indices(libres)] = U_l
    U[indices(restringidos)] = U_r
    R = calcular_reacciones(K_rl, K_rr, U_l, U_r,
                            F[indices(restringidos)])
    N = fuerzas_axiales(barras, geometria, U)
    return {"geometria": geometria, "K": K, "F": F,
            "U": U, "R": R, "N": N, "libres": libres,
            "restringidos": restringidos}
# [fin: c12_analizar]

# %% tags=["exploracion"]
# [inicio: c12_usar_analizar]
resultados = analizar_armadura(nodos, barras, apoyos,
                               cargas)
print(list(resultados.keys()))
for numero, fuerza in resultados["N"].items():
    print(f"Barra {numero}: N = {fuerza:.2f} kN")
# [fin: c12_usar_analizar]

# %% [markdown]
# ## 12.3 El informe de resultados

# %% tags=["acumulable"]
# [inicio: c12_mostrar_resultados]
def mostrar_resultados(nodos, barras, resultados):
    """Tablas de desplazamientos, reacciones y fuerzas."""
    U = resultados["U"]
    R = resultados["R"]
    N = resultados["N"]
    print("Desplazamientos de los nodos (mm)")
    filas = []
    for nodo in nodos:
        ix, iy = indices(gdl_del_nodo(nodo))
        filas.append([str(nodo), U[ix] * 1000,
                      U[iy] * 1000])
    mostrar_tabla(["Nodo", "ux", "uy"], filas,
                  decimales=3)

    print("\nReacciones (kN)")
    filas = []
    restringidos = resultados["restringidos"]
    for posicion, g in enumerate(restringidos):
        nodo = (g + 1) // 2
        if g % 2 == 1:
            direccion = "x"
        else:
            direccion = "y"
        filas.append([str(nodo), direccion, R[posicion]])
    mostrar_tabla(["Nodo", "Dirección", "R"], filas)

    print("\nFuerzas axiales")
    filas = []
    for numero, fuerza in N.items():
        sigma = fuerza / barras[numero]["area"] / 1000
        filas.append([str(numero), fuerza, sigma,
                      clasificar_fuerza(fuerza)])
    encabezados = ["Barra", "N (kN)", "σ (MPa)", "Estado"]
    mostrar_tabla(encabezados, filas)
# [fin: c12_mostrar_resultados]

# %% tags=["exploracion"]
# [inicio: c12_informe_a]
mostrar_resultados(nodos, barras, resultados)
# [fin: c12_informe_a]

# %% tags=["acumulable"]
# [inicio: c12_verificar]
def verificar_resultados(nodos, barras, resultados,
                         tolerancia=1e-6):
    """Equilibrio global y de cada nodo. Devuelve True
    si ambos se cumplen dentro de la tolerancia."""
    F, R = resultados["F"], resultados["R"]
    restringidos = resultados["restringidos"]
    suma_x, suma_y, momento = comprobar_equilibrio(
        nodos, F, R, restringidos)
    global_ok = max(abs(suma_x), abs(suma_y),
                    abs(momento)) < tolerancia
    nodal_ok = equilibrio_nodal(
        nodos, barras, resultados["geometria"],
        resultados["N"], F, R, restringidos) < tolerancia
    for nombre, correcto in (("global", global_ok),
                             ("nodal", nodal_ok)):
        if correcto:
            print(f"Equilibrio {nombre}: correcto")
        else:
            print(f"Equilibrio {nombre}: ERROR")
    return global_ok and nodal_ok
# [fin: c12_verificar]

# %% tags=["acumulable"]
# [inicio: c12_graficar]
def graficar_resultados(nodos, barras, resultados,
                        titulo="", decimales=1,
                        tamano=None):
    """Deformada y diagrama de fuerzas, en dos paneles:
    uno sobre otro si la armadura es muy alargada."""
    U, N = resultados["U"], resultados["N"]
    xs = []
    ys = []
    for punto in nodos.values():
        xs.append(punto["x"])
        ys.append(punto["y"])
    ancho = max(xs) - min(xs)
    alto = max(ys) - min(ys)
    if ancho > 2 * alto:
        fig, (ax1, ax2) = plt.subplots(2, 1,
                                       figsize=(4.5, 3.6))
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2,
                                       figsize=(4.5, 2.4))
    escala = escala_automatica(nodos, U)
    dibujar_armadura(ax1, nodos, barras, estilo="--")
    deformados = nodos_desplazados(nodos, U, escala)
    dibujar_armadura(ax1, deformados, barras,
                     color=PRINCIPAL)
    ax1.set_title(f"Deformada (×{escala:.0f})")
    ax1.axis("off")
    dibujar_fuerzas(ax2, nodos, barras, N, decimales,
                    tamano)
    ax2.set_title("Fuerzas axiales (kN)")
    fig.suptitle(titulo)
    fig.tight_layout()
    plt.show()
# [fin: c12_graficar]

# %% tags=["exploracion"]
# [inicio: c12_ejemplo_b]
resultados_b = analizar_armadura(nodos_b, barras_b,
                                 apoyos_b, cargas_b)
verificar_resultados(nodos_b, barras_b, resultados_b)
graficar_resultados(nodos_b, barras_b, resultados_b,
                    "Ejemplo B")
# [fin: c12_ejemplo_b]

# %% [markdown]
# ## 12.4 Mi calculadora: el ejemplo C
#
# Las celdas siguientes forman la sección **Datos** y la sección
# **Resultados** del notebook «Mi calculadora de armaduras». Para
# analizar otra armadura basta con cambiar los datos.

# %% tags=["calculadora"]
# [inicio: c12_datos_c]
# Ejemplo C: puente peatonal tipo Pratt, 6 paneles de
# 3 m (luz de 18 m) y 3 m de altura. Unidades: kN y m

# Nodos: cordón inferior (1 a 7) y superior (8 a 12)
nodos_c = {}
for k in range(7):
    nodos_c[k + 1] = {"x": 3.0 * k, "y": 0.0}
for k in range(5):
    nodos_c[k + 8] = {"x": 3.0 * (k + 1), "y": 3.0}


def barra(i, j, area, elasticidad=2.0e8):
    """Datos de una barra del nodo i al nodo j."""
    return {"nodo_inicial": i, "nodo_final": j,
            "elasticidad": elasticidad, "area": area}


A_CORDON = 0.0030  # m², cordones y diagonales extremas
A_ALMA = 0.0015    # m², montantes y diagonales

barras_c = {
    # Cordón inferior
    1: barra(1, 2, A_CORDON), 2: barra(2, 3, A_CORDON),
    3: barra(3, 4, A_CORDON), 4: barra(4, 5, A_CORDON),
    5: barra(5, 6, A_CORDON), 6: barra(6, 7, A_CORDON),
    # Cordón superior
    7: barra(8, 9, A_CORDON), 8: barra(9, 10, A_CORDON),
    9: barra(10, 11, A_CORDON),
    10: barra(11, 12, A_CORDON),
    # Diagonales extremas
    11: barra(1, 8, A_CORDON), 12: barra(12, 7, A_CORDON),
    # Montantes
    13: barra(2, 8, A_ALMA), 14: barra(3, 9, A_ALMA),
    15: barra(4, 10, A_ALMA), 16: barra(5, 11, A_ALMA),
    17: barra(6, 12, A_ALMA),
    # Diagonales, descendiendo hacia el centro
    18: barra(8, 3, A_ALMA), 19: barra(9, 4, A_ALMA),
    20: barra(11, 4, A_ALMA), 21: barra(12, 5, A_ALMA),
}

apoyos_c = {
    1: {"x": True, "y": True},   # articulado
    7: {"x": False, "y": True},  # rodillo
}

# 25 kN en cada nodo interior del cordón inferior
cargas_c = {}
for nodo in range(2, 7):
    cargas_c[nodo] = {"x": 0.0, "y": -25.0}
# [fin: c12_datos_c]

# %% tags=["calculadora"]
# [inicio: c12_analisis_c]
resultados_c = analizar_armadura(nodos_c, barras_c,
                                 apoyos_c, cargas_c)
verificar_resultados(nodos_c, barras_c, resultados_c)
graficar_resultados(nodos_c, barras_c, resultados_c,
                    "Ejemplo C: puente Pratt",
                    decimales=0, tamano=7)
# [fin: c12_analisis_c]

# %% tags=["calculadora"]
# [inicio: c12_tablas_c]
mostrar_resultados(nodos_c, barras_c, resultados_c)
# [fin: c12_tablas_c]

# %% [markdown]
# ## Problema resuelto 12.1: el método de las secciones

# %% tags=["exploracion"]
# [inicio: c12_problema_resuelto]
# Corte por el tercer panel (x entre 6 y 9 m)
R1 = 5 * 25.0 / 2  # reacción en cada apoyo, por simetría
h = 3.0
# Momentos respecto del nodo 9 (x = 6): cordón inferior
N_inferior = (R1 * 6 - 25.0 * 3) / h
# Momentos respecto del nodo 4 (x = 9): cordón superior
N_superior = -(R1 * 9 - 25.0 * 6 - 25.0 * 3) / h

N_c = resultados_c["N"]
print(f"Barra 3: secciones {N_inferior:8.2f} kN, "
      f"calculadora {N_c[3]:8.2f} kN")
print(f"Barra 8: secciones {N_superior:8.2f} kN, "
      f"calculadora {N_c[8]:8.2f} kN")
# [fin: c12_problema_resuelto]

# %% tags=["libro"]
U_c = resultados_c["U"]
valor_libro("c12_uy_centro", -U_c[indices([8])][0] * 1000, 2)
valor_libro("c12_reaccion", resultados_c["R"][1], 1)
valor_libro("c12_n_barra_3", resultados_c["N"][3], 1)
valor_libro("c12_n_barra_8", resultados_c["N"][8], 1)

# %% [markdown]
# ## Ejercicios
#
# Resuelva cada ejercicio en su notebook y después ejecute la celda de
# verificación correspondiente.

# %% tags=["exploracion"]
# Ejercicio 12.1: flecha (desplazamiento vertical) del nodo 4 del ejemplo C, en mm
respuesta = None  # reemplace None por su resultado (positivo, en mm)

flecha = -resultados_c["U"][indices([8])][0] * 1000
if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif abs(respuesta - flecha) < 1e-2:
    print("Correcto.")
else:
    print("Todavía no. El nodo 4 tiene los gdl 7 y 8; la flecha es -uy.")
