"""
Turtle Graphics - This is a common project where you create a floor of 20 x 20 squares. Using various
commands you tell a turtle to draw a line on the floor. You have move forward, left or right,
lift or drop pen etc. Do a search online for "Turtle Graphics" for more information.
Optional: Allow the program to read in the list of commands from a file.
"""
import Tkinter
import sys

import Image
import ImageTk
import ImageDraw


class TurtleWorld(object):
    def __init__(self, size, bg_color):
        """
        Class constructor

        size:       Image  - The dimension (width, height) of the world
        bg_color:   String - Color for the world background
        """
        self.size = size
        self.space = Image.new("RGB", self.size, bg_color)
        self.window = Tkinter.Tk()  # Create new OS window
        self.window.geometry('%dx%d' % (self.size[0], self.size[1]))
        self.label = None

    def process(self):
        """
        Configure a label and add it to the window
        """
        # Create image TK instance
        image = ImageTk.PhotoImage(self.space)

        # Remove existing label
        if self.label is not None:
            self.label.destroy()

        # Create a new label and add the image to it
        self.label = Tkinter.Label(self.window, image=image)
        self.label.configure(image=image)
        self.label.image = image
        self.label.pack(side="bottom", fill="both", expand="yes")

    def show(self):
        """
        Display the OS window
        """
        self.process()
        self.window.mainloop()  # Start the GUI

    def show_image(self):
        """
        Display the image only
        """
        self.space.show()


class Turtle(object):
    def __init__(self, world, color='black', width=1):
        """
        Class constructor

        world:   Image  - An Image object
        color:   String - Color for the turtle path
        width:   Integer- The width of the turtle path
        """
        self.color = color
        self.is_pen_down = True  # Draw when move
        self.world = world
        self.draw = ImageDraw.Draw(self.world.space)  # An instance of the drawer
        self.position = (world.size[0] / 2, world.size[1] / 2)  # Starting point in the center of the world
        self.width = width

    def set_position(self, x, y):
        """
        Set the current position

        x:  Integer - x coordinate
        y:  Integer - y coordinate
        """
        self.position = (x, y)

    def _position(self, x, y):
        """
        Calculate the current path and change the current position

        x:  Integer - x coordinate
        y:  Integer - y coordinate
        returns: Tuple - The new path to draw
        """
        new_position = (self.position[0], self.position[1], self.position[0] + x, self.position[1] + y)
        self.set_position(new_position[2], new_position[3])
        return new_position

    def move_to(self, x=0, y=0, width=None, color=None):
        """
        Move the turtle

        x:      Integer - x coordinate
        y:      Integer - y coordinate
        width:  Integer - A specific width for the current path only
        color:  String  - A specific color for the current path only
        """
        xy = self._position(x, y)
        if self.is_pen_down:
            steps_color = color if color is not None else self.color
            steps_width = width if width is not None else self.width
            self.draw.line(xy=xy, fill=steps_color, width=steps_width)

    def forward(self, y=0, x=0, width=None, color=None):
        """
        Move the turtle forward - North of the image

        x:      Integer - x coordinate
        y:      Integer - y coordinate
        width:  Integer - A specific width for the current path only
        color:  String  - A specific color for the current path only
        """
        return self.move_to(x, -y, width, color)

    def right(self, x=0, y=0, width=None, color=None):
        """
        Move the turtle to the east of the image

        x:      Integer - x coordinate
        y:      Integer - y coordinate
        width:  Integer - A specific width for the current path only
        color:  String  - A specific color for the current path only
        """
        return self.move_to(x, y, width, color)

    def left(self, x=0, y=0, width=None, color=None):
        """
        Move the turtle to the west of the image

        x:      Integer - x coordinate
        y:      Integer - y coordinate
        width:  Integer - A specific width for the current path only
        color:  String  - A specific color for the current path only
        """
        return self.move_to(-x, y, width, color)

    def down(self, y=0, x=0, width=None, color=None):
        """
        Move the turtle to the south of the image

        x:      Integer - x coordinate
        y:      Integer - y coordinate
        width:  Integer - A specific width for the current path only
        color:  String  - A specific color for the current path only
        """
        return self.move_to(x, y, width, color)

    def circle(self, radius=0, fill=None, xy=None):
        """
        Create a circle path

        radius: Integer - The circle radius
        fill:   String  - The color to fill the image with
        xy:     Tuple   - A specific coordinates to draw the circle. This ignores the radius parameter
        """
        if self.is_pen_down:
            # If specific position defined then it must be 4 items
            if xy is not None and len(xy) < 4:
                raise TypeError("Coordinate list must contain exactly 2 coordinates")

            # Center the circle around the current point
            if xy is None:
                xy = (self.position[0] - radius, self.position[1] - radius, self.position[0] + radius,
                      self.position[1] + radius)

            # Draw circle
            self.draw.ellipse(xy, outline=self.color, fill=fill)

    def rectangle(self, size=None, fill=None, xy=None):
        """
        Create a rectangle path

        size:   Integer - The rectangle dimension (width, height)
        fill:   String  - The color to fill the image with
        xy:     Tuple   - A specific coordinates to draw the circle. This ignores the radius parameter
        """
        if self.is_pen_down:
            # Rectangle with same dimension sizes
            if isinstance(size, int):
                size = (size, size)

            # If x,y defined, then there must be 4 items in the parameters
            if xy is not None and len(xy) < 4:
                raise TypeError("Coordinate list must contain exactly 2 coordinates")

            # If size parameter is invalid
            elif size is None or size is not None and len(size) < 2:
                raise TypeError("size parameter must contains 2 items for the (width, height)")

            # Center the rectangle around the current point
            if xy is None:
                xy = (self.position[0] - size[0] / 2, self.position[1] - size[1] / 2, self.position[0] + size[0] / 2,
                      self.position[1] + size[1] / 2)

            # Draw rectangle
            self.draw.rectangle(xy, outline=self.color, fill=fill)

    def pen_down(self):
        """
        Pull the pen down - drawing when moving
        """
        self.is_pen_down = True

    def pen_up(self):
        """
        Pull the pen up - no drawing when moving.
        """
        self.is_pen_down = False


