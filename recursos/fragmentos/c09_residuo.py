residuo = K_ll @ U_l - lado_derecho
print(f"Mayor residuo: {np.abs(residuo).max():.1e} kN")
print(np.allclose(K_ll @ U_l, lado_derecho))
