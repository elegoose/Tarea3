from OpenGL.GL import *
import easy_shaders as es
import transformations as tr
import basic_shapes as bs


class Graph:
    def __init__(self, controller, proportion):
        self.controller = controller
        self.proportion = proportion
        self.pipeline = es.SimpleTextureTransformShaderProgram()
        self.gpuShape = es.toGPUShape(bs.createTextureQuad('graph_texture.png'), GL_REPEAT, GL_NEAREST)
        self.bars = [Bar('susceptibles', (0, 0, 1), controller),
                     Bar('recuperados', (0.5, 0.5, 0.5), controller),
                     Bar('infectados', (1, 0, 0), controller),
                     Bar('muertos', (0.8, 0, 0.8), controller)
                     ]

    def draw(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glUseProgram(self.pipeline.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(self.pipeline.shaderProgram, 'transform'), 1, GL_TRUE,
                           tr.matmul([tr.translate(-0.6, 0, 0),
                                      tr.scale(0.6, self.proportion * 0.6, 0)
                                      ]))

        self.pipeline.drawShape(self.gpuShape)

        for bar in self.bars:
            bar.draw()

    def update(self):
        bar_distance = -0.8
        for bar in self.bars:
            bar.update()
            bar.transformation = tr.matmul([tr.translate(bar_distance, bar.value * self.proportion/2 - 0.39, 0),
                                            tr.scale(0.1, self.proportion * bar.value, 0)])
            bar_distance += 0.138


class Bar:
    def __init__(self, bar_name, color, controller):
        self.name = bar_name
        self.color = color
        self.transformation = None
        self.gpuShape = es.toGPUShape(bs.createColorQuad(*color))
        self.pipeline = es.SimpleTransformShaderProgram()
        self.controller = controller
        self.value = get_value(self)

    def draw(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glUseProgram(self.pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(self.pipeline.shaderProgram, 'transform'), 1, GL_TRUE,
                           self.transformation)
        self.pipeline.drawShape(self.gpuShape)

    def update(self):
        self.value = get_value(self)


def get_value(bar):

    if bar.name == 'susceptibles':
        percentage = bar.controller.susceptibleCount / bar.controller.particleAmount
        return percentage * 0.5
    elif bar.name == 'recuperados':
        percentage = bar.controller.recoveredCount / bar.controller.particleAmount
        return percentage * 0.5
    elif bar.name == 'infectados':
        percentage = bar.controller.infectedCount / bar.controller.particleAmount
        return percentage * 0.5
    else:
        percentage = bar.controller.deathCount / bar.controller.particleAmount
        return percentage * 0.5
