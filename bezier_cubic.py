import matplotlib.pyplot as plt
import numpy as np
import cv2

# Calcular un punto en la curva Bezier cubica
def bezier_cubic(t, p0, p1, p2, p3):
    x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
    y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]
    return x, y

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

# Calcular las coordenadas (x, y) en la curva Bezier cubica
curve_points = [bezier_cubic(t, p0, p1, p2, p3) for t in t_values]

# Dibujar la curva Bezier en la imagen
for x, y in curve_points:
    image[int(y), int(x)] = (255, 255, 255)  # Pixel blanco en la ubicacion de la curva

# Mostrar la imagen con la curva Bezier
cv2.imshow('Bezier Curve', image)
cv2.waitKey(0)
cv2.destroyAllWindows()