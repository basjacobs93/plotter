import serial
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Plotter():
	def __init__(self, port, width = 170, height = 240):
		self.port = port
		self.baud = 115200
		self.location = (0, 0) # x, y
		self.pen_state = 0 # 0=up, 1=down
		self.speed = 0

		self.width = width
		self.height = height

	def wake_up(self):
		# Open grbl serial port
		self.serial = serial.Serial(port, baud)

	    # Wake up grbl
	    self.serial.write(b"\r\n\r\n")
	    time.sleep(3)   # Wait for grbl to initialize 
	    self.serial.flushInput()  # Flush startup text in serial input

	    # Configure
	    self.set_unit()   # units = mm
	    self.set_speed(5000) # feed rate
	    self.pen_trigger() # pen slightly down
	    self.pen_up() # pen up


    def shut_down(self):
    	self.pen_up() # pen up
		self.go_home() # go home
		time.sleep(3)   # wait for everything to finish 
		# close serial port
		self.serial.close()

	def execute(self, instruction):
		instruction += "\n"
		logger.debug('Sending: ' + instruction,)
        self.serial.write(l.encode('utf-8')) # Send g-code block to grbl
        response = self.serial.readline().strip() # Wait for grbl response with carriage return
        logger.debug(response)


    # Basic instructions
	def move(self, x, y):
		# TODO: test bounds
		self.execute("G01 X{} Y{}".format(round(-x, 5), round(y, 5)))
		self.location = (x,y)

	def move_quick(self, x, y):
	    self.execute("G00 X{} Y{}".format(round(-x, 5), round(y, 5)))
	    self.location = (x,y)
	    
	def set_speed(self, speed):
		self.execute("F{}".format(speed))
		self.speed = speed
	    
	def pen_down(self):
	    self.execute("S1000 M3")
	    self.pen_state = 1

	def pen_trigger(self):
		self.execute("S0 M3")
		self.pen_state = 0.5
	    
	def pen_up(self):
	    self.execute("S0 M5")
	    self.pen_state = 0
	    
	def set_unit(self):
		# set units in millimeters
	    self.execute("G21")
	
	def go_home(self):
		self.move_quick(0, 0)


	# Shapes
    def arc(self, x1, y1, x2, y2, i, j, cw = True, radius, extent):
		# Draw (cw = clockwise) arc from (x1,y1) to (x2,y2) with center at (i,j)
		if (x1, y1) != self.location:
			self.point(x1, y1)
	    if cw:
	        c = "2"
	    else:
	        c = "3"
	    self.execute("G0{} X{} Y{} I{} J{}".format(c, round(-x2, 5), round(y2, 5), round(-i, 5), round(j, 5)))

	def line(self, x1, y1, x2, y2):
		if (x1, y1) != self.location:
			self.point(x1, y1)
		self.move(x2, y2)

	def point(self, x, y):
		self.pen_up()
		self.move(x, y)
		self.pen_down()


	# Drawing functionality
	def draw(self):
		pass
