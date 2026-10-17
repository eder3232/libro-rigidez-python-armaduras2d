print(f"K_ll: {K_ll.shape}, rango "
      f"{np.linalg.matrix_rank(K_ll)}")
print(f"K_lr es la transpuesta de K_rl: "
      f"{np.allclose(K_lr, K_rl.T)}")
