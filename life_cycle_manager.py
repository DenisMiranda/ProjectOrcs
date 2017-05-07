from enemies import *
from towers import *
from projectiles import *
from soldier import *
from settings import *
from fire_storm import Explosion
from pygame import Rect
import time
import pygame
pygame.init()
class Life_cycle_manager():
	"""This class manager the life cycle of every entity in the game"""
	def __init__(self,waves,paths,money,lives,tower_placements,timers = []):
		self.n = 0
		self.act_tower = ARCHER_TOWER
		self.projectiles = []
		self.enemies = []
		self.soldiers = []
		self.towers = []
		self.tower_placements = tower_placements
		self.wave_num = len(waves)
		self.waves = waves
		self.wave_index = 0
		self.paths = paths
		self.money = money
		self.lives = lives
		self.start_first_wave = False
		self.events = []
		self.time = time.time()
		self.last_reinforcements_call = time.time() - REINFORCEMENTS_COOLDOWN
		self.last_fire_call = time.time() - FIRE_STORM_COOLDOWN
		if timers == []:
			self.timers = [20 for i in xrange(len(self.waves))]
		else:
			self.timers = timers
		self.call_reinforcements = False
		self.fire_rain = False
		self.call_reinforcements_color = (0,120,20)
		self.fire_rain_color = (0,120,20)
		self.sounds = []
	def check_victory(self):
		if self.wave_index == len(self.waves) - 1:
			if self.waves[self.wave_index].index == len(self.waves[self.wave_index].wave):
				if len(self.enemies) == 0:
					return "VICTORY"
	def call_next_wave(self):
		if self.wave_index < len(self.waves) - 1:
			self.sounds.append("horn")
			self.wave_index += 1
	def add_enemies(self,enemy_id = None):
		i = None
		for i in xrange(self.wave_index + 1):
			next_enemy_info = self.waves[i].next_enemy()
			next_enemy = next_enemy_info[0]
			path_index = next_enemy_info[1]
			if next_enemy == BASIC_ENEMY:
				self.add_enemy(Enemy(basic_enemy_breed,self.paths[path_index]))
			elif next_enemy == SKELETON_ENEMY:
				self.add_enemy(Enemy(skeleton_enemy_breed,self.paths[path_index]))
			elif next_enemy == FAST_ENEMY:
				self.add_enemy(Enemy(fast_enemy_breed,self.paths[path_index]))
			elif next_enemy == ARMORED_ENEMY:
				self.add_enemy(Enemy(armored_enemy_breed,self.paths[path_index]))
			elif next_enemy == SORCERER_ENEMY:
				self.add_enemy(Enemy(sorcerer_enemy_breed,self.paths[path_index]))
			elif next_enemy == BOSS_ENEMY:
				self.add_enemy(Enemy(boss_enemy_breed,self.paths[path_index]))
	def add_soldier(self,position,barrack_position,radius,life,damage,tower = None,fromTower = False):
		t1 = time.time()
		if fromTower:
			self.soldiers.append(Soldier(position,barrack_position,radius,life,damage,tower))
			if len(self.soldiers) > 1 and self.soldiers[-2].isFighting:
				self.sounds.append("battle")
			return
		if t1 - self.last_reinforcements_call > REINFORCEMENTS_COOLDOWN :
			self.last_reinforcements_call = t1
			self.soldiers.append(Soldier(position,barrack_position,radius,life,damage,tower))
			if len(self.soldiers) > 1 and self.soldiers[-2].isFighting:
				self.sounds.append("battle")
			return
		self.sounds.append("error")
	def add_tower(self,tower_type,position):
		placement = -1
		for i in xrange(len(self.tower_placements)):
			if inside_circle(position,self.tower_placements[i],25):
				placement = i
				break;
		if placement == -1:	
			self.sounds.append("error")
			return
		if tower_type == ARCHER_TOWER and self.money >= ARCHER_TOWER_COST[0]:
			self.money -= ARCHER_TOWER_COST[0]
			self.towers.append(Tower("ARCHER_TOWER", self.tower_placements[placement]))
		elif tower_type == MAGIC_TOWER and self.money >= MAGIC_TOWER_COST[0]:
			self.money -= MAGIC_TOWER_COST[0]
			self.towers.append(Tower("MAGIC_TOWER", self.tower_placements[placement]))
		elif tower_type == ARTILLERY_TOWER and self.money >= ARTILLERY_TOWER_COST[0]:
			self.money -= ARTILLERY_TOWER_COST[0]
			self.towers.append(Tower("ARTILLERY_TOWER", self.tower_placements[placement]))
		elif tower_type == BARRACK_TOWER and self.money >= BARRACK_TOWER_COST[0]:
			self.money -= BARRACK_TOWER_COST[0]
			self.towers.append(Barrack_tower(self.tower_placements[placement]))
		else:
			self.sounds.append("error")
	def add_enemy(self,enemy):
		self.enemies.append(enemy)
	def add_projectile(self,projectile):
		t1 = time.time()
		if projectile.projectile_type != "FIRE":
			self.projectiles.append(projectile)
		elif projectile.projectile_type == "FIRE" and t1 - self.last_fire_call > FIRE_STORM_COOLDOWN:
			self.projectiles.append(projectile)
			self.last_fire_call = t1
			self.sounds.append("fire")
			return
		else:
			self.sounds.append("error")
	def sell_tower(self,tower_index):
		tower_type = self.towers[tower_index].tower_type
		level = self.towers[tower_index].level
		if tower_type == ARCHER_TOWER:
			self.money += ARCHER_TOWER_SELL_PRICE[level]
		elif tower_type == MAGIC_TOWER:
			self.money += MAGIC_TOWER_SELL_PRICE[level]
		elif tower_type == ARTILLERY_TOWER:
			self.money += ARTILLERY_TOWER_SELL_PRICE[level]
		elif tower_type == BARRACK_TOWER:
			self.money += BARRACK_TOWER_SELL_PRICE[level]
		self.towers[tower_index].willBeSold = True
	def upgrade_tower(self,tower_index):
		money = self.money
		self.money = self.towers[tower_index].upgrade_tower(self.money)
		if self.money == money:
			self.sounds.append("error")
	def remove_tower(self,tower_index):
		del self.towers[tower_index]
	def remove_enemy(self,enemy_index):
		self.money += self.enemies[enemy_index].reward
		del self.enemies[enemy_index]
	def remove_projectile(self,projectile_index):
		del self.projectiles[projectile_index]
	def remove_soldier(self,soldier_index):
		del self.soldiers[soldier_index]
	def update_collision_manager(self): #need to sort this mess
		"""check for collisions betwen entities and act accordingly"""
		#enemy_rects = [Rect(enemy.position.as_tuple(),(10,10)) for enemy in self.enemies]
		projectile_rects = [projectile.rect for projectile in self.projectiles]
		for i in xrange(len(self.enemies)):
			collides = self.enemies[i].bounding_box.collidelistall(projectile_rects)
			if len(collides) > 0:
				for j in collides:
					if self.projectiles[j].projectile_type == "FIRE":
						self.enemies[i].receive_damage(self.projectiles[j].damage,self.projectiles[j].damage_type)
						continue
					elif self.projectiles[j].projectile_type == "CLUSTER_BOMB":
						self.soldiers.append(Explosion(self.projectiles[j].position,BOMB_DURATION))
						for enemy in self.enemies:
							if distance(self.projectiles[j].position,enemy.position) <= self.projectiles[j].radius:
								enemy.receive_damage(self.projectiles[j].damage,self.projectiles[j].damage_type)
								self.projectiles[j].isAlive = False
					else:
						self.enemies[i].receive_damage(self.projectiles[j].damage,self.projectiles[j].damage_type)
						self.projectiles[j].isAlive = False
	def remove_entities(self):
		enemies_to_remove = []
		soldiers_to_remove = []
		projectiles_to_remove = []
		towers_to_remove = []
		#this weird xrange is for iterate the list backwards
		# so we dont have index errors later
		for i in xrange(len(self.enemies)-1,-1,-1):
			if not self.enemies[i].isAlive:
				enemies_to_remove.append(i)
		for i in xrange(len(self.soldiers)-1,-1,-1):
			if not self.soldiers[i].isAlive:
				soldiers_to_remove.append(i)
		for i in xrange(len(self.projectiles)-1,-1,-1):
			if not self.projectiles[i].isAlive:
				projectiles_to_remove.append(i)
		for i in xrange(len(self.towers)-1,-1,-1):
			if self.towers[i].isSold:
				towers_to_remove.append(i)
		for enemy_index in enemies_to_remove:
			self.remove_enemy(enemy_index)
		for soldier_index in soldiers_to_remove:
			self.remove_soldier(soldier_index)
		for projectile_index in projectiles_to_remove:
			self.remove_projectile(i)
		for tower_index in towers_to_remove:
			self.remove_tower(tower_index)
	def update_entities(self):
		life_lost = 0
		for enemy in self.enemies:
			enemy.update()
			if not enemy.isAlive:
				self.events.append(("DEATH",enemy.enemy_type,enemy.position.as_tuple(),time.time()))
			elif enemy.reachEnd:
				life_lost += enemy.life_cost
				enemy.isAlive = False
		for soldier in self.soldiers:
			soldier.update(self.enemies)
		for projectile in self.projectiles:
			projectile.update()
		for tower in self.towers:
			if tower.willBeSold:
				tower.isSold = True
			action = tower.update(self.enemies)
			if action == "SHOOT":
				self.n +=1
				if tower.tower_type == ARCHER_TOWER:
					self.add_projectile(Projectile("ARROW",tower.position, self.enemies[tower.target_index],tower.damage))
				elif tower.tower_type == MAGIC_TOWER:
					self.add_projectile(Projectile("MAGIC RAY",tower.position, self.enemies[tower.target_index],tower.damage))
				elif tower.tower_type == ARTILLERY_TOWER:
					self.add_projectile(Projectile("CLUSTER BOMB",tower.position, self.enemies[tower.target_index],tower.damage,tower.area))
			elif action == "SPAWN":
				self.add_soldier(tower.position,tower.position,tower.radius,tower.soldier_life,tower.soldier_damage,tower,True)
		return life_lost
	def update(self):
		if self.check_victory() == "VICTORY":
			return "VICTORY"
		self.events = []
		if self.start_first_wave:
			t0 = time.time()
			if t0 - self.time > self.timers[self.wave_index]:
				self.time = t0
				self.call_next_wave()
			self.add_enemies()
		else:
			self.time = time.time()
		self.remove_entities()
		lives_lost = self.update_entities()
		self.update_collision_manager()
		self.lives -= lives_lost
		return lives_lost
