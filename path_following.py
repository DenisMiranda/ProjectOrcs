from vector import *
import math

class Path:
	"""This class contains a list of nodes representing a path,
		a node is a vector object ie: a point on the screen.
		This class also provide the means to translate the path,
		and updating it in the event of a window resizing"""
	def __init__(self,nodes = []):
		self.nodes = nodes
	def get_node(self,index):
		if index < len(self.nodes):
			return self.nodes[index]
		else :
			return None
	def add_node(self,node):
		self.nodes.append(Vec2D(node[0],node[1]))
	def remove_node(self,index):
		if index < len(self.node):
			del path[index]
		else:
			print "Index out of range"
	def pop_node(self):
		del self.nodes[-1]
	def update_path(self, inflation_x, inflation_y):
		for i in xrange(len(self.nodes)):
			self.nodes[i].x *= inflation_z
			self.nodes[i].y *= inflation_y
	def new_translated_path(self,offset_module):
		new_nodes = []
		if offset_module == 0:
			return Path(self.nodes)
		direction = abs(offset_module)/offset_module
		for i in xrange(len(self.nodes)):
			if i +1  == len(self.nodes):
				break 
			v = self.nodes[i+1] - self.nodes[i]
			w = normalize(v.rotate(math.pi/2))
			new_node = self.nodes[i] + w*offset_module
			new_nodes.append(new_node)
		return Path(new_nodes)
	def __str__(self):
		if len(self.nodes) == 0:
			return "()"
		string = "("
		for node in self.nodes:
			string += node.__str__() + ","
		string = string[:-1] + ")"
		return string
			
		
		                                                                                                  
		
		
 
		
