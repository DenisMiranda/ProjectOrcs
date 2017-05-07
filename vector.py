import math

class Vec2D():
    def __init__(self, x, y):
        self.x = x
        self.y = y
	def set(self, x, y):
		self.x = x
		self.y = y
    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vec2D(self.x - other.x, self.y - other.y)
    def __mul__(self, n):
        return Vec2D(self.x*n,self.y*n)
    def __neg__(self):
        return Vec2D(-self.x,-self.y)
    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)
    def rotate(self,angle):
		x = self.x*math.cos(angle) - self.y*math.sin(angle)
		y = self.x*math.sin(angle) + self.y*math.cos(angle)
		return Vec2D(x,y)
    def __eq__(self, other):
		if other == None:
			return False
		else:
			return self.x == other.x and self.y == other.y
    def __str__(self):
        return '(%g, %g)' % (self.x, self.y)
    def as_tuple(self):
		return self.x,self.y
    def __ne__(self, other):
        return not self.__eq__(other)  # reuse __eq__

def normalize(v):
	module = v.__abs__()
	if (module == 0):
		return Vec2D(0,0)
	return Vec2D(v.x/module,v.y/module)
def truncate(v,speed):
	if v.__abs__() > speed:
		return normalize(v)*speed
	else:
		return v
def distance(v,w):
	return math.sqrt((v.x - w.x)**2 + (v.y-w.y)**2)
def inside_circle(pos, center, radius):
	if (pos.x - center.x)**2 + (pos.y - center.y)**2 >= radius**2:
		return False
	else:
		return True
def get_slope(v,w):
	if v.x == w.x:
		return "vertical"
	else:
		return float(v.y - w.y)/(v.x - w.x)

def get_quadrant(v):
	if v.x > 0 and v.y > 0:
		return 1
	elif v.x < 0 and v.y > 0:
		return 2
	elif v.x < 0 and v.y < 0:
		return 3
	elif v.x > 0 and v.y < 0:
		return 4
