from pygame import Rect
from vector import *
from settings import *
from soldier import *
import animations
import time
import math
class Tower(object):
	def __init__(self,type, position, level = 0):
		if type == "ARCHER_TOWER":
			self.tower_type = ARCHER_TOWER
			self.radius = ARCHER_TOWER_RADIUS[level]
			self.fire_rate = ARCHER_TOWER_FIRERATE[level] # in seconds
			self.damage = ARCHER_TOWER_DAMAGE[level]
			self.damage_type = "NORMAL"
			self.animation = animations.archer_tower_animation
		elif type == "MAGIC_TOWER":
			self.tower_type = MAGIC_TOWER
			self.radius = MAGIC_TOWER_RADIUS[level]
			self.fire_rate = MAGIC_TOWER_FIRERATE[level] # in seconds
			self.damage = MAGIC_TOWER_DAMAGE[level]
			self.damage_type = "MAGIC"
			self.animation = animations.magic_tower_animation
		elif type == "ARTILLERY_TOWER":
			self.tower_type = ARTILLERY_TOWER
			self.radius = ARTILLERY_TOWER_RADIUS[level]
			self.fire_rate = ARTILLERY_TOWER_FIRERATE[level] # in seconds
			self.damage = ARTILLERY_TOWER_DAMAGE[level]
			self.damage_type = "NORMAL"
			self.animation = animations.artillery_tower_animation
			self.area = ARTILLERY_TOWER_AREA[0]
		self.position = position
		self.IsHighlighted = False # is the tower hightlighted by the player
		self.willBeSold = False
		self.isSold = False
		self.level = level
		self.t0 = time.time() #time elapsed since last shoot
		self.shooting = False
		self.target_index = None
		self.t0 = time.time()
		self.time_alive = time.time()-self.t0
		self.rect = self.animation.get_animation("standing0").get_current_frame(self.time_alive).get_rect()
		self.rect.center = self.position.as_tuple()
	def shoot(self):
		self.shooting = True
	def get_target(self,enemies):
		target_index = None
		fartest_enemy_in_radius = 0
		for i in xrange(len(enemies)):
			if distance(self.position,enemies[i].position) <= self.radius and not enemies[i].act_like_dead:
				if enemies[i].node_index >= fartest_enemy_in_radius:
					fartest_enemy_in_radius = enemies[i].node_index
					target_index = i
		return target_index
	def upgrade_tower(self,money):
		if self.level < MAX_TOWER_LEVEL:
			self.level += 1
			level = self.level
			if self.tower_type == ARCHER_TOWER and money >= ARCHER_TOWER_COST[level]:
				money -= ARCHER_TOWER_COST[level]
				self.damage = ARCHER_TOWER_DAMAGE[level]
				self.fire_rate = ARCHER_TOWER_FIRERATE[level]
				self.radius = ARCHER_TOWER_RADIUS[level]
			elif self.tower_type == MAGIC_TOWER and money >= MAGIC_TOWER_COST[level]:
				money -= MAGIC_TOWER_COST[level]
				self.damage = MAGIC_TOWER_DAMAGE[level]
				self.fire_rate = MAGIC_TOWER_FIRERATE[level]
				self.radius = MAGIC_TOWER_RADIUS[level]
			elif self.tower_type == ARTILLERY_TOWER and money >= ARTILLERY_TOWER_COST[level]:
				money -= ARTILLERY_TOWER_COST[level]
				self.damage = ARTILLERY_TOWER_DAMAGE[level]
				self.fire_rate = ARTILLERY_TOWER_FIRERATE[level]
				self.radius = ARTILLERY_TOWER_RADIUS[level]
				self.area = ARTILLERY_TOWER_AREA[level]
			else:
				self.level -= 1
		return money
	def get_representation(self):
		state = "standing"+str(self.level)
		return self.animation.get_animation(state).get_current_frame(1)
	def update(self,enemies):
		self.time_alive = time.time() - self.t0
		self.target_index = None
		self.shooting = False
		t1 = time.time()
		if t1 - self.t0 > self.fire_rate:
			self.target_index = self.get_target(enemies)
			if self.target_index == None:
				return None
			else:
				self.shoot()
				self.t0 = t1
		if self.shooting == True:
			return "SHOOT"
		else:
			return None

class Barrack_tower(Tower):
	def __init__(self, position,level=0):
		self.active_soldiers = 0
		self.tower_type = BARRACK_TOWER
		self.animation = animations.barrack_tower_animation
		self.IsHighlighted = False # is the tower highlighted by the player
		self.isSold = False
		self.willBeSold = False
		self.position = position
		self.rect = self.animation.get_animation("standing0").get_current_frame(1).get_rect()
		self.rect.center = self.position.as_tuple()
		self.level = level
		self.soldier_damage = BARRACK_SOLDIER_DAMAGE[level]
		self.soldier_life = BARRACK_SOLDIER_LIFE[level]
		self.spawn_rate = BARRACK_TOWER_SPAWN_RATE[level] # in seconds
		self.radius = BARRACK_TOWER_RADIUS[level]
		self.t0 = time.time() #time elapsed since last soldier spawn
	def upgrade_tower(self,money):
		if self.level < MAX_TOWER_LEVEL and money >= BARRACK_TOWER_COST[self.level] :
			self.level += 1
			level = self.level
			money -= BARRACK_TOWER_COST[level]
			self.soldier_damage = BARRACK_SOLDIER_DAMAGE[level]
			self.soldier_life = BARRACK_SOLDIER_LIFE[level]
			self.radius = ARCHER_TOWER_RADIUS[level]
			self.spawn_rate = BARRACK_TOWER_SPAWN_RATE[level] # in seconds
			self.radius = BARRACK_TOWER_RADIUS[level]
		return money
	def get_representation(self):
		state = "standing"+str(self.level)
		return self.animation.get_animation(state).get_current_frame(1)
	def update(self,enemies):
		if self.active_soldiers < SOLDIERS_PER_BARRACK:
			t1 = time.time()
			if t1 -self.t0 > self.spawn_rate:
				self.t0 = t1
				self.active_soldiers += 1
				return "SPAWN"
		return 0
