import numpy as np
from OpenGL.GL import *
import transformations as tr
import my_shapes as my
import easy_shaders as es
import basic_shapes as bs


class Particle:
    def __init__(self):

        self.x, self.y, self.x_vector, self.y_vector = 0, 0, 0, 0

        self.radius_circle = 0

        self.width_square, self.height_square, self.proportion = 0, 0, 0

        self.pipeline, self.gpuShape = None, None

        self.activeEvent = None

        self.initial_velocity, self.velocity = 0, 0

        self.acceleration_factor = 1

        self.virus = None

        self.daysInfected = 0

        self.dayPassed = False

        self.transformation = tr.identity()

        self.state = 'susceptible'

        self.count = True

    def set_box_limits(self, width_square, height_square, radius_circle, proportion):

        self.width_square = width_square

        self.height_square = height_square

        self.proportion = proportion

        self.radius_circle = radius_circle

    def set_initial_pos(self):
        self.x = np.random.uniform(-self.width_square / 2 + self.radius_circle,
                                   self.width_square / 2 - self.radius_circle)

        self.y = np.random.uniform(-self.height_square / 2 + self.radius_circle * self.proportion,
                                   self.height_square / 2 - self.radius_circle * self.proportion)

        self.x_vector = np.random.choice([-1, 1])

        self.y_vector = np.random.choice([-1, 1])

    def set_virus(self, virus):
        self.virus = virus

    def infect(self):
        color = (1, 0, 0)  # red
        self.gpuShape = es.toGPUShape(
            my.createCircle(30, *color, self.radius_circle, self.proportion)
        )
        self.state = 'infected'

    def check_events(self):
        if self.activeEvent is not None:
            return
        select_event(self)

    def update(self):
        if self.dayPassed and self.state == 'infected':
            if self.daysInfected < 5:
                choice = np.random.choice(['die', 'live'],
                                          p=[
                                              self.virus.death_rate,
                                              1 - self.virus.death_rate
                                          ])
                if choice == 'die':
                    kill(self)
            else:
                choice = np.random.choice(['die', 'live'],
                                          p=[
                                              self.virus.death_rate,
                                              1 - self.virus.death_rate
                                          ])
                if choice == 'die':
                    kill(self)
                else:
                    recover(self)

        if self.state != 'dead':
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
                           tr.matmul([tr.translate(self.x, self.y, 0), self.transformation]))
        self.pipeline.drawShape(self.gpuShape)

    def dissapear(self):
        self.transformation = tr.uniformScale(0)

def kill(particle):
    particle.state = 'dead'
    particle.pipeline = es.SimpleTextureTransformShaderProgram()
    particle.gpuShape = es.toGPUShape(bs.createTextureQuad('x_texture.png'), GL_REPEAT, GL_NEAREST)
    particle.velocity = 0
    particle.transformation = tr.uniformScale(0.05)

def recover(particle):
    particle.state = 'recovered'
    color = (0.5, 0.5, 0.5)  # Gray
    particle.gpuShape = es.toGPUShape(
        my.createCircle(30, *color, particle.radius_circle, particle.proportion)
    )

def select_event(particle):
    particle.activeEvent = np.random.choice(
        [None, 'initiate change_direction', 'vertical_acceleration', 'vertical_deceleration'],
        p=[0.6, 0.1, 0.2, 0.1])


def apply_active_event(particle):
    if particle.activeEvent is None:
        return
    elif 'change_direction' in particle.activeEvent:
        change_direction(particle)
    elif particle.activeEvent == 'vertical_acceleration':
        vertical_acceleration(particle)
    elif particle.activeEvent == 'vertical_deceleration':
        vertical_deceleration(particle)


def change_direction(particle):
    if 'decrease_velocity' in particle.activeEvent or \
            'initiate change_direction' in particle.activeEvent:
        decrease_velocity(particle)
    else:
        # It already is turned around
        increase_velocity(particle)


def vertical_acceleration(particle):
    particle.acceleration_factor += 0.01
    if particle.acceleration_factor >= 3:
        particle.activeEvent = None
        return
    particle.y_vector = abs(particle.y_vector) * particle.acceleration_factor / particle.y_vector


def vertical_deceleration(particle):
    particle.acceleration_factor -= 0.01
    if particle.acceleration_factor <= 0.5:
        particle.activeEvent = None
        return
    particle.y_vector = abs(particle.y_vector) * particle.acceleration_factor / particle.y_vector


# Para change_direction
def decrease_velocity(particle):
    particle.velocity -= particle.initial_velocity / 30
    particle.activeEvent = '(change_direction) decrease_velocity'
    if particle.velocity <= 0:
        # Turn around
        particle.x_vector = - particle.x_vector
        particle.y_vector = - particle.y_vector
        particle.activeEvent = '(change_direction) increase_velocity'


# Para change_direction
def increase_velocity(particle):
    particle.velocity += particle.initial_velocity / 30
    if particle.velocity >= particle.initial_velocity:
        particle.activeEvent = None
