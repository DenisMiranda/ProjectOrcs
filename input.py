import pygame
from settings import *
from vector import *
from fire_storm import FireStorm
import time
class Input():
	def __init__(self):
		self.tower_type = ARCHER_TOWER
		self.last_reinforcements_call = time.time() + REINFORCEMENTS_COOLDOWN
		self.reinforcements_icon = pygame.Rect((789,475),(35,35))
		self.fire_rain_icon = pygame.Rect((835,475),(35,35))
		self.font = font_body = pygame.font.SysFont("Algerian",50)
	def handle_input(self,manager):
		manager.act_tower = self.tower_type
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				pass;#time.sleep(8)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				return "quit"
			if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
				self.tower_type = ARCHER_TOWER
			if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
				self.tower_type = MAGIC_TOWER
			if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
				self.tower_type = ARTILLERY_TOWER
			if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
				self.tower_type = BARRACK_TOWER
			if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
				if manager.start_first_wave:
					manager.call_next_wave()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
				manager.money += 100
			if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
				pos = pygame.mouse.get_pos()
				pos = Vec2D(pos[0],pos[1])
				manager.add_soldier(pos,pos,REINFORCEMENTS_RADIUS,REINFORCEMENTS_LIFE,REINFORCEMENTS_DAMAGE)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
				pos = pygame.mouse.get_pos()
				pos = Vec2D(pos[0],pos[1])
				manager.add_projectile(FireStorm(pos,FIRE_STORM_DURATION,FIRE_STORM_DAMAGE))
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				manager.start_first_wave = True
				print "start first wave"
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				x,y = event.pos
				pos = Vec2D(x,y)
				if manager.call_reinforcements:
					manager.add_soldier(pos,pos,REINFORCEMENTS_RADIUS,REINFORCEMENTS_LIFE,REINFORCEMENTS_DAMAGE)
					manager.call_reinforcements = False
					manager.call_reinforcements_color = (0,120,20)
				if manager.fire_rain:
					manager.add_projectile(FireStorm(pos,FIRE_STORM_DURATION,FIRE_STORM_DAMAGE))
					manager.fire_rain = False
					manager.fire_rain_color = (0,120,20)
				if self.reinforcements_icon.collidepoint(x,y):
					manager.call_reinforcements = not manager.call_reinforcements
					manager.call_reinforcements_color = (255,215,0)
				if self.fire_rain_icon.collidepoint(x,y):
					manager.fire_rain = not manager.fire_rain
					manager.fire_rain_color = (255,215,0)
				for i in xrange(len(manager.towers)):
					manager.towers[i].IsHighlighted = False
					if manager.towers[i].rect.collidepoint(x,y):
						manager.towers[i].IsHighlighted = True
						return 1
				manager.add_tower(self.tower_type,Vec2D(x,y))
				return 0
			if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
				for i in xrange(len(manager.towers)):
					if manager.towers[i].IsHighlighted == True:
						manager.sell_tower(i)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
				for i in xrange(len(manager.towers)):
					if manager.towers[i].IsHighlighted == True:
						manager.upgrade_tower(i)
