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
import numpy as np
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

    # Creando figuras
    circle = my.createCircle(30, 0, 0, 1, radius_circle, proportion)
    square = my.createSquare(width_square, height_square)

    # Almacenando figuras en GPU
    gpuCircle = es.toGPUShape(circle)
    gpuSquare = es.toGPUShape(square)
    x = np.random.uniform(-width_square/2 + radius_circle, width_square/2 - radius_circle)
    y = np.random.uniform(-height_square/2 + radius_circle * proportion, height_square/2 - radius_circle * proportion)
    x_vector = np.random.choice([-1, 1])
    y_vector = np.random.choice([-1, 1])
    t0 = glfw.get_time()
    while not glfw.window_should_close(window):
        glfw.poll_events()

        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
        velocity = dt/5
        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        x += velocity * x_vector
        y += velocity * y_vector
        if x + radius_circle >= width_square/2 or x - radius_circle <= -width_square/2:
            x_vector = - x_vector
        if y + radius_circle*proportion >= height_square/2 or y - radius_circle*proportion <= -height_square/2:
            y_vector = - y_vector
        glUseProgram(figurePipeline.shaderProgram)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glUniformMatrix4fv(glGetUniformLocation(figurePipeline.shaderProgram, 'transform'), 1, GL_TRUE,
                           tr.translate(x, y, 0))
        figurePipeline.drawShape(gpuCircle)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(3)
        glUniformMatrix4fv(glGetUniformLocation(figurePipeline.shaderProgram, 'transform'), 1, GL_TRUE,
                           tr.identity())
        figurePipeline.drawShape(gpuSquare)
        glfw.swap_buffers(window)

    glfw.terminate()
