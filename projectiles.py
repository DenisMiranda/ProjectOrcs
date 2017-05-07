from pygame import Rect
from vector import *
import animations
from settings import *
import time
class Projectile:
	def __init__(self,type,starting_pos,objetive,damage,radius = 0):
		if type == "ARROW":
			self.projectile_type = "ARROW"
			self.damage_type = "NORMAL"
			self.speed = ARROW_SPEED
			self.animation = animations.fireb_animation
		if type == "MAGIC RAY":
			self.projectile_type = "MAGIC_RAY"
			self.damage_type = "MAGIC"
			self.speed = MAGIC_RAY_SPEED
			self.animation = animations.magic_missile_animation
		if type == "CLUSTER BOMB":
			self.projectile_type = "CLUSTER_BOMB"
			self.damage_type = "NORMAL"
			self.speed = CLUSTER_BOMB_SPEED
			self.radius = radius
			self.speed = CLUSTER_BOMB_SPEED
			self.animation = animations.firep_animation
		self.damage = damage
		self.objetive = objetive
		self.position = starting_pos
		self.starting_pos = starting_pos
		self.end_pos = starting_pos + objetive.velocity*FRAME_RATE*0.5
		self.v0x = (self.end_pos.x - self.starting_pos.x)/0.5
		self.v0y = (self.end_pos.y - starting_pos.y + 0.5*9.81*0.25)/0.5
		self.velocity = Vec2D(self.v0x,self.v0y)
		self.velocity = Vec2D(0,0)
		self.rect = self.animation.get_animation("traveling").get_current_frame(1).get_rect()
		self.old_rect = self.rect.copy()
		self.old_target = self.objetive.get_position()
		self.t0 = time.time()
		self.isAlive = True
	def follow_arc(self,t):
		self.velocity = Vec2D(self.v0x,self.v0y -9.81*t**2)
		self.position += Vec2D(self.v0x,self.v0y -9.81*t**2)
		self.rect.center = self.position.as_tuple()
	def seek(self,target):
		desired_velocity = normalize(target - self.position)*self.speed
		steering_force = (desired_velocity - self.velocity)*0.1
		self.velocity = truncate(self.velocity + steering_force,self.speed)
		self.position = self.position + self.velocity
		self.rect.center = self.position.as_tuple()
	def get_representation(self):
		state = "traveling"
		return self.animation.get_animation(state).get_current_frame(1)
	def update(self):
		target = self.objetive.get_position()
		if not self.objetive.isAlive: # if the objetive is dead,
			self.isAlive = False	  # the projecitile has no more reasons to exist
		self.old_rect = self.rect.copy()
		t = time.time() - self.t0
		if t > 1:
			self.isAlive = False
			return
		#self.follow_arc(t)
		self.seek(target)
		return 0
