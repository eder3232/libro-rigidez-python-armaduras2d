# Barra vertical: de (2, 3) a (2, -1)
dx = 2.0 - 2.0
dy = -1.0 - 3.0
L = math.sqrt(dx**2 + dy**2)
c = dx / L
s = dy / L
theta = math.degrees(math.atan2(dy, dx))
print(f"L = {L:.3f} m")
print(f"c = {c:.4f}, s = {s:.4f}")
print(f"θ = {theta:.2f}°")
