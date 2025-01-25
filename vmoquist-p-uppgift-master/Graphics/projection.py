import math
import numpy as np

class Projection:
    """Takes display as a parameter in order to access values of objects created in the object of the Application class.
    These values are for the near and far plane of the view-frustum as well as the angles of the frustum. 
    They are then used to create projection matrices that ultimately are used to convert 3d objects
    onto a 2d viewing plane, ie the screen."""
    def __init__(self, display):
        NEAR = display.viewer.nearPlane
        FAR = display.viewer.farPlane
        RIGHT = math.tan(display.viewer.horizontalFov / 2)
        LEFT = -RIGHT
        TOP = math.tan(display.viewer.verticalFov / 2)
        BOT = -TOP

        #Use 2/ or 1/ - 1/ is standard when searching online
        m00 = 2 / (RIGHT-LEFT)
        m11 = 2 / (TOP - BOT)
        m22 = (FAR + NEAR) / (FAR - NEAR) # Total distance b/w near and far plane divided difference b/w near and far plane
        m23 = -2 * NEAR * FAR / (FAR - NEAR)
        self.projectionMatrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m23, 0]
        ])

        HW, HH = display.WIDTH // 2, display.HEIGHT // 2
        self.toScreenMatrix = np.array([
            [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ])

        #Row major form