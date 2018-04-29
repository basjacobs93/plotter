import numpy as np
import math
import plotter as plt
import pygame

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def dist(self, p2):
        return math.sqrt((self.x-p2.x)**2 + (self.y-p2.y)**2)
    
    def minus(self, p2):
        return Point(self.x-p2.x, self.y-p2.y)
    
    def plus(self, p2):
        return Point(self.x+p2.x, self.y+p2.y)
    
    def times(self, n):
        return Point(self.x*n, self.y*n)
    
    def draw(self, canvas, color):
        pygame.draw.rect(canvas, color, (self.x, canvas.get_height()-self.y, 1, 1))
        
    def plot_instructions(self):
        return [plt.pen_up(), plt.move(self.x, self.y), plt.pen_down()]


class Line():
    # a line is defined by 2 points
    def __init__(self, point1, point2):
        self.P1 = point1
        self.P2 = point2
        
    def intersect(self, line2):
        # calculates the intersection point of the lines
        # solution is based on simple algebra
        a = self.P1.x - self.P2.x
        b = self.P1.y - self.P2.y

        u = (a*(line2.P2.y-self.P2.y) - b*(line2.P2.x-self.P2.x)) / (a*(line2.P2.y-line2.P1.y) - b*(line2.P2.x-line2.P1.x))

        return (line2.P1.times(u)).plus(line2.P2.times(1-u))
    
    def perpendicular_at(self, P):
        U = Point(self.P2.y-self.P1.y, self.P1.x - self.P2.x)
        return Line(P, P.plus(U))
    
    def draw(self, canvas, color):
        pygame.draw.line(canvas, color, (self.P1.x, canvas.get_height()-self.P1.y), (self.P2.x, canvas.get_height()-self.P2.y))
        
    def plot_instructions(self):
        # assumes we are at P1
        return [plt.move(self.P2.x, self.P2.y)]


class CircleArc(): 
    # Circle arc between P1 and P2 with center at C
    # clockwise if cw = True
    def __init__(self, P1, P2, C, cw):
        self.P1 = P1
        self.P2 = P2
        self.C = C
        self.cw = cw
        self.r = self.radius()
        self.startAngle = self.start_angle()
        self.endAngle = self.end_angle()
        self.sweepAngle = self.sweep_angle()
        
    def draw(self, canvas, color):
        t = 0.
        while t <= 1.:
            self.point_at(t).draw(canvas, color)
            t += 0.001
    
    def sweep_angle(self):
        sw = self.endAngle - self.startAngle
        if (sw < 0) and self.cw:
            sw += 2 * math.pi
        elif (sw > 0) and (not self.cw):
            sw -= 2 * math.pi
        return sw
    
    def start_angle(self):
        return math.atan2(self.P1.y-self.C.y, self.P1.x-self.C.x)
    
    def end_angle(self):
        return math.atan2(self.P2.y-self.C.y, self.P2.x-self.C.x)
    
    def radius(self):
        return self.P1.dist(self.C)
    
    def point_at(self, t):
        x = self.C.x + self.r * math.cos(self.startAngle + t * self.sweepAngle);
        y = self.C.y + self.r * math.sin(self.startAngle + t * self.sweepAngle);
        return Point(x, y)
    
    def plot_instructions(self):
        # assumes we are at P1
        relC = self.C.minus(self.P1) # relative center
        return [plt.arc(self.P2.x, self.P2.y, relC.x, relC.y, cw = self.cw)]


