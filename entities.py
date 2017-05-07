from pygame import Rect	
from vector import *
from settings import *
import time
import math

class Tower:
	def shoot(self):
		self.shooting = True
	def get_target(self,enemies):
		target_index = None
		fartest_enemy_in_radius = 0
		for i in xrange(len(enemies)):
			if distance(self.position,enemies[i].position) <= self.radius:
				if enemies[i].node_index >= fartest_enemy_in_radius:
					fartest_enemy_in_radius = enemies[i].node_index
					target_index = i		
		return target_index
	def update(self,enemies):
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
			
class Enemy:
	def get_position(self):
		return self.position
	def receive_damage(self,damage,damage_type):
		self.life -= damage
	def seek(self,target):
		desired_velocity = normalize(target - self.position)*self.speed
		steering_force = desired_velocity - self.velocity#*0.1
		self.velocity = truncate(self.velocity + steering_force,self.speed)
		self.position = self.position + self.velocity
		self.rect.center = self.position.as_tuple()
	def get_orientation(self):
		n = 2.0
		current_node = self.path.get_node(self.node_index)
		v = current_node - self.position
		slope = float(v.y)/v.x
		if (slope > n or slope<-n) and v.y>0:
			return "up"
		if (n > slope and 1/n < slope) and v.y>0:
			return "rightup"
		if (slope < 1/n and slope > -1/n) and v.y<0:
			return "right"
		if (slope < -1/n and slope > -n) and v.y <0:
			return "right"
		if (slope > n or slope<-n) and v.y<0:
			return "m"
		if (n > slope and 1/n < slope) and v.y<0:
			return "left"
		if (slope > -1/n and slope < 1/n):
			return "left"
		if (slope < -1/n and slope > -n) and v.y >0:
			return "leftup"
	def update(self):
		if self.isFighting:
			return 1
		self.time_alive = time.time() - self.t0
		current_node = self.path.get_node(self.node_index)
		if current_node == None:
			return -1
		elif (current_node - self.position).__abs__() < 10:
			self.node_index += 1
		self.orientation = self.get_orientation()
		self.seek(current_node)
		return 0
		
class Soldier:
	def __init__(self, pos, barrack_pos, barrack_radius,life,damage):
		self.position = pos
		self.velocity = Vec2D(0,0)
		self.speed = SOLDIER_SPEED
		self.barrack_pos = barrack_pos
		self.barrack_radius = barrack_radius
		self.life = life
		self.damage = damage
		self.target_index = -1
		self.rect = Rect(pos.as_tuple(),(5,5))
		self.isAlive = True
		self.objetive = None
	def get_target(self,enemies):
		target_index = -1
		for i in xrange(len(enemies)):
			if distance(enemies[i].position,self.barrack_pos) < self.barrack_radius:
				if not enemies[i].isTargetedByASoldier:
					target_index = i
					break
				#if enemies[i].node_index >= fartest_enemy_in_radius:
				#	fartest_enemy_in_radius = enemies[i].node_index
				#	target_index = i
		if target_index == -1:
			return None
		else:
			return enemies[target_index]
	def seek(self,target):
		desired_velocity = normalize(target - self.position)*self.speed
		steering_force = (desired_velocity - self.velocity)*0.1
		self.velocity = truncate(self.velocity + steering_force,self.speed)
		self.position = self.position + self.velocity
		self.rect.center = self.position.as_tuple()
	def update(self,enemies):
		if self.objetive == None:
			self.objetive = self.get_target(enemies)
			if self.objetive != None:
				self.objetive.isTargetedByASoldier = True
			return 0
		if distance(self.position, self.objetive.position) > 10:
			self.seek(self.objetive.position)
		else:
			self.objetive.isFighting = True
			self.objetive.receive_damage(self.damage/FRAME_RATE)
			self.life -= enemies[self.target_index].meele_damage/FRAME_RATE
			if self.life <= 0:
				self.isAlive = False
				self.objetive.isTargetedByASoldier = False
				self.objetive.isFighting = False
			if self.objetive.life <= 0:
				self.objetive = None

class Projectile:
	def seek(self,target):
		desired_velocity = normalize(target - self.position)*self.speed
		steering_force = (desired_velocity - self.velocity)*0.1
		self.velocity = truncate(self.velocity + steering_force,self.speed)
		self.position = self.position + self.velocity
		self.rect.center = self.position.as_tuple()
	def update(self):
		#a = self.position.x > SCREEN_WIDTH
		#b = self.position.x < 0
		#c = self.position.y > SCREEN_HEIGHT
		#d = self.position.y < 0
		#if (a or b or c or d):
		#	self.IsAlive = False
		target = self.objetive.get_position()
		if target == self.old_target: # if the objetive did not move we consider it dead, 
			self.IsAlive = False	  # so the projecitile has no more reasons to exist
			return 1				  # this may be changed later
		self.old_target = target
		self.seek(target)
		return


