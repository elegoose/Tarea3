# Autor : Felipe Torralba
# Algunos comentarios y variables del código están en ingles por simplicidad y legibilidad de código
import glfw
from OpenGL.GL import *
import sys
import easy_shaders as es
import transformations as tr
import json
import my_shapes as my
import particleclass as pr
import numpy as np
import graphmatplotlib as matplot
import graphopengl as opengl_graph


class Controller:
    def __init__(self):
        self.pause = False

        self.infectedCount = 0
        self.susceptibleCount = 0
        self.recoveredCount = 0
        self.deathCount = 0
        self.dayCount = 0
        self.particleAmount = 0
        self.print = False

    def print_particle_count(self):
        print("---------------")
        print('infected:', self.infectedCount)
        print('susceptible:', self.susceptibleCount)
        print('recovered:', self.recoveredCount)
        print('dead:', self.deathCount)
        total = self.susceptibleCount + self.recoveredCount + \
            self.deathCount + self.infectedCount
        print("total:", total)
        if total != self.particleAmount:
            self.pause = True
            print("Error")

    def draw_matplotlib(self):
        matplot.drawgraph(self.susceptibleCount,
                          self.recoveredCount,
                          self.deathCount,
                          self.infectedCount,
                          self.dayCount)


controller = Controller()


def on_key(window, key, scancode, action, mods):  # noqa
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_P:
        controller.pause = not controller.pause
        controller.print = not controller.print
        if controller.print:
            controller.print_particle_count()
            controller.draw_matplotlib()


class Timer:
    def __init__(self):
        self.initial_time = 0
        self.current_time = 0
        self.seconds_passed = 0

    def update(self):
        self.current_time = glfw.get_time()
        self.seconds_passed = self.current_time - self.initial_time

    def seconds_has_passed(self, seconds):
        if self.current_time == 0:
            return False
        elif self.seconds_passed >= seconds:
            self.initial_time = glfw.get_time()
            return True
        else:
            return False


class Virus:
    def __init__(self, radius, contagious_prob, death_rate, days_to_heal):
        self.radius = radius
        self.contagious_prob = contagious_prob
        self.death_rate = death_rate
        self.days_to_heal = days_to_heal


def check_nearby_particles(this_particle, my_particle_array):
    if this_particle.ignore:
        return
    aux_particle_array = list(my_particle_array)
    aux_particle_array.remove(this_particle)
    for near_particle in aux_particle_array:
        if near_particle.ignore:
            pass
        dx = this_particle.x - near_particle.x
        dy = this_particle.y - near_particle.y
        distance = np.sqrt(dx ** 2 + dy ** 2)
        if distance < \
                this_particle.radius_circle + near_particle.radius_circle + virus.radius and \
                this_particle.state == 'infected' and \
                near_particle.state == 'susceptible':
            choice = np.random.choice([None, 'infect'],
                                      p=[1 - virus.contagious_prob, virus.contagious_prob])
            if choice == 'infect':
                near_particle.infect()


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
    glfw.set_key_callback(window, on_key)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Estableciendo color de pantalla
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Estableciendo pipelines
    figurePipeline = es.SimpleTransformShaderProgram()

    # Estableciendo medidas
    width_square = 0.5
    height_square = width_square * proportion
    radius_circle = 0.01

    # Creando figuras
    circle = my.createCircle(30, 0, 0, 1, radius_circle, proportion)
    square = my.createSquare(width_square, height_square)

    # Almacenando figuras en GPU
    gpuCircle = es.toGPUShape(circle)
    gpuSquare = es.toGPUShape(square)

    # Virus variables
    with open('virus.json') as f:
        data = json.load(f)
    virus_data = data[0]
    virus = Virus(virus_data['Radius'],
                  virus_data['Contagious_prob'],
                  virus_data['Death_rate'],
                  virus_data['Days_to_heal'])

    particle_amount = virus_data['Initial_population']
    controller.susceptibleCount = particle_amount

    particle_array = []
    for i in range(particle_amount):
        particle = pr.Particle()
        particle.set_box_limits(width_square, height_square, radius_circle, proportion)
        particle.set_initial_pos()
        particle.pipeline = figurePipeline
        particle.gpuShape = gpuCircle
        particle.initial_velocity = 0.01 / 6
        particle.velocity = particle.initial_velocity
        particle.virus = virus
        particle.controller = controller
        particle_array.append(particle)
    particle_array[0].infect()  # Infect the first particle
    particle_array[1].infect()

    # Opengl graph Values
    controller.particleAmount = particle_amount
    graph = opengl_graph.Graph(controller, proportion)

    clock = Timer()
    clock.initial_time = glfw.get_time()
    dayCounter = Timer()
    dayCounter.initial_time = glfw.get_time()

    graph.update()
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        if not controller.pause:

            dayCounter.update()
            # Every one second, a day passes
            dayPassed = dayCounter.seconds_has_passed(1)

            clock.update()
            time_up = clock.seconds_has_passed(5)
            for particle in particle_array:
                if 0.5 >= dayCounter.seconds_passed >= 0.4:
                    check_nearby_particles(particle, particle_array)
                if dayPassed:
                    particle.dayPassed = True
                    if particle.state == 'infected':
                        particle.daysInfected += 1
                    if particle.state == 'dead':
                        particle.disappear()

                else:
                    particle.dayPassed = False
                if time_up:
                    # Check random movement events every 5 seconds
                    particle.check_events()

                particle.update()
                particle.draw()

            if dayPassed:
                graph.update()
                controller.dayCount += 1
                print('day:', controller.dayCount)
        else:
            for particle in particle_array:
                particle.draw()
        glUseProgram(figurePipeline.shaderProgram)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(3)
        glUniformMatrix4fv(glGetUniformLocation(figurePipeline.shaderProgram, 'transform'), 1, GL_TRUE,
                           tr.identity())
        figurePipeline.drawShape(gpuSquare)

        graph.draw()

        glfw.swap_buffers(window)

    glfw.terminate()
