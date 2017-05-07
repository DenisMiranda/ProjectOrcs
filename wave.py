import time
import random
class Wave():
	def __init__(self,cant_routes,timer = 1):
		self.wave = []
		self.index = 0
		self.timer = timer
		self.t0 = time.time()
		self.cant_routes = cant_routes
	def load_from_file(self,wave_file):
		try:
			f = open(wave_file,"r")
		except IOError:
			print 'Error: Can\'t find "%s" file'
			return 1
		for line in f.readlines():
			line = line.split(" ")
			try:
				enemy_type = int(line[0])
				route = line[1][0]
				if route == "*":
					path = random.randint(0,self.cant_routes-1)
				elif int(route) >= 0 and int(route) < self.cant_routes:
					path = int(route)
				else:
					print 'Error: Skiping invalid line'
					continue
				self.wave.append((enemy_type,path))
			except ValueError:
				print 'Error: Skiping invalid line'
				continue
		f.close()
	def load_from_list(self,wave_list):
		self.wave = wave
	def add_enemy(self,enemy_type):
		self.wave.append(enemy_type)
	def next_enemy(self):
		t1 = time.time()
		if t1 - self.t0 > self.timer:
			self.t0 = t1
			if self.index < len(self.wave):
				enemy_type = self.wave[self.index][0]
				route = self.wave[self.index][1]
				self.index += 1
				return (enemy_type,route)
			else:
				return "WAVE END"
		else:
			return (-1,-1)

		
