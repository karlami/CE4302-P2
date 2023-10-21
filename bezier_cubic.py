import matplotlib.pyplot as plt
import numpy as np

def bezier_cubic(t, p0, p1, p2, p3):
    # Fórmula de la curva Bézier cúbica
    return (1 - t)**3 * p0 + 3 * (1 - t)**2 * t * p1 + 3 * (1 - t) * t**2 * p2 + t**3 * p3

# Puntos de control
p0 = (0, 0)
p1 = (1, 2)
p2 = (3, 2)
p3 = (4, 0)

# Parámetros de t (0 a 1)
t_values = np.linspace(0, 1, 100)
x_values = []
y_values = []

# Calcular las coordenadas (x, y) en la curva Bézier cúbica
for t in t_values:
    x, y = bezier_cubic(t, p0, p1, p2, p3)
    x_values.append(x)
    y_values.append(y)

# Dibujar la curva Bézier
plt.plot(x_values, y_values, label='Curva Bézier Cúbica')
plt.scatter([p0[0], p1[0], p2[0], p3[0]], [p0[1], p1[1], p2[1], p3[1],], c='red', label='Puntos de control')
plt.legend()
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.title('Curva Bézier Cúbica')
plt.grid(True)
plt.show()