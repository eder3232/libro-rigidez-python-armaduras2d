"""Motor de la calculadora de armaduras planas por el método de rigidez.

Construido a lo largo del libro *Análisis matricial de armaduras con Python*.
Es el mismo código de la sección Motor de mi_calculadora.ipynb.

Uso, desde un archivo o notebook en la misma carpeta:

    from calculadora import analizar_armadura, mostrar_resultados
"""

import math


import matplotlib.pyplot as plt


def calcular_geometria(nodos, barras):
    """Longitud y cosenos directores de cada barra.

    Devuelve un diccionario {número de barra:
    {"longitud": L, "c": c, "s": s}}.
    """
    geometria = {}
    for numero, barra in barras.items():
        inicial = nodos[barra["nodo_inicial"]]
        final = nodos[barra["nodo_final"]]
        dx = final["x"] - inicial["x"]
        dy = final["y"] - inicial["y"]
        L = math.sqrt(dx**2 + dy**2)
        geometria[numero] = {"longitud": L,
                             "c": dx / L, "s": dy / L}
    return geometria


import numpy as np


np.set_printoptions(precision=1, suppress=True)


def rigidez_local(E, A, L):
    """Matriz de rigidez de la barra en sus ejes (2x2)."""
    return E * A / L * np.array([[1.0, -1.0],
                                 [-1.0, 1.0]])


def matriz_transformacion(c, s):
    """Matriz T (2 x 4) tal que u' = T u."""
    return np.array([[c, s, 0.0, 0.0],
                     [0.0, 0.0, c, s]])


def rigidez_barra(E, A, L, c, s):
    """Matriz de rigidez de la barra en ejes globales."""
    T = matriz_transformacion(c, s)
    return T.T @ rigidez_local(E, A, L) @ T


def calcular_rigideces(barras, geometria):
    """Matriz de rigidez global (4 x 4) de cada barra."""
    rigideces = {}
    for numero, barra in barras.items():
        g = geometria[numero]
        rigideces[numero] = rigidez_barra(
            barra["elasticidad"], barra["area"],
            g["longitud"], g["c"], g["s"])
    return rigideces


def gdl_del_nodo(nodo):
    """Grados de libertad (x, y) del nodo, desde 1."""
    return 2 * nodo - 1, 2 * nodo


def gdl_de_barra(barra):
    """Grados de libertad de los extremos de una barra."""
    xi, yi = gdl_del_nodo(barra["nodo_inicial"])
    xj, yj = gdl_del_nodo(barra["nodo_final"])
    return [xi, yi, xj, yj]


def clasificar_gdl(nodos, apoyos):
    """Grados de libertad libres y restringidos."""
    libres = []
    restringidos = []
    sin_apoyo = {"x": False, "y": False}
    for nodo in nodos:
        gdl_x, gdl_y = gdl_del_nodo(nodo)
        apoyo = apoyos.get(nodo, sin_apoyo)
        if apoyo["x"]:
            restringidos.append(gdl_x)
        else:
            libres.append(gdl_x)
        if apoyo["y"]:
            restringidos.append(gdl_y)
        else:
            libres.append(gdl_y)
    return libres, restringidos


def indices(gdl):
    """Traduce grados de libertad (desde 1) a índices
    de NumPy (desde 0). Es el único lugar del libro donde
    se hace esta traducción."""
    resultado = []
    for g in gdl:
        resultado.append(g - 1)
    return resultado


def indeterminacion(nodos, barras, restringidos):
    """b + r - 2n: incógnitas menos ecuaciones."""
    b, r, n = len(barras), len(restringidos), len(nodos)
    return b + r - 2 * n


def mostrar_matriz(matriz, filas, columnas=None,
                   decimales=1, ancho=7):
    """Imprime una matriz con los grados de libertad
    (desde 1) como encabezados de filas y columnas."""
    if columnas is None:
        columnas = filas
    encabezado = " gdl"
    for g in columnas:
        encabezado += f"{g:>{ancho}}"
    print(encabezado)
    for i, g in enumerate(filas):
        linea = f"{g:>4}"
        for valor in matriz[i]:
            # Sumar 0.0 evita mostrar -0.0
            valor = round(valor, decimales) + 0.0
            linea += f"{valor:>{ancho}.{decimales}f}"
        print(linea)


