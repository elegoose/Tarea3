# Radius: radio de contagio entra una persona y otra
# Contagious_prob: probabilidad de contagio. Si la persona se encuentra en radius, se puede contagiar
# con esa probabilidad.
# Death_rate: probabilidad de muerte por contagio
# Initial_population: población inicial
# Days_to_heal: cantidad de días para recuperarse

import glfw
from OpenGL.GL import *
import sys
# import basic_shapes as bs
import easy_shaders as es
import transformations as tr
# import json
import my_shapes as my
import particleclass as pr


class Timer:
    def __init__(self):
        self.initial_time = 0
        self.current_time = 0
        self.seconds_passed = 0

    def update(self):
        self.seconds_passed = self.current_time - self.initial_time

    def seconds_has_passed(self, seconds):
        if self.current_time == 0:
            return False
        if self.seconds_passed >= seconds:
            self.initial_time = glfw.get_time()
            return True
        else:
            return False


if __name__ == '__main__':
    # Initialize glfw
    if not glfw.init():
        sys.exit()
    width = 1280
    height = 720
    proportion = width / height
    window = glfw.create_window(width, height, 'Pandemic Simulator 2D', None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)

    # Estableciendo color de pantalla
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Estableciendo pipelines
    texturePipeline = es.SimpleTextureTransformShaderProgram()
    figurePipeline = es.SimpleTransformShaderProgram()

    # Estableciendo medidas
    width_square = 1
    height_square = proportion
    radius_circle = 0.02
    particle_amount = 20
    # Creando figuras
    circle = my.createCircle(30, 0, 0, 1, radius_circle, proportion)
    square = my.createSquare(width_square, height_square)

    # Almacenando figuras en GPU
    gpuCircle = es.toGPUShape(circle)
    gpuSquare = es.toGPUShape(square)

    particle_array = []
    for i in range(particle_amount):
        particle = pr.Particle(width_square, height_square, radius_circle, proportion)
        particle.pipeline = figurePipeline
        particle.gpuShape = gpuCircle
        particle.initial_velocity = 0.01/5
        particle.velocity = particle.initial_velocity
        # particle.clock.initial_time = glfw.get_time()
        particle_array.append(particle)

    clock = Timer()
    clock.initial_time = glfw.get_time()
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        clock.current_time = glfw.get_time()
        clock.update()
        time_up = clock.seconds_has_passed(3)
        for particle in particle_array:
            if time_up:
                particle.check_events()

            particle.update()
            particle.draw()

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(3)
        glUniformMatrix4fv(glGetUniformLocation(figurePipeline.shaderProgram, 'transform'), 1, GL_TRUE,
                           tr.identity())
        figurePipeline.drawShape(gpuSquare)

        glfw.swap_buffers(window)

    glfw.terminate()
