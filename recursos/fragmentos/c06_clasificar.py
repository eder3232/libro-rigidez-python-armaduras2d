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
