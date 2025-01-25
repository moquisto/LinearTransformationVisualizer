import pygame as pg
from matrices import *

class Viewer:
    def __init__(self, display, position):
        """This class creates a Viewer/camera object which views the 3d transformations. The viewer class takes
        a position parameter which is the relative position to the coordinate system. This position parameter
        is then changed by the controls method which allows the user to move the camera around in order to view
        things from other perspectives. Display is used to access things such as the resolution of the screen."""
        self.display = display
        self.position = np.array([*position, 1.0]) #Alternatively could use np.array(position + [1.0]). Achieves the same result.
        self.x = np.array([1,0,0,1])
        self.y = np.array([0,1,0,1])
        self.z = np.array([0,0,1,1])
        self.horizontalFov = math.pi / 2
        self.verticalFov = self.horizontalFov * (display.HEIGHT / display.WIDTH)
        self.nearPlane = 0.1
        self.farPlane = 100
        self.movementSpeed = 0.1
        self.rotationSpeed = 0.05
        self.objectRotationMde = False
        #Above will be implemented later
    
    def controls(self):
        """Checks for user input on the keyboard in order to move the perspective. Movement is done by calling the following methods."""
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.x * self.movementSpeed
        if key[pg.K_d]:
            self.position += self.x * self.movementSpeed
        if key[pg.K_w]:
            self.position += self.z * self.movementSpeed
        if key[pg.K_s]:
            self.position -= self.z * self.movementSpeed
        if key[pg.K_SPACE]:
            self.position += self.y * self.movementSpeed
        if key[pg.K_LCTRL]:
            self.position -= self.y * self.movementSpeed
        if key[pg.K_LEFT]:
            self.yaw(-self.rotationSpeed)
        if key[pg.K_RIGHT]:
            self.yaw(self.rotationSpeed)
        if key[pg.K_UP]:
            self.pitch(-self.rotationSpeed)
        if key[pg.K_DOWN]:
            self.pitch(self.rotationSpeed)

    def yaw(self, angle):
        """Rotates camera left and right according to the angle specified by the user input from controls using the rotation matrix below."""
        rotate = rotateY(angle)
        self.z = self.z @ rotate
        self.x = self.x @ rotate
        self.y = self.y @ rotate

    def pitch(self, angle):
        """Rotates camera up and down like the camera_yaw method."""
        rotate = rotateX(angle)
        self.z = self.z @ rotate
        self.x = self.x @ rotate
        self.y = self.y @ rotate

    def viewTranslationMatrix(self):
        """Takes the position specified by the viewer and constructs a translation matrix which will later be applied
        on the objects in the rendered space in order to give off the illusion of the camera moving (camera is actually
        stationary, it is the world that moves around it.)"""
        x, y, z, w = self.position
        return np.array([
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [-x,-y,-z,1]
        ])

    def viewRotationMatrix(self):
        """Like the translation matrix but for rotation."""
        xx, xy, xz, w = self.x
        yx, yy, yz, w = self.y
        zx, zy, zz, w = self.z
        return np.array([
            [xx, yx, zx, 0],
            [xy, yy, zy, 0],
            [xz, yz, zz, 0], 
            [0, 0, 0, 1]
        ])

    def viewMatrix(self):
        """Combines both translation and rotation to create a new matrix which will be applied on the verteces of the 3d objects."""
        if self.objectRotationMde == False:
            return self.viewTranslationMatrix() @ self.viewRotationMatrix()
        else:
            return self.viewRotationMatrix() @ self.viewTranslationMatrix() #Does not work as intended atm
