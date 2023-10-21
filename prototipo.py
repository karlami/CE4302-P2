import numpy as np
from PIL import Image

matrix = np.full((480,640),255,dtype=np.uint8)
def DibujarPixel(x, y, color):
    matrix[x][y] = color

def LineaBresenham(y1, x1, y2, x2):
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
      while x != x2 or y != y2:
          DibujarPixel(x, y, 4) # Como mínimo se dibujará siempre 1 píxel (punto).
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
    LineaBresenham(320, 50, 380, 245)
    LineaBresenham(380, 245, 590, 250)
    LineaBresenham(590, 250, 400, 350)
    LineaBresenham(400, 350, 500, 420)
    LineaBresenham(500, 420, 320, 340)
    LineaBresenham(320, 340, 140, 420)
    LineaBresenham(140, 420, 260, 350)
    LineaBresenham(260, 350, 50, 250)
    LineaBresenham(50, 250, 280, 245)
    LineaBresenham(280, 245, 320, 50)
    # Nombre del archivo en el que deseas guardar la matriz
    nombre_archivo = "matriz.txt"

    # Guardar la matriz en el archivo de texto
    np.savetxt(nombre_archivo, matrix, fmt='%1.2f', delimiter='\t')

    # Crear una imagen desde la matriz
    img = Image.fromarray(matrix, 'L')

    # Guardar la imagen en un archivo PNG
    nombre_archivo = "matriz.png"
    img.save(nombre_archivo)
    img.show()

if __name__ == "__main__":
    main()