import pygame

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Canvas():
	def __init__(self, width = 170, height = 240):
		pygame.init()

	    self.canvas = pygame.display.set_mode((height,width),0,32)

	    self.white = (255, 255, 255)
	    self.black = (0, 0, 0)

	    self.canvas.fill(white)

	    self.height = height


	# Shapes
	def arc(self, x, y, i, j, cw = True):
		# TODO
		pass

	def line(self, x1, y1, x2, y2):
		pygame.draw.line(self.canvas, self.black, (x1, self.height-y1), (x2, self.height-y2))

	def point(self, x, y):
		pygame.draw.rect(self.canvas, self.black, (self.x, self.height-self.y, 1, 1))


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

