# Barra 2 del ejemplo A: del nodo 2 al nodo 3
x_i, y_i = 6.0, 0.0
x_j, y_j = 3.0, 4.0

dx = x_j - x_i
dy = y_j - y_i
L = math.sqrt(dx**2 + dy**2)
c = dx / L
s = dy / L
theta = math.degrees(math.atan2(dy, dx))

print(f"L = {L:.3f} m")
print(f"c = {c:.4f}, s = {s:.4f}")
print(f"θ = {theta:.2f}°")
