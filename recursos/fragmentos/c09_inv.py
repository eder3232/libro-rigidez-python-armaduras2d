U_l_con_inv = np.linalg.inv(K_ll) @ lado_derecho
np.allclose(U_l_con_inv, U_l)
