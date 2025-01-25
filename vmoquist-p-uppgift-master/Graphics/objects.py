import pygame as pg
from matrices import *

class Object3d:
    """This class creates some values which are used for all 3d objects as well as includes the method
    which uses the matrices from the projection.py class in order to map 3d objects onto the screen (draw())."""
    def __init__(self, display):
        self.display = display
        self.verteces = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (0.5, 0.5, 1, 1)]) #Example - pyramid
        self.faces = np.array([(0, 1, 2), (1, 2, 3), (0, 1, 4), (0, 2, 4), (1, 3, 4), (2, 3, 4)]) #Pyramid has 5 surfaces. BUt 
        self.font = pg.font.SysFont("Arial", 30, bold = True)
        self.color_faces = [(pg.Color("blue"), face) for face in self.faces]
        self.draw_verteces = True
        self.label = ""
    
    def draw(self):
        """Uses matrices to change the coordinates of the verteces into view/camera space (viewer is at origin) and then
        from camera-space to clip space (after projection) and then finally to the 2d screen using another matrix which takes the coordinates of the
        verteces of each 3d object and maps them to the display according to the screen resolution (rasterization)."""
        verteces = self.verteces @ self.display.viewer.viewMatrix() # First we align the verteces to the position given by our viewer/camera
        verteces = verteces @ self.display.projection.projectionMatrix # Then we project it onto the screen using the projection matrix
        verteces /= verteces[:, -1].reshape(-1, 1) # Division by w for depth perception. Things get weird when this is commented out.
        verteces[(verteces > 2) | (verteces < -2)] = 0 # Cutoff for things outside the screen. 
        verteces = verteces @ self.display.projection.toScreenMatrix # Final projection to the screen, this means that only 2 dimensions are relevant now.
        verteces = verteces[:, :2] # For each vertex, we cut off the z and w component since the screen only has x and y components.
        
        #Draws faces specified by object
        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = verteces[face] # Look at self.color_faces
            if not np.any((polygon == self.display.WIDTH // 2) | (polygon == self.display.HEIGHT // 2)):
                pg.draw.polygon(self.display.screen, color, polygon, 3) # Works like pygame's rectangle but is a polygon.
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color("white"))
                    self.display.screen.blit(text, polygon[-1])
        #Draws verteces specified by object
        if self.draw_verteces:
            for vertex in verteces:
                if not np.any((vertex == self.display.WIDTH // 2) | (vertex == self.display.HEIGHT // 2)):
                    pg.draw.circle(self.display.screen, pg.Color("white"), vertex, 5)

    def translate(self, pos):
        """Translation matrix from matrices - reason why it is in objects and not just used directly
        is because of ease of use as a method on a 3d object."""
        self.verteces = self.verteces @ translate(pos)

    def scale(self, scale_to):
        """Similar to translate() but for scaling."""
        self.verteces = self.verteces @ scale(scale_to)
    
    def transformationHandler(self, matrix):
        """Handles general transformations of 3d objects like grids - built to be compatible with future
        3d objects if implemented. The actual animation is handled by the animationHandler() method"""
        if self.change == False:
            matrix = np.transpose(matrix)
            matrix = matrix.tolist()
            for row in matrix:
                row.append(0)
            matrix.append([0,0,0,1])
            matrix = np.array(matrix)
            self.ogVerteces = self.verteces[:]
            self.goalVerteces = self.verteces @ matrix
            self.deltaVerteces = [[0,0,0,1]] * len(self.goalVerteces)
            for i in range(len(self.verteces)):   
                self.deltaVerteces[i] = (self.goalVerteces[i] - self.verteces[i])/60
            self.deltaVerteces = np.array(self.deltaVerteces)
            self.change = True

    def animationHandler(self):
        """Works together with transformationHandler to animate transformations."""
        if self.change == True:
            if self.count == 60:
                self.verteces = self.goalVerteces
                self.change = False
                self.count = 1
            else:
                self.verteces = self.verteces + self.deltaVerteces
                self.count += 1

class Axes(Object3d):
    """3d object for the axes that display the x,y and z axes."""
    def __init__(self, display):
        super().__init__(display)
        self.verteces = np.array(
            [(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color("red"), pg.Color("green"), pg.Color("blue")]
        self.color_faces = [(color, face)
                            for color, face in zip(self.colors, self.faces)]
        self.draw_verteces = False
        self.label = "XYZ"

class Vector(Object3d):
    """3d object for displaying vectors. Due to the additional functionality with changing vectors without
    transformations (from zero-vector to non-zero for example), this object doesn't share the same transformationHandler."""
    def __init__(self, display, vector):
        super().__init__(display)
        self.verteces = np.array([
            (0,0,0,1), (vector[0], vector[1] ,vector[2] ,1)
        ])
        self.faces = np.array([(0, 1)])
        self.colors = [pg.Color("purple")]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.label = "Vector"

class Grid2d(Object3d):
    """2d grid object built by loops. Each intersection of lines in the grid is given as a vertex,
    each line is between the edges of the grid and not between each vertex to lower memory and time complexity."""
    def __init__(self, display, length):
        super().__init__(display)
        #Use da loop
        self.verteces = []
        self.faces = []
        self.change = False
        self.count = 1
        self.length = length
        n = self.length
        for i in range(n):
            for j in range(n):
                self.verteces.append((i, j, 0, 1))
                #Since there will be n^2 many points. Each row has n points. We can use this to find the right faces.
        for i in range(n):
            self.faces.append((i*n, ((i+1)*n)-1))
            self.faces.append((i, n**2 - n + i))
        self.verteces = np.array(self.verteces)
        self.faces = np.array(self.faces)
        self.color = pg.Color("blue")
        self.color_faces = []
        for face in self.faces:
            self.color_faces.append((self.color, face))
        
class Grid3d(Object3d):
    """Similar to Grid2d but for 3 dimensions."""
    def __init__(self, display, length):
        super().__init__(display)
        self.verteces = []
        self.faces = []
        self.change = False
        self.count = 1
        self.draw_verteces = True
        self.length = length
        n = self.length
        for k in range(n):
            for j in range(n):
                for i in range(n):
                    self.verteces.append((i, j, k, 1))
        for j in range(n):
            for i in range(n):
                self.faces.append(((j*n*n)+(i*n), ((j*n*n)+(i+1)*n)-1))
                self.faces.append(((j*n*n)+i, (j*n*n)+n**2 - n + i)) 
                self.faces.append((((j*n)+(i)), (n**3 - n**2) + (j*n)+(i))) 
        self.verteces = np.array(self.verteces)
        self.faces = np.array(self.faces)
        self.color = pg.Color("blue")
        self.color_faces = []
        for face in self.faces:
            self.color_faces.append((self.color, face))