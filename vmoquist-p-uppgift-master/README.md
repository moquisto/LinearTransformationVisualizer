# Specifikation

## Inledning
Projektet är ett grafiskt hjälpmedel för att visualisera linjära transformationer i 3d likt animationerna i 3blue1browns videoserie om linjär algebra (https://www.youtube.com/watch?v=rHLEWRxRGiM&list=PL0-GT3co4r2y2YErbmuJw2L5tW4Ew2O5B&index=6). Programmet är helt grafiskt både i simulering av transformationerna och UI och bygger på att användaren ska ha frihet att experimentera själv för att få en mer intuitiv förståelse av linjär algebra. Några av dem viktigaste funktionerna av programmet är därför att användaren ska kunna bygga egna matriser, välja vektorer fritt och även kunna välja några andra meshar så som rutnät i 2d och 3d.

Eftersom mycket av tekniken för att skapa visualisera 3d på en skärm redan är standardiserat (moduler som openGL och vPython finns + mycket material finns online) så kommer det svåraste med det här projektet vara att integrera ett grafiskt användargränsnitt som effektivt kommunicerar det användaren vill göra till ett språk som fungerar för 3d-grafik.

## Användarscenarier
En person som studerar linjär algebra vill få en mer intuitiv geometrisk förståelse för linjära transformationer. Personen startar programmet och skapar en vektor i det tredimensionella rummet. Sen byter personen till transformationsmenyn där hen väljer någon/några matriser att experimentera med. När personen är nöjd byter hen tillbaka till skärmen med vektor-objektet och testar att transformera vektorn med transformationsknappen. Använderan testar att skapa några nya objekt i rummet, testar några andra matriser och får sen en mer intuitiv förståelse om hur linjära transformationer kan se ut geometriskt.

En person har ett matteproblem som består av att räkna ut var en vektor landar efter ett flertal linjära transformationer. Personen skapar en vektor på original-positionen och matar sedan in matriserna som representerar transformationerna. Personen klickar sedan tillbaka till skärmen med vektorn och klickar på transformationsknappen för att se var vektor landar.

## Programskelett
Programmet består av flera filer för att organisera det bättre.
### main.py
main.py är filen som körs för att starta programmet. Den initialiserar objekten som kommer användas samt bestämmer några grundläggande värden som behövs för det grafiska användargränssnittet (upplösning, fps). Det innehåller även logiken för att byta skärmar och kallar även vissa metoder på objekten som skapades.


    class Application:
    """An object of this class is created when running main.py - this is calls all other files in this project, ie this is an instance of the program itself.""" 
        def __init__(self):
        """Decides constant values for things necessary for the display like resolution and FPS."""

        def create_objects(self):
        """Creates objects that will be used later on by the other methods. Objects are created by importing classes from other files."""

        def draw_main(self):
        """This method decides the values for the pixels on the main screen before they are "flipped" and thus rendered on the display by main()."""

        def main(self):
        """This method holds the logic for the functions of the main screen. This includes calling eventHandler() methods on some of the initialized objects as well as handling screen-changes. This method calls draw_main() and is also the method that is called when running the program."""

        def draw_transform(self):
        """Much like draw_main() but for the transformation-screen (where the user decides what transformation should be used."""

        def transformationScreen(self):
        """Similar to the main screen but doesn't display anything other than UI tools."""

        def draw_presets(self):
        """Similar to draw_transform() but for the presets-screen."""

        def presetsScreen(self):
        """Similar to the transformation-screen in that doesn't display any 3d animations and only UI tools. Might be integrated into the transformation-screen since they have similar functions."""


### components.py
Den här filen innehåller i alla klasser för UI.


    class InputButton:
        def __init__(self, render, x, y, w, h, text = ""):
        """Class that creates button-objects which the user can click and assert values to. This is later used when the user inputs values to matrices and vectors. The class takes a few parameters relating to the dimensions of the rectangular box which will be drawn, render - which is needed to later draw the button on the screen as well as the text value which defaulted to an empty string unless called with the text parameter."""


        def eventHandler(self, event):
        """This method handles the logic of the inputButton. It takes the event parameter which comes from pg.event in order to determine whether the user clicked on the button or not as well as to confirm user input from the keyboard."""


        def draw(self):
        """This method uses the render parameter from the inputButton in order to draw both the rectangle for the container of the button as well as the text on the button."""


    class CreateVector:
        def __init__(self, render, x, y):
        """This class is used to create objects of the VectorPackage class and keeps track of the current number of vectors. Only one such object is created and it also acts as the connection b/w the users matrices and the vectors on the screen. It takes render for the same reason as the inputButton and the x and y parameters are for the position of the button itself."""


        def eventHandler(self, event):
        """Much like the eventHandler for the inputButton, this method also takes the event parameter, but it is only used to register clicks on the button. Once clicked, a new VectorPackage object is created. This eventHandler also connects to the eventHandler for the VectorPackage objects since no such objects will be initialized in the Render class in main.py."""
        


        def draw(self):
        """Draws both the CreateVector button as well as the related VectorPackage objects."""



    class VectorPackage:
        def __init__(self, render, x, y, text = ""):
        """This class creates VectorPackages which are combinations of 3d Vector-objects as well as the UI that allows the user to manipulate their values. The class takes a few parameters, render, x, y, and text. Render is to draw the object on the screen, x and y is for the position where the UI for the vector is spawned, and the text is linked to the inputButtons which are used by the Vector UI. This class also handles animations relating to the 3d-object as well as the logic to move the Vector UI using drag and drop since the user might spawn a lot of VectorPackages."""


        def draw(self):
        """Draws the UI and the Vector"""


        def transformationHandler(self, matrix):
        """Takes the matrix from the transformationScreen as a parameter, transforms the vector according the transformation matrix and then calls the animation method in order to animate the change in 3d. This method is called by the transformation button which is separate from this class - since multiple objects need to be able to be transformed simultaneously."""


        def eventHandler(self, event):
        """Takes the event parameter in order to register input into the inputButtons for the vector position, input from the mouse during drag and drop of the vector UI as well as input for when the user changes the values of the vector and confirms those changes with the confirmation button. It then passes those changes to the animation method."""


        def animate(self):
        """This holds the logic for animating changes of the vector."""


    class navigationButton:
        def __init__(self, render, x, y, w, h, text = ""):
        """This button is used to switch screens and are essentially just buttons with a boolean value which is checked in the screen-loops in main.py. It takes a few parameters for the position of the button as well as the text and render in order to draw it."""

        def eventHandler(self, event):
        """Takes event to check if the button is clicked, when clicked, switches a boolean value that breaks or switches loops in main.py."""

        def draw(self):
        """Draws the button using render and the positions given."""


    class InputMatrix:
        def __init__(self, render, x, y, text = ""):
        """This class creates inputMatrix objects which utilize the inputButton class in a grid format. The matrix UI is built using for loops and the parameters are only to specify the spawn location of the matrix as well as the name them."""


        def draw(self):
        """Draws the matrix according to the current position using render."""


        def eventHandler(self, event):
        """Takes the event parameter and checks for input in the inputButtons of the matrix as well as whether the user is dragging the matrix to change its position. This is to allow the user to freely order the matrices in the order of multiplication.""" 


    class CreateMatrix:
        def __init__(self, render, x, y):
        """Much like the createVector class, an object of this class is simply a button that spawns objects of the inputMatrix class. It takes the parameters render, x and y for draw the button on the screen."""
        
        def eventHandler(self, event):
        """Checks for clicks on the button, creates objects of the inputMatrix class."""
        

        def draw(self):
        """Draws the button as well as the matrices it created."""



    class TransformButton:
        def __init__(self, render, x, y):
        """Takes parameters in order to draw the button. This button will construct the correct matrix and apply the transformation on the objects listed."""
        
        def eventHandler(self, event, objectLists = []):
        """Takes event to register clicks on the transformation button. Also takes objectLists as a parameter which is a list of the lists of objects which are to be transformed. This is because each button that creates a vector for example will hold a list of different vectors so in order to generalize the transformation across all objects in the 3d space, a list of lists is taken as a parameter in order to access the transformationHandler of each 3d object and pass the correct matrix to that handler."""

        def draw(self):
        """Draws the button and its corresponding text."""
        
        
    """classes and methods for objects other than vectors are yet to be created."""
    
### matrices.py
Den här filen innehåller matriser nödvändiga för att manipulera 3d-objekt.

    def translate(pos):
    """This matrix translates 3d-objekts in 3d-space using a 4x4 matrix (homogeneous coordinates for the projective plane). The functions takes the parameter for pos for position to translate to."""

    def rotate_x(a):
    """Rotates around the x-axis with an angle a."""

    def rotate_y(a):
    """Rotates around the y-axis with an angle a."""

    def scale(n):
    """Scales with a factor n."""
    
    
### projection.py
Den här filen innehåller projektionsmatriser för att föra över 3d-objekt till en 2d skärm sådant att perspektivet behålls.

    class Projection:
        def __init__(self, render):
        """Takes display as a parameter in order to access values of objects created in the object of the Application class.
    These values are for the near and far plane of the view-frustum as well as the angles of the frustum. 
    They are then used to create projection matrices that ultimately are used to convert 3d objects
    onto a 2d viewing plane, ie the screen."""


### objects.py
Den här filen innehåller klasser för 3d-objekt och använder funktionerna från matrices.py.

    class Object3D:
        def __init__(self, render):
        """This class creates some values which are used for all 3d objects as well as includes the method which uses the matrices from the projection.py class in order to map 3d objects onto the screen."""

        def draw(self):
        """Uses matrices to change the coordinates of the verteces into camera space and then from camera-space to clip space and then finally to the 2d screen using another matrix which takes the coordinates of the verteces of each 3d object and maps them to the display according to the screen resolution."""
        
        def translate(self, pos):
        """Calls the corresponding function from the matrices.py file on the verteces of the object in order to change each vertex accordingly."""

        def scale(self, scale_to):
        """Calls the corresponding function from the matrices.py file on the verteces of the object in order to change each vertex accordingly."""

        def rotate_x(self, angle):
        """Calls the corresponding function from the matrices.py file on the verteces of the object in order to change each vertex accordingly."""

        def rotate_y(self, angle):
        """Calls the corresponding function from the matrices.py file on the verteces of the object in order to change each vertex accordingly."""

        def rotate_z(self, angle):
        """Calls the corresponding function from the matrices.py file on the verteces of the object in order to change each vertex accordingly."""

    class Axes(Object3D):
        def __init__(self, render):
            super().__init__(render)
         """ Inherits from the Oject3D class and creates a 3d object corresponding to the x, y and z axes.This is done by simply deciding the correct verteces for the axes and then coloring and labeling them to differentiate b/w the different axes."""

    class Vector(Object3D):
        def __init__(self, render, vector):
        """Uses similar logic as the Axes class. Since these values are subject to change due to the associated VectorPackage class that calls this method, the verteces are given by the vector parameter which is a list of the verteces. During transformations, what happens is essentially that this vector list changes. This means that these 3D objects are called repeadetly for each loop in main.py."""
       
    class grid2d(object3D):
        def __init__(self, render, transformation):
        """These are yet to be added but will likely use similar logic as the vector objects. Most likely this object will be constructed using loops that create a grid like structure, much like how loops were used to create grid-like matrices on the transformation-screen. The transformation parameter will change the structure. A UI tool will probably be created for this as well and put on the presets screen."""
    
    class grid3d(object3D):
        def __init__(self, render, transformation):
        """Same as for grid2d."""
    
    """Might add more 3d objects."""

        
### viewer.py

    class Viewer:
        def __init__(self, render, position):
        """This class creates a Viewer/camera object which views the 3d transformations. The viewer class takes
        a position parameter which is the relative position to the coordinate system. This position parameter
        is then changed by the controls method which allows the user to move the camera around in order to view
        things from other perspectives. Display is used to access things such as the resolution of the screen."""

        def controls(self):
        """Checks for user input on the keyboard in order to move the perspective. Movement is done by calling the following methods."""

        def camera_yaw(self, angle):
        """Rotates camera left and right according to the angle specified by the user input from controls using the rotation matrix below."""

        def camera_pitch(self, angle):
        """Rotates camera up and down like the camera_yaw method."""

        def viewTranslationMatrix(self):
        """Takes the position specified by the camera and constructs a translation matrix which will later be applied on the objects in the rendered space in order to give off the illusion of the camera moving (camera is actually stationary, it is the world that moves around it.)"""

        def viewRotationMatrix(self):
        """Like the translation matrix but for rotation"""

        def viewMatrix(self):
        """Combines both translation and rotation to create a new matrix which will be applied on the verteces of the 3d objects."""

## Minne
Eftersom programmet är så pass stort så kan diagrammet inte göra det rättvisa utan att bli massivt, använd det därför endast för att följa med den här korta förklaringen:

När main.py körs skapas ett objekt av Render klassen som i sin tur skapar många andra objekt av klasser som importeras från andra filer. När programmet körs så kan användaren genom objekten som skapades i början skapa flera objekt så som vektorer och matriser, alltså är det objekt i UI:n som pekar på ett flertal andra objekt av t.ex klassen VectorPackage. Tills användaren tar bort dessa så lagras de i minnet. Varenda en av dessa skapar i varje loop ett 3d-objekt som målas i loopen och sedan skickas till garbage collectorn. Alltså finns 3d-objekten inte permanent i minnet utan skapas och förstörs i varje loop. 
(https://gits-15.sys.kth.se/gruprogf23/vmoquist-p-uppgift/blob/master/IMG_20231130_162400__01.jpg)