class CubicBezier():
    def __init__(self, P1, C1, C2, P2):
        self.P1 = P1
        self.C1 = C1
        self.C2 = C2
        self.P2 = P2
        self.cw = self.is_clockwise()

    def is_clockwise(self):
        sum = 0
        sum += (self.C1.x - self.P1.x) * (self.C1.y + self.P1.y)
        sum += (self.C2.x - self.C1.x) * (self.C2.y + self.C1.y)
        sum += (self.P2.x - self.C2.x) * (self.P2.y + self.C2.y)
        sum += (self.P1.x - self.P2.x) * (self.P1.y + self.P2.y)
        return sum < 0
    
    def point_at(self, t):
        x = (1 - t)**3 * self.P1.x + (3 * (1 - t)**2 * t) * self.C1.x + \
            (3 * (1 - t) * (t**2)) * self.C2.x + (t**3) * self.P2.x
        y = (1 - t)**3 * self.P1.y + (3 * (1 - t)**2 * t) * self.C1.y + \
            (3 * (1 - t) * (t**2)) * self.C2.y + (t**3) * self.P2.y
        return Point(x, y)

    def draw(self, canvas, color):
        t = 0.
        while t <= 1:
            p = self.point_at(t)
            p.draw(canvas, color)
            
            t += 0.001
    
    def to_biarc(self):
        # based on:
        # http://dlacko.org/blog/2016/10/19/approximating-bezier-curves-by-biarcs/

        # calculate V: the intersection point of the line between P1 and C1 with the line between P2 and C2
        V = Line(self.P1, self.C1).intersect(Line(self.P2, self.C2))
        

        # calculate G: the incenter point of the triangle P1, P2 and V
        # https://en.wikipedia.org/wiki/Incenter#Cartesian_coordinates

        # determine lengths of sides opposite the points
        lP1 = self.P2.dist(V)
        lP2 = self.P1.dist(V)
        lV  = self.P1.dist(self.P2)

        # the incenter point is the weighted average of the points with these lenghts
        G = ((self.P1.times(lP1)).plus(self.P2.times(lP2)).plus(V.times(lV))).times(1./(lP1 + lP2 + lV))
        
        # We know the tangent at P1.
        # Q1 lies on the line which is perpendicular to this tangent
        #  and goes through P1, let’s denote it by P1Q.
        # If we take the section between P1 and G,
        #  its perpendicular bisector (EQ1) intersects with P1Q at Q1.
        # The same method can be used to find Q2.

        # calculate the perpendicular bisectors
        E1 = self.P1.plus(G).times(0.5)
        E2 = self.P2.plus(G).times(0.5)

        
        # create the lines perpendicular to the tangents through P1, P2
        P1Q1 = Line(self.P1, self.C1).perpendicular_at(self.P1)
        P2Q2 = Line(self.P2, self.C2).perpendicular_at(self.P2)

        # create the perpendicular bisectors
        E1Q1 = Line(self.P1, G).perpendicular_at(E1)
        E2Q2 = Line(G, self.P2).perpendicular_at(E2)

        # find the centers and radii of the circles by intersecting the lines
        Q1 = P1Q1.intersect(E1Q1)
        Q2 = P2Q2.intersect(E2Q2)

        return CircleArc(self.P1, G, Q1, self.cw), CircleArc(G, self.P2, Q2, self.cw)
    
    def split_at(self, t):
        # split curve at t, return both new curves
        p0 = self.P1.plus(self.C1.minus(self.P1).times(t))
        p1 = self.C1.plus(self.C2.minus(self.C1).times(t))
        p2 = self.C2.plus(self.P2.minus(self.C2).times(t))

        p01 = p0.plus(p1.minus(p0).times(t))
        p12 = p1.plus(p2.minus(p1).times(t))

        dp = p01.plus(p12.minus(p01).times(t))
        
        return (CubicBezier(self.P1, p0, p01, dp), CubicBezier(dp, p12, p2, self.P2))
    
    def inflection_points(self):
        # http://www.caffeineowl.com/graphics/2d/vectorial/cubic-inflexion.html
        
        A = self.C1.minus(self.P1)
        B = self.C2.minus(self.C1).minus(A)
        C = self.P2.minus(self.C2).minus(A).minus(B.times(2))

        a = B.x * C.y - B.y * C.x
        b = A.x * C.y - A.y * C.x
        c = A.x * B.y - A.y * B.x
        
        d = b * b - 4 * a * c
        if d < 0:
            # no real inflection points
            t1 = t2 = -1
        else:
            # two real inflection points
            t1 = (-b + math.sqrt(d)) / (2*a)
            t2 = (-b - math.sqrt(d)) / (2*a)

        if not (0 < t1 < 1):
            t1 = -1
            
        if not (0 < t2 < 1):
            t2 = -1
            
        # order them
        if (t1 > t2):
            tmp = t1
            t1 = t2
            t2 = tmp
            
        return (t1, t2)

    def plot_instructions(self):
    	# convert to biarc
    	c1, c2 = self.to_biarc()
    	return c1.plot_instructions() + c2.plot_instructions()