def ensamblar_rigidez(nodos, barras, rigideces):
    """Matriz de rigidez global de la armadura."""
    n_gdl = 2 * len(nodos)
    K = np.zeros((n_gdl, n_gdl))
    for numero, barra in barras.items():
        g = indices(gdl_de_barra(barra))
        K[np.ix_(g, g)] += rigideces[numero]
    return K


def ensamblar_cargas(nodos, cargas):
    """Vector de cargas nodales F de la armadura."""
    F = np.zeros(2 * len(nodos))
    for nodo, carga in cargas.items():
        fila_x, fila_y = indices(gdl_del_nodo(nodo))
        F[fila_x] += carga["x"]
        F[fila_y] += carga["y"]
    return F


def mostrar_vector(vector, gdl, decimales=2, ancho=10):
    """Imprime un vector con sus grados de libertad."""
    for i, g in enumerate(gdl):
        valor = round(vector[i], decimales) + 0.0
        print(f"{g:>4}{valor:>{ancho}.{decimales}f}")


def particionar(K, libres, restringidos):
    """Bloques Kll, Klr, Krl y Krr de la matriz K."""
    l = indices(libres)
    r = indices(restringidos)
    K_ll = K[np.ix_(l, l)]
    K_lr = K[np.ix_(l, r)]
    K_rl = K[np.ix_(r, l)]
    K_rr = K[np.ix_(r, r)]
    return K_ll, K_lr, K_rl, K_rr


def resolver_desplazamientos(K_ll, K_lr, F_l, U_r):
    """Desplazamientos de los gdl libres, U_l."""
    if np.linalg.matrix_rank(K_ll) < len(K_ll):
        raise ValueError("La armadura es inestable: "
                         "K_ll es singular.")
    return np.linalg.solve(K_ll, F_l - K_lr @ U_r)


def calcular_reacciones(K_rl, K_rr, U_l, U_r, F_r):
    """Reacciones en los grados de libertad restringidos.

    F_r son las cargas aplicadas directamente sobre los
    apoyos (normalmente ceros)."""
    return K_rl @ U_l + K_rr @ U_r - F_r


def comprobar_equilibrio(nodos, F, R, restringidos):
    """Resultantes de cargas más reacciones: Fx, Fy y el
    momento respecto del origen. Deben ser nulas."""
    total = F.copy()
    total[indices(restringidos)] += R
    momento = 0.0
    for nodo in nodos:
        ix, iy = indices(gdl_del_nodo(nodo))
        x, y = nodos[nodo]["x"], nodos[nodo]["y"]
        momento += x * total[iy] - y * total[ix]
    return total[0::2].sum(), total[1::2].sum(), momento


def fuerzas_axiales(barras, geometria, U):
    """Fuerza axial de cada barra (+ en tracción)."""
    N = {}
    for numero, barra in barras.items():
        g = geometria[numero]
        u = U[indices(gdl_de_barra(barra))]
        T = matriz_transformacion(g["c"], g["s"])
        u_local = T @ u
        k_local = rigidez_local(barra["elasticidad"],
                                barra["area"],
                                g["longitud"])
        N[numero] = (k_local @ u_local)[1]
    return N


def clasificar_fuerza(N, tolerancia=1e-6):
    """Tracción, compresión o sin fuerza."""
    if N > tolerancia:
        return "tracción"
    elif N < -tolerancia:
        return "compresión"
    else:
        return "sin fuerza"


def mostrar_tabla(encabezados, filas, decimales=2,
                  ancho=11):
    """Imprime una tabla con columnas alineadas. Los
    números se muestran con los decimales indicados."""
    linea = ""
    for encabezado in encabezados:
        linea += f"{encabezado:>{ancho}}"
    print(linea)
    for fila in filas:
        linea = ""
        for valor in fila:
            if isinstance(valor, str):
                linea += f"{valor:>{ancho}}"
            else:
                valor = round(valor, decimales) + 0.0
                linea += f"{valor:>{ancho}.{decimales}f}"
        print(linea)


