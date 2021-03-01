import numpy as np
from OpenGL.GL import *
import transformations as tr
class Particle:
    def __init__(self, width_square, height_square, radius_circle, proportion):

        self.x = np.random.uniform(-width_square / 2 + radius_circle, width_square / 2 - radius_circle)

        self.y = np.random.uniform(-height_square/2 + radius_circle * proportion, height_square/2 - radius_circle * proportion)

        self.x_vector = np.random.choice([-1, 1])

        self.y_vector = np.random.choice([-1, 1])

        self.radius_circle = radius_circle

        self.width_square = width_square

        self.height_square = height_square

        self.proportion = proportion

        self.pipeline = None

        self.gpuShape = None

    def set_pipeline(self, pipeline):
        self.pipeline = pipeline

    def set_gpuShape(self, shape):
        self.gpuShape = shape

    def update(self, velocity):
        self.x += velocity * self.x_vector
        self.y += velocity * self.y_vector
        if self.x + self.radius_circle >= self.width_square / 2 or \
                self.x - self.radius_circle <= -self.width_square / 2:

            self.x_vector = - self.x_vector

        if self.y_vector + self.radius_circle * self.proportion >= self.height_square / 2 or\
                self.y_vector - self.radius_circle * self.proportion <= -self.height_square / 2:

            self.y_vector = - self.y_vector

    def draw(self):
        glUseProgram(self.pipeline.shaderProgram)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glUniformMatrix4fv(glGetUniformLocation(self.pipeline.shaderProgram, 'transform'), 1, GL_TRUE,
                           tr.translate(self.x, self.y, 0))
        self.pipeline.drawShape(self.gpuShape)