class SineWave():
    # Sine wave with amplitude A, width n, starting point P
    # width = n, phase = p
    def __init__(self, P, A, n):
        self.P = P
        self.A = A
        self.n = n

    # we can parametrize the wave with t
    def point_at(self, t):
        return Point(self.P.x + t*self.n, self.A*math.sin(2*math.pi * t) + self.P.y)


    def draw(self, canvas, color):
        t = 0.
        while t <= 1:
            p = self.point_at(t)
            p.draw(canvas, color)
            
            t += 0.001

    def to_bezier(self):
        # cut into 4 parts
        P1 = Point(0, 0).plus(self.P)
        P2 = Point(self.n/4, self.A).plus(self.P)
        C1 = Point(self.n/(2*math.pi), self.A).plus(self.P)
        bez1 = CubicBezier(P1, C1, C1, P2)

        P1 = Point(self.n/4, self.A).plus(self.P)
        P2 = Point(self.n/2, 0).plus(self.P)
        C1 = Point((math.pi-1)*self.n/(2*math.pi), self.A).plus(self.P)
        bez2 = CubicBezier(P1, C1, C1, P2)

        P1 = Point(self.n/2, 0).plus(self.P)
        P2 = Point(3*self.n/4, -self.A).plus(self.P)
        C1 = Point((math.pi+1)*self.n/(2*math.pi), -self.A).plus(self.P)
        bez3 = CubicBezier(P1, C1, C1, P2)

        P1 = Point(3*self.n/4, -self.A).plus(self.P)
        P2 = Point(self.n, 0).plus(self.P)
        C1 = Point((2*math.pi-1)*self.n/(2*math.pi), -self.A).plus(self.P)
        bez4 = CubicBezier(P1, C1, C1, P2)

        return [bez1, bez2, bez3, bez4]

    def to_bezier2(self):
        # cut into 2 parts
        # these parameters were estimated by minimizing mse
        k1 = 0.205165
        k2 = 1.335837

        P1 = Point(0, 0).plus(self.P)
        P2 = Point(self.n/2, 0).plus(self.P)
        C1 = Point(k1*self.n, self.A*k2).plus(self.P)
        C2 = Point(self.n/2 - k1*self.n, self.A*k2).plus(self.P)
        bez1 = CubicBezier(P1, C1, C2, P2)

        P1 = Point(self.n/2, 0).plus(self.P)
        P2 = Point(self.n, 0).plus(self.P)
        C1 = Point(self.n/2 + k1*self.n, -self.A*k2).plus(self.P)
        C2 = Point(self.n - k1*self.n, -self.A*k2).plus(self.P)
        bez2 = CubicBezier(P1, C1, C2, P2)

        # looks better, but when converting to biarcs it looks horrible
        return [bez1, bez2]

    def to_bezier3(self):
    	# cut into 8 parts, each with 2 control points and 2 endpoints,
    	# hence 24 points. the pattern repeats after 12
    	# https://www.tinaja.com/glib/bezsine.pdf
    	s2 = math.sqrt(2)
    	pi = math.pi

    	P0  = self.P
    	P1  = Point( 1/24*self.n, (2*s2/7 - 1/7)*self.A).plus(P0)
    	P2  = Point( 2/24*self.n, (4*s2/7 - 2/7)*self.A).plus(P0)
    	P3  = Point( 3/24*self.n, (  s2/2      )*self.A).plus(P0)
    	P4  = Point( 4/24*self.n, (3*s2/7 + 2/7)*self.A).plus(P0)
    	P5  = Point( 5/24*self.n, (           1)*self.A).plus(P0)
    	P6  = Point( 6/24*self.n, (           1)*self.A).plus(P0)
    	P7  = Point( 7/24*self.n, (           1)*self.A).plus(P0)
    	P8  = Point( 8/24*self.n, (3*s2/7 + 2/7)*self.A).plus(P0)
    	P9  = Point( 9/24*self.n, (  s2/2      )*self.A).plus(P0)
    	P10 = Point(10/24*self.n, (4*s2/7 - 2/7)*self.A).plus(P0)
    	P11 = Point(11/24*self.n, (2*s2/7 - 1/7)*self.A).plus(P0)
    	P12 = Point(12/24*self.n, (           0)*self.A).plus(P0)

    	per1 = [CubicBezier(P0, P1, P2, P3), CubicBezier(P3, P4, P5, P6), CubicBezier(P6, P7, P8, P9), CubicBezier(P9, P10, P11, P12)]

    	P0  = self.P.plus(Point(self.n/2, 0))
    	P1  = Point( 1/24*self.n, -(2*s2/7 - 1/7)*self.A).plus(P0)
    	P2  = Point( 2/24*self.n, -(4*s2/7 - 2/7)*self.A).plus(P0)
    	P3  = Point( 3/24*self.n, -(  s2/2      )*self.A).plus(P0)
    	P4  = Point( 4/24*self.n, -(3*s2/7 + 2/7)*self.A).plus(P0)
    	P5  = Point( 5/24*self.n, -(           1)*self.A).plus(P0)
    	P6  = Point( 6/24*self.n, -(           1)*self.A).plus(P0)
    	P7  = Point( 7/24*self.n, -(           1)*self.A).plus(P0)
    	P8  = Point( 8/24*self.n, -(3*s2/7 + 2/7)*self.A).plus(P0)
    	P9  = Point( 9/24*self.n, -(  s2/2      )*self.A).plus(P0)
    	P10 = Point(10/24*self.n, -(4*s2/7 - 2/7)*self.A).plus(P0)
    	P11 = Point(11/24*self.n, -(2*s2/7 - 1/7)*self.A).plus(P0)
    	P12 = Point(12/24*self.n, -(           0)*self.A).plus(P0)

    	per2 = [CubicBezier(P0, P1, P2, P3), CubicBezier(P3, P4, P5, P6), CubicBezier(P6, P7, P8, P9), CubicBezier(P9, P10, P11, P12)]

    	return per1 + per2


    def plot_instructions(self):
    	# convert to bezier curves and plot these
    	bezs = self.to_bezier3()
    	return [pl for bez in bezs for pl in bez.plot_instructions()]