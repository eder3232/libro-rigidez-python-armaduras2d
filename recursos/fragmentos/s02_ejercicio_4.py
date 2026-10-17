# Barra de (6, 0) a (0, 3): hacia la izquierda y arriba
dx = 0.0 - 6.0
dy = 3.0 - 0.0
con_atan = math.degrees(math.atan(dy / dx))
con_atan2 = math.degrees(math.atan2(dy, dx))
print(f"Con atan:  θ = {con_atan:.2f}°")
print(f"Con atan2: θ = {con_atan2:.2f}°")
