import pyglet
from OpenGL import GL
import transformations as tr
import circle as cl
from pyglet.gl import *
import aux_functions as af
import random
import square as sq

# Seteamos variables para el tamaño
WIDTH = 640
HEIGHT = 640

# Tamaño imagen
WIDTH_img = 100
HEIGHT_img = 100
# Tamaño inicial de la imagen
initial_scale = 0.5 


# Asigno valores iniciales a la velocidad del círculo, cuadrado e imagen de forma random
VEL_X_cl = random.uniform(-0.03, 0.03)
VEL_Y_cl = random.uniform(-0.03, 0.03)
VEL_X_sq = random.uniform(-0.03, 0.03)
VEL_Y_sq = random.uniform(-0.03, 0.03)
VEL_X_img = random.choice([-3, -2, 2, 3])
VEL_Y_img = random.choice([-3, -2, 2, 3])

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

    vertex_source_code_img = """
        #version 330

        in vec3 position;
        in vec3 color;
        in float intensity;
        uniform mat4 transform;


        out vec3 fragColor;
        out float fragIntensity;

        void main()
        {
            fragColor = color;
            fragIntensity = intensity;
            gl_Position = vec4(position, 1.0f);
        }
    """

    # Compilamos los shaders
    vert_shader = pyglet.graphics.shader.Shader(vertex_source, "vertex")
    vert_shader_img = pyglet.graphics.shader.Shader(vertex_source_code_img, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source, "fragment")

    # Creamos nuestro pipeline de rendering
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)
    pipelineimg = pyglet.graphics.shader.ShaderProgram(vert_shader_img, frag_shader)


    # Creamos el circulo
    circle_pos = cl.create_circle(0.0, 0.0, 0.15, DEFINITION)

    # Creamos el circulo en la gpu, ahora con menos vertices en total
    # y le tenemos que pasar los índices
    circle_gpu = pipeline.vertex_list_indexed(DEFINITION+1, GL_TRIANGLES, cl.create_circle_indices(DEFINITION))

    # Copiamos los datos, añadimos el color
    circle_gpu.position[:] = circle_pos
    # Le asigno un color inicial al azar al círculo
    circle_gpu.color[:] = af.randomize_color(DEFINITION+1)

    # Ahora creamos el cuadrado
    square_gpu = pipeline.vertex_list_indexed(4, GL_TRIANGLES, sq.indices)
    # Asignamos la posición
    square_gpu.position[:] = sq.positions
    # Le asigno un color inicial al azar al cuadrado
    square_gpu.color[:] = af.randomize_color(4)

    # Cargamos la imagen
    image1 = pyglet.image.load("snoopy_happy.png")
    image2 = pyglet.image.load("snoopy_angry.png")

    # Crear sprite con posición inicial y escala
    sprite = pyglet.sprite.Sprite(image1, x = WIDTH_img, y = HEIGHT_img)
    sprite.scale = initial_scale

    @window.event
    def on_draw():

        # Esta linea limpia la pantalla entre frames
        window.clear()
        glClearColor(0, 0, 0, 1)

        pipeline.use()
        circle_gpu.draw(GL_TRIANGLES)
        square_gpu.draw(GL_TRIANGLES)
        
        pipelineimg.use()
        sprite.draw()

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



    # HAREMOS QUE UN SNOOPY SE ENOJE CADA VEZ QUE SE GOLPEE # 

    # timer_event me indicará si ya hay algún schedule_once corriendo, para poder pararlo y generar uno nuevo
    timer_event = False
    # Función para volver a la imagen original de snoopy feliz
    def reset_image(dt):
        global timer_event,sprite
        # Cancelar el temporizador si ya existe
        if timer_event:
            pyglet.clock.unschedule(timer_event)
        # Asignar la imagen original
        sprite.scale = initial_scale
        sprite.image = image1

    # Función para el movimiento de la imagen
    def move_image(dt):
        global sprite, VEL_X_img, VEL_Y_img, timer_event

        # Muevo la imagen
        sprite.x += VEL_X_img 
        sprite.y += VEL_Y_img

        # Rebotar en los bordes y cambiar de imagen
        if sprite.x + sprite.width  > window.width or sprite.x < 0:
            timer_event = True
            # Cambio el sentido del movimiento
            VEL_X_img = -VEL_X_img
            sprite.scale = 0.08
            sprite.image = image2
            # Luego de medio segundo, se vuelve a la imagen original
            pyglet.clock.schedule_once(reset_image, 0.5)  # Programar el reinicio en 1 segundo


        if sprite.y + sprite.height> window.height or sprite.y < 0:
            timer_event = True
            VEL_Y_img = -VEL_Y_img
            sprite.scale = 0.08
            sprite.image = image2
            pyglet.clock.schedule_once(reset_image, 0.5)  # Programar el reinicio en 1 segundo


            


    pyglet.clock.schedule_interval(move_circle, 1/60)
    pyglet.clock.schedule_interval(move_square, 1/60)
    pyglet.clock.schedule_interval(move_image, 1/60)


    pyglet.app.run()

    

