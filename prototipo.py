import numpy as np
from PIL import Image

matrix = np.full((640,480),255,dtype=np.uint8)
def DibujarPixel(x, y, color):
    matrix[x][y] = color

def LineaBresenham(x1, y1, x2, y2):
      #0 - Distancias que se desplazan en cada eje
      dY = (y2 - y1)
      dX = (x2 - x1)
    
      #1 - Incrementos para las secciones con avance inclinado
      if (dY >= 0):
          IncYi = 1
      else:
          dY = -dY
          IncYi = -1

      if (dX >= 0):
          IncXi = 1
      else:
          dX = -dX
          IncXi = -1
    
      # 2 - Incrementos para las secciones con avance recto:
      if (dX >= dY):
          IncYr = 0
          IncXr = IncXi
      else:
          IncXr = 0
          IncYr = IncYi
    
          # Cuando dy es mayor que dx, se intercambian, para reutilizar el mismo bucle.
          # ver octantes blancos en la imagen encima del código
          k = dX 
          dX = dY 
          dY = k
    
      # 3  - Inicializar valores (y de error).
      x = x1
      y = y1
      avR = (2 * dY)
      av = (avR - dX)
      avI = (av - dX)
    
      # 4  - Bucle para el trazado de las línea.
      while x != x2 and y != y2:
          DibujarPixel(x, y, 0) # Como mínimo se dibujará siempre 1 píxel (punto).
          print(str(av) + " ") # (debug) para ver los valores de error global que van apareciendo.
          if (av >= 0):
              x = (x + IncXi)     # X aumenta en inclinado.
              y = (y + IncYi)     # Y aumenta en inclinado.
              av = (av + avI)     # Avance Inclinado
          else:
              x = (x + IncXr)     # X aumenta en recto.
              y = (y + IncYr)     # Y aumenta en recto.
              av = (av + avR)     # Avance Recto

def main():
    # Tu código principal va aquí
    LineaBresenham(200,200,640,480)
    # Nombre del archivo en el que deseas guardar la matriz
    nombre_archivo = "matriz.txt"

    # Guardar la matriz en el archivo de texto
    np.savetxt(nombre_archivo, matrix, fmt='%1.2f', delimiter='\t')

    # Crear una imagen desde la matriz
    img = Image.fromarray(matrix, 'L')

    # Guardar la imagen en un archivo PNG
    nombre_archivo = "matriz.png"
    img.save(nombre_archivo)

if __name__ == "_main_":
    main()