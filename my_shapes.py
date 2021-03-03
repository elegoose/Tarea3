import numpy as np
import basic_shapes as bs


def createCircle(N, r, g, b, radius, proportion):
    vertices = [0, 0, 0, r, g, b]  # Primer vertice
    indices = []

    dtheta = 2 * np.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            radius * np.cos(theta), radius * proportion * np.sin(theta), 0,
            r, g, b]

        # Se crean triángulos respecto al centro para rellenar la circunferencia
        indices += [0, i, i + 1]
    # Conectado al segundo vertice
    indices += [0, N, 1]

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    return bs.Shape(vertices, indices)


def createSquare(width_square, height_square):
    # Defining locations and colors for each vertex of the shape
    r, g, b = 1, 1, 1  # Color: white
    vertices = [
        #   positions        colors
        -width_square/2, -height_square/2, 0.0, r, g, b,
        width_square/2, -height_square/2, 0.0, r, g, b,
        width_square/2, height_square/2, 0.0, r, g, b,
        -width_square/2, height_square/2, 0.0, r, g, b
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 1,
        1, 2, 2,
        2, 3, 3,
        3, 0, 0
    ]

    return bs.Shape(vertices, indices)