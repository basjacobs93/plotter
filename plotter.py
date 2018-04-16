import serial
import time
import numpy as np

class Plotter():

	def __init__(self, port, baud, speed):
		self.s = serial.Serial(port, baud)
		self.speed = speed
		self.initialize()

	def send_command(self, cmd):
	    l = cmd.strip()
	    print l
	    self.s.write(cmd + "\n")
	    grbl_out = self.s.readline() # Wait for grbl response with carriage return
	    print '> ' + grbl_out.strip()

	def in_range(self, x, y):
	    return ((0 <= x <= 240) and (0 <= y <= 170))
	    
	def move(self, x, y):
	    if self.in_range(x, y):
	        self.send_command("G01 X{} Y{}".format(-x, y))
	    else:
	        print("{}, {} not in range".format(x, y))
	    
	def move_quick(self, x, y):
	    if self.in_range(x, y):
	        self.send_command("G00 X{} Y{}".format(-x, y))
	    else:
	        print("{}, {} not in range".format(x, y))
	    
	def set_speed(self, speed):
	    # in mm/sec
	    self.send_command("F{}".format(speed))
	    
	def pen_down(self):
	    self.send_command("S1000 M3")
	    
	def pen_up(self):
	    self.send_command("S0 M5")
	    
	def set_unit(self):
	    self.send_command("G21")    # set units in millimeters
	    
	def draw_line(self, x1, y1, x2, y2):
	    self.move(x1, y1)
	    self.pen_down()
	    self.move(x2, y2)
	    self.pen_up()
	    
	def arc(self, x, y, i, j, cw = True):
	    if cw:
	        c = "3"
	    else:
	        c = "2"
	    self.send_command("G0{} X{} Y{} I{} J{}".format(c, -x, y, -i, j))
	    
	def draw_circle(self, x, y, r):
	    if self.in_range(x-r, y-r) and self.in_range(x+r, y+r):
	        self.move(x-r/2., y-r/2.)
	        self.pen_down()
	        self.arc(x-r/2., y-r/2., r/2., r/2.)
	        self.pen_up()
	    else:
	        print("circle {},{},{} not in range".format(x, y, r))

	def stop(self):
		self.pen_up()
		self.move_quick(0, 0)
		time.sleep(5)
		self.s.close()
	        
	def initialize(self):
	    # Wake up grbl
	    self.s.write("\r\n\r\n")
	    time.sleep(5)   # Wait for grbl to initialize
	    self.s.flushInput()  # Flush startup text in serial input

	    self.set_unit()
	    self.set_speed(self.speed)