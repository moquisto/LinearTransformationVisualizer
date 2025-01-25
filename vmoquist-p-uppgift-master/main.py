import pygame as pg
from Graphics.viewer import *
from Graphics.projection import *
from Graphics.objects import *
from components import *

class Application:
    """This class creates instances of the application, only one will be made but you could technically create more with this approach.
    It has a few attributes that are essential for the pg.display to work such as resolution. Also includes FPS to cap refresh rate."""
    def __init__(self):
        pg.init()
        self.WIDTH = 1600
        self.HEIGHT = 900
        self.FPS = 60
        self.RES = (self.WIDTH, self.HEIGHT)
        self.screen_flags = pg.RESIZABLE
        self.screen = pg.display.set_mode(self.RES, self.screen_flags)
        self.clock = pg.time.Clock()
        self.black = pg.Color("black")
        self.createObjects()
    
    def createObjects(self):
        """Creates objects from the other files."""

        """Initializes camera and projection"""
        self.viewer = Viewer(self, [1.5, 2, -4])
        self.viewer.pitch(0.2)
        self.viewer.yaw(-0.1)
        self.projection = Projection(self)

        """Initializes objects and tweaks their attributes"""
        #self.object = Object3d(self)
        #self.object.translate([0.2, 0.4, 0.2])
        self.world_axes = Axes(self)
        self.world_axes.movement_flag = False
        self.world_axes.scale(2.5)
        self.world_axes.translate([0.0001, 0.0001, 0.0001])
        self.create_vector = CreateVector(self, 50, 100)
        self.create_matrix = CreateMatrix(self, 50, 100)
        self.create_grid2d = CreateGrid(self, 50, 300, 2)
        self.create_grid3d = CreateGrid(self, 50, 450, 3)
        self.transform_button = TransformButton(self, 50, 300)
        
        """Navigation buttons"""
        self.mainToTransform = NavigationButton(self, 50, 200, 250, 40, "Transformation menu")
        self.transformToMain = NavigationButton(self, 50, 200, 250, 40, "Main")

    def draw_main(self):
        """Sets values for pixels on the scren before flipping in main."""
        self.screen.fill(self.black)
        #self.object.draw()
        self.world_axes.draw()
        self.create_vector.draw()
        self.transform_button.draw()
        self.mainToTransform.draw()
        self.create_grid2d.drawGrid()
        self.create_grid3d.drawGrid()

    def main(self):
        """Main loop. Animations happen here."""
        while True:
            """Logic for switching screens"""
            if self.mainToTransform.switch == True:
                self.transformationScreen()
                self.mainToTransform.switch = False
            """Logic for animating 3d vectors in vectorList"""
            if len(self.create_vector.vectorList) != 0:
                for vectorPack in self.create_vector.vectorList:
                    vectorPack.animate()
            self.draw_main()
            self.viewer.controls()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                """New functionality - currently not working"""
                if event.type == pg.KEYDOWN: #Beta vesion yo
                    if event.key == pg.K_r:
                        if self.camera.objectRotationMde == False:
                            print("Now True")
                            self.camera.objectRotationMde = True
                        else:
                            print("Now False")
                            self.camera.objectRotationMde = False
                self.mainToTransform.eventHandler(event)
                self.create_vector.eventHandler(event)
                self.transform_button.eventHandler(event, [self.create_vector.vectorList, self.create_grid2d.gridList, self.create_grid3d.gridList])
            pg.display.set_caption("Main screen  🐫  FPS = " + str(round(self.clock.get_fps())))
            pg.display.flip()
            self.clock.tick(self.FPS)

    def draw_transform(self):
        """Draw method for transformation screen"""
        self.screen.fill(self.black)
        self.transformToMain.draw()
        self.create_matrix.draw()
        self.create_grid2d.draw()
        self.create_grid3d.draw()
    
    def transformationScreen(self):
        """TransformationScreen loop, this is where you can modify matrices (soon might be able to change mesh too)"""
        self.screen.fill(pg.Color("black"))
        running = True
        while running:
            if self.transformToMain.switch == True:
                running = False
                self.transformToMain.switch = False
            self.draw_transform()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                self.transformToMain.eventHandler(event)
                self.create_matrix.eventHandler(event)
                self.create_grid2d.eventHandler(event)
                self.create_grid3d.eventHandler(event)
                self.transform_button.matrices = self.create_matrix.matrixList[:]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    app = Application()
    app.main()