def equilibrio_nodal(nodos, barras, geometria, N, F, R,
                     restringidos):
    """Mayor desequilibrio en los nodos, con las fuerzas
    de las barras, las cargas y las reacciones."""
    residuo = F.copy()
    residuo[indices(restringidos)] += R
    for numero, barra in barras.items():
        g = geometria[numero]
        c, s = g["c"], g["s"]
        ix, iy, jx, jy = indices(gdl_de_barra(barra))
        # En tracción, la barra tira de cada nodo hacia
        # el otro extremo
        residuo[[ix, iy]] += N[numero] * np.array([c, s])
        residuo[[jx, jy]] -= N[numero] * np.array([c, s])
    return np.abs(residuo).max()


TRACCION = "#0072B2"


COMPRESION = "#D55E00"


PRINCIPAL = "#1F4E79"


NEUTRO = "#8C8C8C"


def dibujar_armadura(ax, nodos, barras, color=NEUTRO,
                     estilo="-", etiqueta=None):
    """Dibuja las barras de una armadura en ax."""
    for barra in barras.values():
        i = nodos[barra["nodo_inicial"]]
        j = nodos[barra["nodo_final"]]
        ax.plot([i["x"], j["x"]], [i["y"], j["y"]],
                color=color, linestyle=estilo, marker="o",
                markersize=4, label=etiqueta)
        etiqueta = None  # la leyenda, una sola vez
    ax.set_aspect("equal")


def nodos_desplazados(nodos, U, escala):
    """Nodos en su posición deformada, con los
    desplazamientos multiplicados por la escala."""
    nuevos = {}
    for nodo, punto in nodos.items():
        ix, iy = indices(gdl_del_nodo(nodo))
        nuevos[nodo] = {"x": punto["x"] + escala * U[ix],
                        "y": punto["y"] + escala * U[iy]}
    return nuevos


def escala_automatica(nodos, U, fraccion=0.1):
    """Escala para que el mayor desplazamiento dibujado
    sea una fracción del tamaño de la armadura."""
    xs = []
    ys = []
    for punto in nodos.values():
        xs.append(punto["x"])
        ys.append(punto["y"])
    tamano = max(max(xs) - min(xs), max(ys) - min(ys))
    return fraccion * tamano / np.abs(U).max()


def dibujar_fuerzas(ax, nodos, barras, N, decimales=1,
                    tamano=None):
    """Barras en colores según su fuerza axial, con su
    valor en kN al 40 % de cada barra. tamano: tamaño
    de letra de los valores."""
    for numero, barra in barras.items():
        estado = clasificar_fuerza(N[numero])
        if estado == "tracción":
            color = TRACCION
        elif estado == "compresión":
            color = COMPRESION
        else:
            color = NEUTRO
        i = nodos[barra["nodo_inicial"]]
        j = nodos[barra["nodo_final"]]
        ax.plot([i["x"], j["x"]], [i["y"], j["y"]],
                color=color, linewidth=3)
        # Al 40 % y no en el punto medio: así no se tapan
        # los valores de dos diagonales que se cruzan
        xm = i["x"] + 0.4 * (j["x"] - i["x"])
        ym = i["y"] + 0.4 * (j["y"] - i["y"])
        valor = round(N[numero], decimales) + 0.0
        fondo = {"facecolor": "white", "linewidth": 0}
        ax.text(xm, ym, f"{valor:.{decimales}f}",
                color=color, ha="center", va="center",
                bbox=fondo, fontsize=tamano)
    # Leyenda con líneas vacías: solo muestran los colores
    ax.plot([], [], color=TRACCION, linewidth=3,
            label="Tracción")
    ax.plot([], [], color=COMPRESION, linewidth=3,
            label="Compresión")
    # Leyenda debajo del dibujo, para no tapar las barras
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 0),
              ncol=2, frameon=False)
    ax.set_aspect("equal")
    ax.axis("off")


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
