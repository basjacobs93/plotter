import turtle
import logging
from math import pi

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Canvas():
    def __init__(self, width = 170, height = 240):
        self.canvas = turtle.Screen()

        self.canvas = self.canvas.setup(width=width, height=height, startx=0, starty=-0)

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        self.width = width
        self.height = height


    # Shapes
    def arc(self, x1, y1, x2, y2, i, j, cw, radius, extent):
        # Draw (cw = clockwise) arc from (x1,y1) to (x2,y2) with center at (i,j)
        if turtle.position() != (x1, y1):
            self.point(x1, y1)

        # The center is radius units left of the turtle;
        #  extent – an angle – determines which part of the circle is drawn.
        angle_to_center = turtle.towards(i+x1, j+y1)
        # Center left of turtle
        turtle.left(angle_to_center-90)
        turtle.circle(radius, extent/(2*pi) * 360) # extent is in radians

    def line(self, x1, y1, x2, y2):
        if turtle.position() != (x1, y1):
            self.point(x1, y1)
        turtle.goto(x2, y2)

    def point(self, x, y):
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()


    # Drawing functionality
    def draw(self, objs):
        for obj in objs:
            obj.draw(self, black)

        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    return
            pygame.display.update()


canvas = Canvas()

canvas.line(10, 10, 30, 50)

canvas.arc(10, 10, 30, 50, 20, 40, cw = True, radius = 10, extent = pi)

turtle.done()

