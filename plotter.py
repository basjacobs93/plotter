def move(x, y):
	return "G01 X{} Y{}".format(-x, y)
    
def move_quick(x, y):
    return "G00 X{} Y{}".format(-x, y)
    
def set_speed(speed):
	return "F{}".format(speed)
    
def pen_down():
    return "S1000 M3"
    
def pen_up():
    return "S0 M5"
    
def set_unit():
    return "G21"    # set units in millimeters
    
def arc(x, y, i, j, cw = True):
    if cw:
        c = "3"
    else:
        c = "2"
    return "G0{} X{} Y{} I{} J{}".format(c, -x, y, -i, j)