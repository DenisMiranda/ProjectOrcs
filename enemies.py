from pygame import Rect
from vector import *
from settings import *
import time
import math
import animations
import random

class Breed():
	def __init__(self,type,life,speed,damage,resistance,animations,reward,life_cost):
		self.type = type
		self.life = life
		self.speed = speed
		self.melee_damage = damage
		self.animations = animations
		self.resistance = resistance
		self.reward = reward
		self.life_cost = life_cost

basic_enemy_breed = Breed(BASIC_ENEMY,BASIC_ENEMY_LIFE,BASIC_ENEMY_SPEED,
						BASIC_ENEMY_MEELE_DAMAGE,
						(None,None),
						animations.basic_enemy_animations,
						BASIC_ENEMY_REWARD,BASIC_ENEMY_LIVES_COST)
fast_enemy_breed = Breed(FAST_ENEMY,FAST_ENEMY_LIFE,FAST_ENEMY_SPEED,
						FAST_ENEMY_MEELE_DAMAGE,
						(None,None),
						animations.fast_enemy_animations,
						FAST_ENEMY_REWARD,FAST_ENEMY_LIVES_COST)
armored_enemy_breed = Breed(ARMORED_ENEMY,ARMORED_ENEMY_LIFE,ARMORED_ENEMY_SPEED,
						ARMORED_ENEMY_MEELE_DAMAGE,
						("NORMAL",0.5),
						animations.armored_enemy_animations,
						ARMORED_ENEMY_REWARD,ARMORED_ENEMY_LIVES_COST)
boss_enemy_breed = Breed(BOSS_ENEMY,BOSS_ENEMY_LIFE,BOSS_ENEMY_SPEED,
						BOSS_ENEMY_MEELE_DAMAGE,
						("NORMAL",0.5),
						animations.boss_enemy_animations,
						BOSS_ENEMY_REWARD,BOSS_ENEMY_LIVES_COST)
skeleton_enemy_breed = Breed(BASIC_ENEMY,BASIC_ENEMY_LIFE,BASIC_ENEMY_SPEED,
						BASIC_ENEMY_MEELE_DAMAGE,
						(None,None),
						animations.skeleton_enemy_animations,
						BASIC_ENEMY_REWARD,BASIC_ENEMY_LIVES_COST)

class Enemy:
	def __init__(self,breed,path):
		self.enemy_type = breed.type
		self.life = breed.life
		self.speed = breed.speed
		self.meele_damage = breed.melee_damage
		self.animations = breed.animations
		self.resistance = breed.resistance
		self.reward = breed.reward
		self.life_cost = breed.life_cost
		self.t0 = time.time() + 1000*random.random()
		self.time_alive = time.time() - self.t0
		self.node_index = 0
		self.path = path
		self.position = self.path.get_node(0)
		self.velocity = Vec2D(0,0)
		self.rect = self.animations.get_animation("walking_up").get_current_frame(self.time_alive).get_rect()
		self.rect.center = self.position.as_tuple()
		self.old_rect = self.rect
		self.bounding_box = Rect((0,0),(5,5))
		self.isTargetedByASoldier = 0
		self.isFighting = False
		self.isAlive = True
		self.reachEnd = False
		self.orientation = "up"
		self.act_like_dead = False
		self.time_dead = 0
	def get_position(self):
		return self.position
	def receive_damage(self,damage,damage_type="NORMAL"):
		if damage_type == self.resistance[0]:
			self.life -= damage*self.resistance[1]
		else:
			self.life -= damage
	def seek(self,target):
		desired_velocity = normalize(target - self.position)*self.speed
		steering_force = desired_velocity - self.velocity#*0.1
		self.velocity = truncate(self.velocity + steering_force,self.speed)
		self.position = self.position + self.velocity
		self.rect.center = self.position.as_tuple()
		self.bounding_box.center = self.position.as_tuple()
	def get_orientation(self):
		n = 2.0 #magic constants :(
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
		if self.act_like_dead:
			return self.animations.get_animation("dead").get_current_frame(self.time_alive)
		if not self.isFighting:
			return self.animations.get_animation("walking_"+self.orientation).get_current_frame(self.time_alive)
		else:
			return self.animations.get_animation("fighting_"+self.orientation).get_current_frame(self.time_alive)
	def update(self):
		if self.act_like_dead:
			#self.time_alive = time.time() - self.t0
			if time.time() - self.time_dead > 2.0:
				self.isAlive = False
			return
		if self.life <=0:
			self.act_like_dead = True
			self.time_dead = time.time()
			return
		if self.isFighting:
			self.time_alive = time.time() - self.t0
			return
		self.time_alive = time.time() - self.t0
		current_node = self.path.get_node(self.node_index)
		if current_node == None:
			self.reachEnd = True
			return
		elif (current_node - self.position).__abs__() < 10:
			self.node_index += 1
		self.orientation = self.get_orientation()
		self.old_rect = self.rect
		self.seek(current_node)
		return 0
