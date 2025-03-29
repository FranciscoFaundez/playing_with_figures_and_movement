import numpy as np
from aux_functions import randomize_color

# Posición de los 4 vértices de un cuadrado
LARGO = 0.15
positions = np.array([
    -LARGO, LARGO, 0.0,
    -LARGO, -LARGO, 0.0,
    LARGO, -LARGO, 0.0,
    LARGO, LARGO, 0.0
], dtype=np.float32)

# Índices de los 2 triángulos que forman el cuadrado
indices = np.array([
    0, 1, 2,
    2, 3, 0
], dtype=np.uint32)

# Movimiento del cuadrado
def move_sq(arr, velx_sq, vely_sq):
    # Recorro la lista con las posiciones de los vértices y los muevo 
    for i in range(0, len(arr)-2, 3):
        arr[i] += velx_sq
        arr[i+1] += vely_sq

    # Obtener límites del cuadrado.
    # Si uno de estos vértices sale de la pantalla, quiere decir que el cuadrado
    # salió de la pantalla
    x_min = min(arr[0::3])  # Coordenada X más baja
    x_max = max(arr[0::3])  # Coordenada X más alta
    y_min = min(arr[1::3])  # Coordenada Y más baja
    y_max = max(arr[1::3])  # Coordenada Y más alta

    # Aparecer por el lado contrario significa moverse el largo de la pantalla
    # menos el largo del cuadrado
    move = 2.0 + LARGO*2

    # Teletransportación diagonal (si sale por una esquina)
    if x_min > 1.0 and y_min > 1.0:  # Sale arriba a la derecha
        for i in range(0, len(arr), 3):
            arr[i] -= move  # Mueve a la izquierda
            arr[i + 1] -= move # Mueve abajo
    elif x_max < -1.0 and y_max < -1.0:  # Sale abajo a la izquierda
        for i in range(0, len(arr), 3):
            arr[i] += move # Mueve a la derecha
            arr[i + 1] += move # Mueve arriba
    elif x_min > 1.0 and y_max < -1.0:  # Sale abajo a la derecha
        for i in range(0, len(positions), 3):
            arr[i] -= move # Mueve a la izquierda
            arr[i + 1] += move  # Mueve arriba
    elif x_max < -1.0 and y_min > 1.0:  # Sale arriba a la izquierda
        for i in range(0, len(positions), 3):
            arr[i] += move # Mueve a la derecha
            arr[i + 1] -= move # Mueve abajo

    # Teletransportación si sale solo por un lado
    elif x_min > 1.0:  # Sale por la derecha
        for i in range(0, len(positions), 3):
            arr[i] -= move  # Mueve a la izquierda
    elif x_max < -1.0:  # Sale por la izquierda
        for i in range(0, len(positions), 3):
            arr[i] += move # Mueve a la derecha
    elif y_min > 1.0:  # Sale por arriba
        for i in range(0, len(positions), 3):
            arr[i + 1] -= move  # Mueve abajo
    elif y_max < -1.0:  # Sale por abajo
        for i in range(0, len(positions), 3):
            arr[i + 1] += move # Mueve arriba
    
    return arr, velx_sq, vely_sq
    