import numpy as np
from OpenGL.GL import *
import transformations as tr


class Particle:
    def __init__(self, width_square, height_square, radius_circle, proportion):

        self.x = np.random.uniform(-width_square / 2 + radius_circle, width_square / 2 - radius_circle)

        self.y = np.random.uniform(-height_square / 2 + radius_circle * proportion,
                                   height_square / 2 - radius_circle * proportion)

        self.x_vector = np.random.choice([-1, 1])

        self.y_vector = np.random.choice([-1, 1])

        self.radius_circle = radius_circle

        self.width_square = width_square

        self.height_square = height_square

        self.proportion = proportion

        self.pipeline = None

        self.gpuShape = None

        self.activeEvent = None

        self.initial_velocity = 0

        self.velocity = 0

    def check_events(self):
        if self.activeEvent is not None:
            return
        select_event(self)

    def update(self):
        apply_active_event(self)
        self.x += self.velocity * self.x_vector
        self.y += self.velocity * self.y_vector
        if self.x + self.radius_circle >= self.width_square / 2 or \
                self.x - self.radius_circle <= -self.width_square / 2:
            self.x_vector = - self.x_vector

        if self.y + self.radius_circle * self.proportion >= self.height_square / 2 or \
                self.y - self.radius_circle * self.proportion <= -self.height_square / 2:
            self.y_vector = - self.y_vector

    def draw(self):
        glUseProgram(self.pipeline.shaderProgram)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glUniformMatrix4fv(glGetUniformLocation(self.pipeline.shaderProgram, 'transform'), 1, GL_TRUE,
                           tr.translate(self.x, self.y, 0))
        self.pipeline.drawShape(self.gpuShape)


def change_direction(particle):
    particle.velocity -= particle.initial_velocity / 30
    if particle.velocity <= 0:
        particle.x_vector = - particle.x_vector
        particle.y_vector = - particle.y_vector
        particle.activeEvent = 'reverse_change_direction'
        return


def reverse_change_direction(particle):
    particle.velocity += particle.initial_velocity / 30
    if particle.velocity >= particle.initial_velocity:
        particle.activeEvent = None
        return


def select_event(particle):
    particle.activeEvent = np.random.choice([None, 'change_direction'], p=[0.9, 0.1])


def apply_active_event(particle):
    if particle.activeEvent == 'change_direction':
        change_direction(particle)
    elif particle.activeEvent == 'reverse_change_direction':
        reverse_change_direction(particle)
