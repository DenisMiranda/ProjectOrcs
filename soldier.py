from vector import *
from settings import *
import animations
import time
class Soldier:
	def __init__(self, pos, barrack_pos, barrack_radius,life,damage,tower=None):
		self.position = pos
		self.velocity = Vec2D(0,0)
		self.speed = SOLDIER_SPEED
		self.barrack_pos = barrack_pos
		self.barrack_radius = barrack_radius
		self.life = life
		self.damage = damage
		self.target_index = -1
		self.isAlive = True
		self.isFighting = False
		self.objetive = None
		self.t0 = time.time()
		self.time_alive = time.time() - self.t0
		self.animations = animations.soldier_animations
		self.rect = self.animations.get_animation("walking_up").get_current_frame(self.time_alive).get_rect()
		self.rect.center = self.position.as_tuple()
		self.old_rect = self.rect.copy()
		self.state = "standing"
		self.orientation = "up"
		self.tower = tower
	def notify_dead(self):
		if not self.tower == None:
			self.tower.active_soldiers-=1
	def get_target(self,enemies):
		target_index = -1
		counter = 0
		for i in xrange(len(enemies)):
			if distance(enemies[i].position,self.barrack_pos) < self.barrack_radius:
				if not enemies[i].isTargetedByASoldier:
					target_index = i
					break
				else:
					target_index = i

				#if enemies[i].node_index >= fartest_enemy_in_radius:
				#	fartest_enemy_in_radius = enemies[i].node_index
				#	target_index = i
		if target_index == -1:
			return None
		else:
			return enemies[target_index]
	def get_orientation(self):
		n = 2.0
		m = 0.5
		v = -self.velocity
		if v.x == 0 and v.y >= 0:
			return "up"
		elif v.x == 0 and v.y<0:
			return "down"
		slope = float(v.y)/v.x
		if (slope > n or slope <= -1/m) and v.y>0:
			return "up"
		elif (slope < -1/n and slope > -1/m) and v.y > 0:
			return "right_up"
		#elif (slope <= m and slope >= -1/n) and v.x > 0:
		elif ((slope < m and slope >= -1/n) and v.x < 0):
			return "right"
		elif (slope > m and slope < n) and v.y<0:
			return "right_down"
		elif (slope < -1/m or slope > n) and v.y < 0:
			return "down"
		elif (slope < -1/n and slope > -1/m) and v.y <0:
			return "left_down"
		elif (slope <= m and slope >= -1/n) and v.x > 0:
			return "left"
		elif (slope < n and slope > m) and v.y>0:
			return "left_up"
	def get_representation(self):
		if not self.isFighting:
			if self.state == "standing":
				return self.animations.get_animation("walking_right").get_current_frame(1)
			if self.state == "walking":
				return self.animations.get_animation("walking_"+self.orientation).get_current_frame(self.time_alive)
		else:
			return self.animations.get_animation("fighting_"+self.orientation).get_current_frame(self.time_alive)
	def seek(self,target):
		desired_velocity = normalize(target - self.position)*self.speed
		steering_force = (desired_velocity - self.velocity)*0.1
		self.velocity = truncate(self.velocity + steering_force,self.speed)
		self.position = self.position + self.velocity
		self.rect.center = self.position.as_tuple()
	def update(self,enemies):
		self.time_alive = time.time() - self.t0
		self.orientation = self.get_orientation()
		if self.objetive == None:
			self.state = "standing"
			self.objetive = self.get_target(enemies)
			if self.objetive != None:
				self.objetive.isTargetedByASoldier += 1
			return 0
		if  distance(self.barrack_pos,self.objetive.position) > self.barrack_radius:
			self.objetive = None
			self.state = "standing"
			return
		if distance(self.position, self.objetive.position) > 40:
			self.state = "walking"
			self.old_rect = self.rect.copy()
			self.seek(self.objetive.position)
		else:
			if self.life <= 0:
				self.isAlive = False
				self.objetive.isTargetedByASoldier -=1
				self.objetive.isFighting = False
				self.notify_dead()
				return
			if self.objetive.life <= 0:
				self.isFighting = False
				self.objetive = None
				return
			self.isFighting = True
			self.objetive.isFighting = True
			self.objetive.receive_damage(self.damage/FRAME_RATE)	
			self.life -= self.objetive.meele_damage/FRAME_RATE