class TurtleCommandReader(object):
    def __init__(self, file_path):
        """
        Class constructor

        file_path:  String - Full path to the file containing the commands
        """
        self.file_path = file_path
        self.commands = []  # List of commands
        self.world = None   # Instance of TurtleWorld
        self.turtle = None  # Instance of Turtle

    def load_commands(self):
        """
        Load commands from the file
        """
        file_object = open(self.file_path, 'r')
        self.commands = file_object.readlines()
        file_object.close()

    @staticmethod
    def fetch_command(command):
        """
        Convert string command into items in a list

        command: String - Command string extracted from the file
        returns: List   - List with 2 items the method name and then sub-list containing the method arguments
        """
        # Separate the method name from the arguments
        command = map(lambda x: x.strip(), command.split(':'))

        # Convert the arguments string into a list with the correct dataType for each item
        if command[1] == '':
            command[1] = []
        else:
            command[1] = command[1].split(',')
            for i, arg in enumerate(command[1]):
                arg = arg.strip()
                if arg == 'None':
                    # Word None equal to None dataType
                    command[1][i] = None
                else:
                    # Allow for negative/positive number, else it's string
                    try:
                        command[1][i] = int(arg)
                    except ValueError:
                        command[1][i] = arg

        return command

    def init_objects(self, command, index):
        """
        Initiate the TurtleWorld & Turtle objects

        command: String  - Command string extracted from the file
        index:   Integer - The index number of the line in the file
        """
        if index == 0:
            bg_color = command.pop(2)
            size = command[:2]
            self.world = TurtleWorld(size, bg_color)
        elif index == 1:
            self.turtle = Turtle(self.world, command[0], int(command[1]))

    def execute_command(self, method, args):
        """
        Execute a turtle command if valid

        method: String - The method name in Turtle object
        args:   List   - The method arguments
        """
        if method in dir(self.turtle):
            getattr(self.turtle, method)(*args)

    def start(self):
        """
        Start reading the file and draw the turtle commands
        """
        # Load commands from a file
        self.load_commands()

        # Process each line in the file
        for index, line in enumerate(self.commands):
            command, args = self.fetch_command(line)
            if index < 2:
                self.init_objects(args, index)
            else:
                self.execute_command(command, args)

        # Show the image
        self.world.show()


# Start the program
if __name__ == '__main__':
    example = '0' if len(sys.argv) == 1 else sys.argv[1]

    # Hard coded turtle path
    if example == '1':
        world = TurtleWorld((300, 300), 'white')

        turtle = Turtle(world)
        turtle.pen_down()
        turtle.forward(100)
        turtle.right(100, width=3)
        turtle.left(200)
        turtle.circle(50)
        turtle.pen_up()
        turtle.move_to(100, 100)
        turtle.pen_down()
        turtle.rectangle(size=(10, 100))

        world.show()

    else:
        # Draw turtle path from a file
        TurtleCommandReader('./turtle_commands.txt').start()
