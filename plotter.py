def move(x, y):
	return "G01 X{} Y{}".format(round(-x, 5), round(y, 5))
    
def move_quick(x, y):
    return "G00 X{} Y{}".format(round(-x, 5), round(y, 5))
    
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
        c = "2"
    else:
        c = "3"
    return "G0{} X{} Y{} I{} J{}".format(c, round(-x, 5), round(y, 5), round(-i, 5), round(j, 5))