class Archer_tower(Tower):
	def __init__(self, position, level = 0):
		self.tower_type = ARCHER_TOWER
		self.IsHighlighted = False # is the tower hightlighted by the player
		self.isSold = False
		self.position = position
		self.rect = Rect((0,0),(20,20))
		self.rect.center = self.position.as_tuple()
		self.level = level
		self.radius = ARCHER_TOWER_RADIUS[level]
		self.fire_rate = ARCHER_TOWER_FIRERATE[level] # in seconds
		self.damage = ARCHER_TOWER_DAMAGE[level]
		self.damage_type = "NORMAL"
		self.t0 = time.time() #time elapsed since last shoot
		self.shooting = False
		self.target_index = None
class Magic_tower(Tower):
	def __init__(self, position,level=0):
		self.tower_type = MAGIC_TOWER
		self.IsHighlighted = False # is the tower hightlighted by the player
		self.isSold = False
		self.position = position
		self.rect = Rect((0,0),(20,20))
		self.rect.center = self.position.as_tuple()
		self.level = level
		self.fire_rate = MAGIC_TOWER_FIRERATE[level] # in seconds
		self.radius = MAGIC_TOWER_RADIUS[level]
		self.damage = MAGIC_TOWER_DAMAGE[level]
		self.damage_type = "MAGIC"
		self.t0 = time.time() #time elapsed since last shoot
		self.shooting = False
		self.target_index = None
class Artillery_tower(Tower):
	def __init__(self, position,level=0):
		self.tower_type = ARTILLERY_TOWER
		self.IsHighlighted = False # is the tower hightlighted by the player
		self.isSold = False
		self.position = position
		self.rect = Rect((0,0),(20,20))
		self.rect.center = self.position.as_tuple()
		self.level = level
		self.damage = ARTILLERY_TOWER_DAMAGE[level]
		self.fire_rate = ARTILLERY_TOWER_FIRERATE[level] # in seconds
		self.damage_type = "AREA"
		self.radius = ARTILLERY_TOWER_RADIUS[level]
		self.t0 = time.time() #time elapsed since last shoot
		self.shooting = False
		self.target_index = None
class Barrack_tower():
	def __init__(self, position,level=0):
		self.active_soldiers = []
		self.tower_type = BARRACK_TOWER
		self.IsHighlighted = False # is the tower highlighted by the player
		self.isSold = False
		self.position = position
		self.rect = Rect((0,0),(20,20))
		self.rect.center = self.position.as_tuple()
		self.level = level
		self.soldier_damage = BARRACK_SOLDIER_DAMAGE[level]
		self.soldier_life = BARRACK_SOLDIER_LIFE[level]
		self.spawn_rate = BARRACK_TOWER_SPAWN_RATE[level] # in seconds
		self.radius = BARRACK_TOWER_RADIUS[level]
		self.t0 = time.time() #time elapsed since last soldier spawn
		for i in xrange(SOLDIERS_PER_BARRACK):
			self.active_soldiers.append(Soldier(self.position,
													self.position,
													self.radius,
													self.soldier_life,
													self.soldier_damage))
	def update(self,enemies):
		if len(self.active_soldiers) < SOLDIERS_PER_BARRACK:
			t1 = time.time()
			if t1 -self.t0 > self.spawn_rate:
				t0 = t1
				print "creating soldier"
				self.active_soldiers.append(Soldier(self.position,
													self.position,
													self.radius,
													self.soldier_life,
													self.soldier_damage))
		for i in xrange(len(self.active_soldiers)-1,-1,-1):
			self.active_soldiers[i].update(enemies)
			if self.active_soldiers[i].life <= 0:
				del self.active_soldiers[i]
		return 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

