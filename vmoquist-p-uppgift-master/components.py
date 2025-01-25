import pygame as pg
from Graphics.objects import *

class InputButton:
    def __init__(self, render, x, y, w, h, text = ""):
        """Class that creates button-objects which the user can click and assert values to.
        This is later used when the user inputs values to matrices and vectors. 
        The class takes a few parameters relating to the dimensions of the rectangular
        box which will be drawn, render - which is needed to later draw the button on
        the screen as well as the text value which defaulted to an empty string unless 
        called with the text parameter."""
        self.render = render
        self.FONT = pg.font.Font(None, 32)
        self.COLOR_ACTIVATED, self.COLOR_INACTIVATED, self.COLOR = pg.Color("red"), pg.Color("white"), pg.Color("white")
        self.TEXT_COLOR = pg.Color("white")
        self.rectangle = pg.Rect(x, y, w, h)
        self.text = text
        self.displayed_text = self.FONT.render(self.text, True, self.COLOR)
        self.active = False
    
    def eventHandler(self, event):
        """This method handles the logic of the inputButton. It takes the event parameter
        which comes from pg.event in order to determine whether the user clicked on the button
        or not as well as to confirm user input from the keyboard."""
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rectangle.collidepoint(event.pos) == True:
                self.active = True
            else:
                self.active = False
            self.COLOR = self.COLOR_ACTIVATED if self.active == True else self.COLOR_INACTIVATED
        if event.type == pg.KEYDOWN:
            if self.active == True:
                if event.key == pg.K_RETURN:
                    self.active = False
                    self.COLOR = self.COLOR_INACTIVATED
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.displayed_text = self.FONT.render(self.text, True, self.TEXT_COLOR)
                else:
                    try:
                        int(event.unicode)
                        self.text += event.unicode
                        self.displayed_text = self.FONT.render(self.text, True, self.TEXT_COLOR)
                    except:
                        if event.unicode == ("." or "-"):
                            self.text += event.unicode
                            self.displayed_text = self.FONT.render(self.text, True, self.TEXT_COLOR)

    def draw(self):
        """This method uses the render parameter from the inputButton in order to draw both the rectangle
        for the container of the button as well as the text on the button."""
        pg.draw.rect(self.render.screen, self.COLOR, self.rectangle, 3)
        self.render.screen.blit(self.displayed_text, (self.rectangle.x + self.rectangle.w / 3, self.rectangle.y + self.rectangle.h / 4))

