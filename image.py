import pyglet
from OpenGL import GL
import numpy as np
import transformations as tr


# Definimos la clase "Imagen" para generar imagenes mas fácilmente
class Image():
    def __init__(self, path, width, height, x = 0, y = 0):
        self.image = pyglet.resource.image(path)
        self.image.width = width
        self.image.height = height
        self.x = x
        self.y = y

    def draw(self):
        self.image.blit(self.x, self.y)