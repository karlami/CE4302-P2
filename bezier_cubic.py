import matplotlib.pyplot as plt
import numpy as np
import cv2

# Función para calcular un punto en la curva Bézier cúbica y guardar los valores
def bezier_cubic(p0, p1, p2, p3, x_values, y_values):
    for t in range(0, 100, 2(1/99)):
        x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
        y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]
        x1 = (1 - (t+1/99))**3 * p0[0] + 3 * (1 - (t+1/99))**2 * (t+1/99) * p1[0] + 3 * (1 - (t+1/99)) * (t+1/99)**2 * p2[0] + (t+1/99)**3 * p3[0]
        y1 = (1 - (t+1/99))**3 * p0[1] + 3 * (1 - (t+1/99))**2 * (t+1/99) * p1[1] + 3 * (1 - (t+1/99)) * (t+1/99)**2 * p2[1] + (t+1/99)**3 * p3[1]
        x_values.append(x)
        y_values.append(y)
        x_values.append(x1)
        y_values.append(y1)

# Dimensiones de la imagen
width, height = 640, 480

# Crear una imagen en blanco
image = np.zeros((height, width, 3), dtype=np.uint8)

# Puntos de control necesarios para crear la curva
p0 = (50, 400)
p1 = (200, 100)
p2 = (400, 100)
p3 = (550, 400)

# Parámetros de t (0 a 1)
t_values = np.linspace(0, 1, 100)
x_values = []
y_values = []

# Dibujar la curva Bezier en la imagen
for x, y in zip(x_values, y_values):
    image[int(y), int(x)] = (255, 255, 255)

# Mostrar la imagen con la curva Bezier
cv2.imshow('Bezier Curve', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