class CreateGrid:
    """Creates either a 2d or 3d grid by taking the type parameter. The other parameters are for the position
    of the button itself, render is to display it on the screen."""
    def __init__(self, render, x, y, type = 2):
        self.type = type
        dimension = ""
        if self.type == 2:
            dimension = "2d"
        elif self.type == 3:
            dimension = "3d"
        else:
            raise Exception("Enter valid dimensions")
        self.render = render
        self.text = f"Spawn {dimension} grid"
        self.FONT = pg.font.Font(None, 32)
        self.container = pg.Rect(x, y, 200, 40)
        self.lengthInput = InputButton(render, self.container.x + 10, self.container.y + 50, 40, 40, "5")
        self.gridList = []
        self.removeButtonList = []

    def eventHandler(self, event):
        """Calls the classes responsible for creating grid objects depending on specified type."""
        self.lengthInput.eventHandler(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.container.collidepoint(event.pos):
                    if self.type == 2:
                        self.gridList.append(Grid2d(self.render, int(self.lengthInput.text)))
                    else:
                        self.gridList.append(Grid3d(self.render, int(self.lengthInput.text)))

    def draw(self):
        """Draws button."""
        pg.draw.rect(self.render.screen, pg.Color("white"), self.container, 3)
        self.render.screen.blit(self.FONT.render(self.text, True, pg.Color("white")), (self.container.x + 10, self.container.y + 10))
        self.lengthInput.draw()

    def drawGrid(self):
        """Draws each grid-object in the gridList of the button."""
        if len(self.gridList) != 0:
            for grid in self.gridList:
                    grid.draw()
                    grid.animationHandler() 

class CreateVector:
    """This class is used to create objects of the VectorPackage class and keeps track of the current
        number of vectors. Only one such object is created and it also acts as the connection b/w the 
        users matrices and the vectors on the screen. It takes render for the same reason as the inputButton
        and the x and y parameters are for the position of the button itself."""

    def __init__(self, render, x, y):
        self.render = render
        self.text = "Spawn vector"
        self.FONT = pg.font.Font(None,32)
        self.container = pg.Rect(x, y, 170, 40)
        self.vectorList = []
    
    def eventHandler(self, event):
        """Much like the eventHandler for the inputButton, this method also takes the event parameter,
        but it is only used to register clicks on the button. Once clicked, a new VectorPackage object
        is created. This eventHandler also connects to the eventHandler for the VectorPackage objects 
        since no such objects will be initialized in the Render class in main.py."""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.container.collidepoint(event.pos):
                    self.vectorList.append(VectorPackage(self.render, 50, 500, f"V{len(self.vectorList)+1}"))
        if len(self.vectorList) != 0:
            for vectorPack in self.vectorList:
                vectorPack.eventHandler(event)

    def draw(self):
        """Draws both the CreateVector button as well as the related VectorPackage objects."""
        pg.draw.rect(self.render.screen, pg.Color("white"), self.container, 3)
        self.render.screen.blit(self.FONT.render(self.text, True, pg.Color("white")), (self.container.x + 10, self.container.y + 10))
        if len(self.vectorList) != 0:
            for vectorPack in self.vectorList:
                if vectorPack.remove == True:
                    self.vectorList.remove(vectorPack)
                else:
                    vectorPack.draw()

class VectorPackage:
    """This class creates VectorPackages which are combinations of 3d Vector-objects as well as
    the UI that allows the user to manipulate their values. The class takes a few parameters,
    render, x, y, and text. Render is to draw the object on the screen, x and y is for the 
    position where the UI for the vector is spawned, and the text is linked to the inputButtons
    which are used by the Vector UI. This class also handles animations relating to the 3d-object
    as well as the logic to move the Vector UI using drag and drop since the user might spawn
    a lot of VectorPackages."""
    def __init__(self, render, x, y, text = ""):
        self.render = render
        self.container = pg.Rect(x-10, y-10, 190, 160)
        self.exitBox = pg.Rect(x+self.container.w - 20, y-10, 10, 10)
        self.FONT = pg.font.Font(None, 32)
        self.COLOR = pg.Color("white")
        self.inputButtons = []
        self.active = False
        for i in range(3):
            self.inputButtons.append(InputButton(render, x, y+(i*50), 40, 40, "1"))
        self.confirmationButton = pg.Rect(x+60, y+50, 110, 40)
        self.text = text
        self.og_vector = [1, 1, 1, 1]
        self.goal_vector = [1, 1, 1, 1]
        self.animation_vector = [1, 1, 1, 1]
        self.delta_coord = [0, 0, 0]
        self.change = False
        self.count = 1
        self.remove = False

    def draw(self):
        """Draws the UI and the Vector"""
        pg.draw.rect(self.render.screen, self.COLOR, self.container, 3)
        for button in self.inputButtons:
            button.draw()
        pg.draw.rect(self.render.screen, pg.Color("red"), self.exitBox)
        pg.draw.rect(self.render.screen, self.COLOR, self.confirmationButton, 3)
        self.render.screen.blit(self.FONT.render("Change", True, self.COLOR), (self.confirmationButton.x + self.confirmationButton.w / 8, self.confirmationButton.y + self.confirmationButton.h / 4))
        self.render.screen.blit(self.FONT.render(self.text, True, pg.Color("red")), (self.container.x + 80, self.container.y + 15))
        self.vector = Vector(self.render, self.animation_vector)
        self.vector.translate([0.0001, 0.0001, 0.0001])
        self.vector.movement_flag = False
        self.vector.draw()
    
    def transformationHandler(self, matrix):
        """Takes the matrix from the transformationScreen as a parameter, transforms the vector
        according the transformation matrix and then calls the animation method in order to animate
        the change in 3d. This method is called by the transformation button which is separate
        from this class - since multiple objects need to be able to be transformed simultaneously."""
        tempVector = []
        for i in range(3):
            tempVector.append(self.og_vector[i])
        transformedVector = matrix@tempVector
        for i in range(3):
            self.goal_vector[i] = transformedVector[i]
            if self.og_vector[i] != self.goal_vector[i]:
                sign = -1 if self.og_vector[i] > self.goal_vector[i] else 1
                self.delta_coord[i] = sign*abs(self.og_vector[i] - (self.goal_vector[i]))
                self.change = True
        self.animate()
        for i in range(3):
            self.inputButtons[i].text = str(self.goal_vector[i])
            self.inputButtons[i].displayed_text = self.inputButtons[i].FONT.render(str(self.goal_vector[i]), True, pg.Color("white"))
        
    def eventHandler(self, event):
        """Takes the event parameter in order to register input into the inputButtons
        for the vector position, input from the mouse during drag and drop of the vector
        UI as well as input for when the user changes the values of the vector and confirms
        those changes with the confirmation button. It then passes those changes to the animation method."""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.exitBox.collidepoint(event.pos):
                    self.remove = True
                if self.container.collidepoint(event.pos):
                    self.active = True
                if self.confirmationButton.collidepoint(event.pos):
                    for i in range(3):
                        self.goal_vector[i] = float(self.inputButtons[i].text)
                        if self.og_vector[i] != self.goal_vector[i]:
                            sign = -1 if self.og_vector[i] > self.goal_vector[i] else 1
                            self.delta_coord[i] = sign*abs(self.og_vector[i] - (self.goal_vector[i]))
                            self.change = True
                    print("current " + str(self.og_vector))
                    print("change " + str(self.delta_coord))
                    print("end " + str(self.goal_vector))    
        if self.active == True:
            if event.type == pg.MOUSEMOTION:
                for button in self.inputButtons:
                    button.rectangle.move_ip(event.rel)
                self.container.move_ip(event.rel)
                self.confirmationButton.move_ip(event.rel)
                self.exitBox.move_ip(event.rel)
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.active = False
        for button in self.inputButtons:
            button.eventHandler(event)
    
    def animate(self):
        """This holds the logic for animating changes of the vector."""
        if self.change == True:
            for i in range(3):
                self.animation_vector[i] = self.animation_vector[i] + (1/60) * self.delta_coord[i]
            self.count += 1
            if self.count == 60:
                self.animation_vector = self.goal_vector[:]
                self.change = False
                self.count = 1
                self.delta_coord = [0, 0, 0]
                self.og_vector = self.animation_vector[:]
        
class NavigationButton:
    """This button is used to switch screens and are essentially just buttons
    with a boolean value which is checked in the screen-loops in main.py. 
    It takes a few parameters for the position of the button as well as the
    text and render in order to draw it."""
    def __init__(self, render, x, y, w, h, text = ""):
        self.render = render
        self.FONT = pg.font.Font(None, 32)
        self.rectangle = pg.Rect(x, y, w, h)
        self.text = text
        self.COLOR = pg.Color("white")
        self.displayed_text = self.FONT.render(self.text, True, self.COLOR)
        self.switch = False
    
    def eventHandler(self, event):
        """Takes event to check if the button is clicked, when clicked, switches a boolean value that breaks or switches loops in main.py."""
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rectangle.collidepoint(event.pos) == True:
                self.switch = True
    
    def draw(self):
        """Draws the button using render and the positions given."""
        pg.draw.rect(self.render.screen, self.COLOR, self.rectangle, 3)
        self.render.screen.blit(self.displayed_text, (self.rectangle.x + 10, self.rectangle.y + 10))

class InputMatrix:
    """This class creates inputMatrix objects which utilize the inputButton class in a grid format.
    The matrix UI is built using for loops and the parameters are only to specify the spawn location
    of the matrix as well as the name them."""
    def __init__(self, render, x, y, text = ""):
        self.container = pg.Rect(x-20, y-40, 180, 200)
        self.exitBox = pg.Rect(x+self.container.w - 30, y-40, 10, 10)
        self.remove = False
        self.buttonList = []
        self.render = render
        self.text = text
        self.FONT = pg.font.Font(None, 32)
        self.active = False
        for i in range(3):
            for j in range(3):
                self.buttonList.append(InputButton(render, x+(j*50), y+(i*50), 40, 40, "1"))
    
    def draw(self):
        """Draws the matrix according to the current position using render."""
        pg.draw.rect(self.render.screen, pg.Color("red"), self.exitBox)
        pg.draw.rect(self.render.screen, pg.Color("white"), self.container, 3)
        for button in self.buttonList:
            button.draw()
        self.render.screen.blit(self.FONT.render(self.text, True, pg.Color("red")), (self.container.x + 75, self.container.y + 10))
    
    def eventHandler(self, event):
        """Takes the event parameter and checks for input in the inputButtons of the matrix as well as
        whether the user is dragging the matrix to change its position. This is to allow the user to 
        freely order the matrices in the order of multiplication.""" 
        #Move matrix
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.exitBox.collidepoint(event.pos):
                    self.remove = True
                if self.container.collidepoint(event.pos):
                    self.active = True
        if self.active == True:
            if event.type == pg.MOUSEMOTION:
                for button in self.buttonList:
                    button.rectangle.move_ip(event.rel)
                self.container.move_ip(event.rel)
                self.exitBox.move_ip(event.rel)
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.active = False
        for button in self.buttonList: #Activate inputbuttons
            button.eventHandler(event)

class CreateMatrix:
    """Much like the createVector class, an object of this class is simply a button
    that spawns objects of the inputMatrix class. It takes the parameters render,
    x and y for draw the button on the screen."""
    def __init__(self, render, x, y):
        self.render = render
        self.text = "Spawn matrix"
        self.FONT = pg.font.Font(None, 32)
        self.container = pg.Rect(x, y, 170, 40)
        self.matrixList = []
    
    def eventHandler(self, event):
        """Checks for clicks on the button, creates objects of the inputMatrix class."""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.container.collidepoint(event.pos):
                    self.matrixList.append(InputMatrix(self.render, 400, 100, f"M{len(self.matrixList)+1}"))
        if len(self.matrixList) != 0:
            for matrix in self.matrixList:
                matrix.eventHandler(event)

    def draw(self):
        """Draws the button as well as the matrices it created."""
        pg.draw.rect(self.render.screen, pg.Color("white"), self.container, 3)
        self.render.screen.blit(self.FONT.render(self.text, True, pg.Color("white")), (self.container.x + 10, self.container.y + 10))
        if len(self.matrixList) != 0:
            for matrix in self.matrixList:
                if matrix.remove == True:
                    self.matrixList.remove(matrix)
                else:
                    matrix.draw()
        
class TransformButton:
    """Takes parameters in order to draw the button. This button will construct the correct matrix and
    apply the transformation on the objects listed."""
    def __init__(self, render, x, y):
        self.render = render
        self.container = pg.Rect(x, y, 200, 40)
        self.text = "Transform"
        self.FONT = pg.font.Font(None, 32)
        self.COLOR = pg.Color("white")
        self.matrices = []        

    def eventHandler(self, event, objectLists = []):
        """Takes event to register clicks on the transformation button. Also takes objectLists
        as a parameter which is a list of the lists of objects which are to be transformed. 
        This is because each button that creates a vector for example will hold a list of different 
        vectors so in order to generalize the transformation across all objects in the 3d space,
        a list of lists is taken as a parameter in order to access the transformationHandler
        of each 3d object and pass the correct matrix to that handler."""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.container.collidepoint(event.pos):
                    """Get the objects to be transformed"""
                    objects = []
                    for oList in objectLists:
                        for o in oList:
                            objects.append(o)
                    if objects != []:
                        """This part sorts the matrices according to their x-position on the transformation-screen."""
                        mSorted = []
                        mReady = []
                        if self.matrices != []:
                            for matrix in self.matrices:
                                if len(mSorted) == 0:
                                    mSorted.append(matrix)
                                else:
                                    for each in mSorted:
                                        inserted = False
                                        if matrix.container.x < each.container.x:
                                            mSorted.insert(mSorted.index(each), matrix)
                                            inserted = True
                                            break
                                    if inserted == False:
                                        mSorted.append(matrix)
                            mSorted.reverse()
                            """This part formats the matrices into the correct format for multiplication."""
                            for matrix in mSorted:
                                formatted = []
                                for i in range(3):
                                    row = []
                                    for j in range(3):
                                        row.append(float(matrix.buttonList[i*3 + j].text))
                                    formatted.append(row)
                                formatted = np.array(formatted)
                                mReady.append(formatted)
                            """This part multiplies into a singular matrix"""
                            for i in range(len(mReady)):
                                if i != len(mReady) - 1:
                                    mReady[i+1] = mReady[i+1]@mReady[i]
                                else:
                                    result = mReady[i]
                            for o in objects:
                                o.transformationHandler(result)
                        else:
                            print("No matrices")
                    else:
                        print("No objects to transform")

    def draw(self):
        """Draws the button and its corresponding text."""
        pg.draw.rect(self.render.screen, self.COLOR, self.container, 3)
        self.render.screen.blit(self.FONT.render(self.text, True, self.COLOR), (self.container.x + 10, self.container.y + 10))
