import numpy as np

#Crea un círclo.
# Recibe el vértice, radio y la cantidad de triángulos que usará para armarlo
def create_circle(x, y, radius, N):
    # Discretizamos un circulo en N pasos
    # Cada punto tiene 3 coordenadas y 3 componentes de color
    # Consideramos tambien el centro del circulo
    positions = np.zeros((N + 1)*3, dtype=np.float32) 
    colors = np.zeros((N + 1) * 3, dtype=np.float32)
    dtheta = 2*np.pi / N

    for i in range(N):
        theta = i*dtheta
        positions[i*3:(i+1)*3] = [x + np.cos(theta)*radius, y + np.sin(theta)*radius, 0.0]

    # Finalmente agregamos el centro
    positions[3*N:] = [x, y, 0.0]

    return positions

# Crea los índices que usará
def create_circle_indices(N):
    # Ahora calculamos los indices
    indices = np.zeros(3*( N + 1 ), dtype=np.int32)
    for i in range(N):
        # Cada triangulo se forma por el centro, el punto actual y el siguiente
        indices[3*i: 3*(i+1)] = [N, i, i+1]
   
    # Completamos el circulo (pueden borrar esta linea y ver que pasa)
    indices[3*N:] = [N, N - 1, 0]
    return indices


# Traslado una figura en (vel_x, vel_y) y hago que rebote en la ventana
def move_circ(dt, arr, vel_x, vel_y):

    # Si el color cambia, cambio la siguiente variable a True
    change_color = False

    # Obtener la posición del centro del círculo
    center_x = arr[-3]  # Último vértice es el centro en X
    center_y = arr[-2]  # Último vértice es el centro en Y

    # Calculo el radio del círculo
    radius = np.sqrt((arr[0] - center_x)**2 + (arr[1] - center_y)**2)

    # Detectar colisión con los bordes de la ventana (-1 a 1 en OpenGL normalizado)
    if center_x + radius >= 1.0 or center_x - radius <= -1.0:
        vel_x *= -1  # Invertir dirección en X
        change_color = True

    if center_y + radius >= 1.0 or center_y - radius <= -1.0:
        vel_y *= -1  # Invertir dirección en Y
        change_color = True
    
    # Recorro la lista con las posiciones de los vértices y los muevo 
    for i in range(0, len(arr)-2, 3):
        arr[i] += vel_x
        arr[i+1] += vel_y
    
    return arr, vel_x, vel_y, change_color

