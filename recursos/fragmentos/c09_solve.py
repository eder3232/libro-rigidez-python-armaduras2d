# Apoyos sin asentamientos: U_r es nulo
U_r = np.zeros(len(restringidos))
lado_derecho = F_l - K_lr @ U_r
U_l = np.linalg.solve(K_ll, lado_derecho)
U_l * 1000  # en mm
