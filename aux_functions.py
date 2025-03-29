import random
import numpy as np

# Genero una lista con N cantidad de vértices a los que se le asigna un color al azar
def randomize_color(N):
    # Elijo los colores RGB al azar
    R = random.random()  
    G = random.random()  
    B = random.random()  

    # Genero la lista llena de ceros
    colors = np.zeros(N*3, dtype=float)

    # Relleno cada vértice de la lista con el color RGB
    for i in range(0, N*3-2, 3):
        colors[i] = R
        colors[i+1] = G
        colors[i+2] = B
    return colors