class Basic_enemy(Enemy):
	def __init__(self,path):
		self.enemy_type = BASIC_ENEMY
		self.path = path
		self.position = self.path.get_node(0)
		self.speed = BASIC_ENEMY_SPEED
		self.rect = Rect((0,0),(5,5))
		self.node_index = 0
		self.velocity = Vec2D(0,0)
		self.life = BASIC_ENEMY_LIFE
		self.t0 = time.time()
		self.time_alive = time.time() - self.t0
		self.isTargetedByASoldier = False
		self.isFighting = False
		self.meele_damage = BASIC_ENEMY_MEELE_DAMAGE
	def receive_damage(self,damage,damage_type = "NORMAL"):
		self.life -= damage
	def pick_representation(self):
		swap_time = 0.2
		sprites_per_row = 5
		sprites_per_column = 11
		walking_sprites = 5
		fighting_sprites = 3
		if orientation = "up":
			if not isFighting:
				n = int(self.time_alive/swap_time)%walking_sprites
				return sprites_per_row*n
			else:
				n = int(self.time_alive/swap_time)%fighting_sprites
				return (sprites_per_row*(walking_sprites+n)
class Fast_enemy(Enemy):
	def __init__(self,path):
		self.enemy_type = FAST_ENEMY
		self.path = path
		self.position = self.path.get_node(0)
		self.speed = FAST_ENEMY_SPEED
		self.rect = Rect((0,0),(5,5))
		self.node_index = 0
		self.velocity = Vec2D(0,0)
		self.life = FAST_ENEMY_LIFE
		self.t0 = time.time()
		self.time_alive = time.time() - self.t0
		self.isTargetedByASoldier = False
		self.isFighting = False
		self.meele_damage = FAST_ENEMY_MEELE_DAMAGE
	def receive_damage(self,damage,damage_type = "NORMAL"):
		self.life -= damage
class Armored_enemy(Enemy):
	def __init__(self,path):
		self.enemy_type = ARMORED_ENEMY
		self.path = path
		self.position = self.path.get_node(0)
		self.speed = ARMORED_ENEMY_SPEED
		self.rect = Rect((0,0),(5,5))
		self.node_index = 0
		self.velocity = Vec2D(0,0)
		self.life = ARMORED_ENEMY_LIFE
		self.isTargetedByASoldier = False
		self.isFighting = False
		self.meele_damage = ARMORED_ENEMY_MEELE_DAMAGE
	def receive_damage(self,damage,damage_type = "NORMAL"):
		if damage_type == "NORMAL":
			self.life -= damage*ARMORED_ENEMY_RESISTANCE
		if damage_type == "MAGIC":	
			self.life -= damage
class Sorcerer_enemy(Enemy):
	def __init__(self,path):
		self.enemy_type = SORCERER_ENEMY
		self.path = path
		self.position = self.path.get_node(0)
		self.speed = SORCERER_ENEMY_SPEED
		self.rect = Rect((0,0),(5,5))
		self.node_index = 0
		self.velocity = Vec2D(0,0)
		self.life = SORCERER_ENEMY_LIFE
		self.isTargetedByASoldier = False
		self.isFighting = False
		self.meele_damage = SORCERER_ENEMY_MEELE_DAMAGE
	def receive_damage(self,damage,damage_type = "NORMAL"):
		if damage_type == "NORMAL":
			self.life -= damage
		if damage_type == "MAGIC":	
			self.life -= damage*SORCERER_ENEMY_MAGIC_RESISTANCE

class Arrow(Projectile):
	def __init__(self,starting_pos,objetive,damage):
		self.projectile_type = "ARROW"
		self.damage = damage
		self.damage_type = "NORMAL"
		self.objetive = objetive
		self.position = starting_pos
		self.velocity = Vec2D(0,0)
		self.speed = ARROW_SPEED
		self.rect = Rect((0,0),(5,5))
		self.old_target = self.objetive.get_position()
		self.IsAlive = True
class Magic_ray(Projectile):
	def __init__(self,starting_pos,objetive,damage):
		self.projectile_type = "MAGIC RAY"
		self.damage = damage
		self.damage_type = "MAGIC"
		self.objetive = objetive
		self.position = starting_pos
		self.velocity = Vec2D(0,0)
		self.speed = MAGIC_RAY_SPEED
		self.rect = Rect((0,0),(5,5))
		self.old_target = self.objetive.get_position()
		self.IsAlive = True
class Cluster_bomb(Projectile):
	def __init__(self,starting_pos,objetive,damage):
		self.projectile_type = "CLUSTER BOMB"
		self.damage = damage
		self.damage_type = "NORMAL"
		self.bomb_radius = ARTILLERY_TOWER_AREA
		self.objetive = objetive
		self.position = starting_pos
		self.velocity = Vec2D(0,0)
		self.speed = CLUSTER_BOMB_SPEED
		self.rect = Rect((0,0),(5,5))
		self.bomb_rect = Rect((0,0),(5,5))
		self.old_target = self.objetive.get_position()
		self.IsAlive = True
	

	
		
