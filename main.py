import pyglet
from OpenGL import GL
import transformations as tr
import circle as cl
from pyglet.gl import *
import aux_functions as af
import random
import square as sq


# Opcionalmente seteamos variables para el tamaño
WIDTH = 640
HEIGHT = 640

# Asigno valores iniciales a la velocidad del círculo y cuadrado de forma random
VEL_X_cl = random.uniform(-0.03, 0.03)
VEL_Y_cl = random.uniform(-0.03, 0.03)
VEL_X_sq = random.uniform(-0.03, 0.03)
VEL_Y_sq = random.uniform(-0.03, 0.03)

# Cantidad de triángulos a usar para armar el círculo
DEFINITION = 100

# controlador de la ventana, basicamente una ventana
class Controller(pyglet.window.Window):
    #Función init se ejecuta al construir el objeto
    def __init__(self, title, *args, **kargs):
        super().__init__(*args, **kargs)
        # Evita error cuando se redimensiona a 0
        self.set_minimum_size(240, 240)
        self.set_caption(title)


if __name__ == "__main__":

    # Creamos una instancia del controlador
    window = Controller("Tarea 1", width=WIDTH,
                            height=HEIGHT, resizable=True)
    # Creamos nuestros shaders
    vertex_source = """
#version 330

in vec3 position;
in vec3 color;

out vec3 fragColor;

void main() {
    fragColor = color;
    gl_Position = vec4(position, 1.0f);
}
    """

    fragment_source = """
#version 330

in vec3 fragColor;
out vec4 outColor;

void main()
{
    outColor = vec4(fragColor, 1.0f);
}
    """

    # Compilamos los shaders
    vert_program = pyglet.graphics.shader.Shader(vertex_source, "vertex")
    frag_program = pyglet.graphics.shader.Shader(fragment_source, "fragment")

    # Creamos nuestro pipeline de rendering
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_program, frag_program)

    # Creamos el circulo
    circle_pos = cl.create_circle(0.0, 0.0, 0.15, DEFINITION)

    # Creamos el circulo en la gpu, ahora con menos vertices en total
    # y le tenemos que pasar los indices
    circle_gpu = pipeline.vertex_list_indexed(DEFINITION+1, GL_TRIANGLES, cl.create_circle_indices(DEFINITION))

    # Copiamos los datos, añadimos el color
    circle_gpu.position[:] = circle_pos
    # Le asigno un color inicial al azar al círculo
    circle_gpu.color[:] = af.randomize_color(DEFINITION+1)

    # Ahora creamos el cuadrado
    # Creamos el cuadrado en la gpu
    square_gpu = pipeline.vertex_list_indexed(4, GL_TRIANGLES, sq.indices)
    # Copiamos los datos, añadimos el color
    square_gpu.position[:] = sq.positions
    # Le asigno un color inicial al azar al cuadrado
    square_gpu.color[:] = af.randomize_color(4)


    @window.event
    def on_draw():

        # Esta linea limpia la pantalla entre frames
        window.clear()
        glClearColor(0, 0, 0, 1)

        pipeline.use()
        circle_gpu.draw(GL_TRIANGLES)
        square_gpu.draw(GL_TRIANGLES)

    # Función para mover el círculo
    def move_circle(dt):
        global VEL_X_cl, VEL_Y_cl
        # Lógica del movimiento y el rebote en el borde en la funcion move_circ
        circle_gpu.position[:], VEL_X_cl, VEL_Y_cl, changed_color = cl.move_circ(dt, circle_gpu.position[:], VEL_X_cl, VEL_Y_cl)
        # Si la variable changed_color es True, cambio el color del círculo
        if changed_color:
            # Genero un nuevo color al azar
            new_color = af.randomize_color(DEFINITION+1)
            # Asigno el nuevo color al círculo
            circle_gpu.color[:] = new_color

    def move_square(dt):
        global VEL_X_sq, VEL_Y_sq
        # Lógica del movimiento y el rebote en el borde en la funcion move_sq
        square_gpu.position[:], VEL_X_sq, VEL_Y_sq = sq.move_sq(square_gpu.position[:], VEL_X_sq, VEL_Y_sq)


    pyglet.clock.schedule_interval(move_circle, 1/60)
    pyglet.clock.schedule_interval(move_square, 1/60)


    pyglet.app.run()

    

