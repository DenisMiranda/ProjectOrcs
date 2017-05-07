import pygame
from pygame.locals import *
from settings import *
import time
#from sprites import *


pygame.font.init()
def sprite_sheet_loader(file,size,cant = (0,0),pos=(0,0)):
	pygame.display.init()
	len_sprt_x,len_sprt_y = size #sprite size
	sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet
	sheet = pygame.image.load(file).convert_alpha() #Load the sheet
	sheet_rect = sheet.get_rect()
	sprites = []
	columns = cant[0]

	rows = cant[1]
	for i in range(rows):#rows
		for i in range(columns):#columns+--+
			rect = pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)
			sheet.set_clip(rect) #find sprite you want
			sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
			sprites.append(sprite)
			sprt_rect_x += len_sprt_x
		sprt_rect_y += len_sprt_y
		sprt_rect_x = 0
	return sprites
def blit_sprite(screen,sprite,pos):
	blit_position = (pos.x - sprite.get_width()/2, pos.y - sprite.get_height()/2)
	screen.blit(sprite, blit_position)
def blit_background(screen,background,rect):
	try:
		surface = background.subsurface(rect)
		screen.blit(surface,rect)
	except ValueError:
		rect = rect.clamp(screen.get_rect())
		surface = background.subsurface(rect)
		screen.blit(surface,rect)

class Gameplay_render():
	def __init__(self,background):
		self.font = pygame.font.Font(None,22)
		self.level_dic = {0:self.font.render("0",True,(255,255,255)),
					 1:self.font.render("1",True,(255,255,255)),
					 2:self.font.render("2",True,(255,255,255)),
					 3:self.font.render("3",True,(255,255,255))}
		self.background = pygame.image.load(background).convert()
		self.rects = []
		self.FX_list = []
		self.c = 0
		self.tower_icons = {ARCHER_TOWER:pygame.image.load("graphics/archer_icon.png").convert(),
							MAGIC_TOWER :pygame.image.load("graphics/magic_icon.png").convert(),
							ARTILLERY_TOWER:pygame.image.load("graphics/artillery_icon.png").convert(),
							BARRACK_TOWER:pygame.image.load("graphics/barrack_icon.png").convert()}
		for key,value in self.tower_icons.items():
			self.tower_icons[key]= pygame.transform.scale(self.tower_icons[key],(32,32))
	def render_static_items(self,screen,tower_placements,entry_points,bases_pos):
		placement = pygame.image.load("graphics/placement.png")
		base = pygame.image.load("graphics/start_point.png")
		entry_point = pygame.image.load("graphics/end_point.png")
		rect_ = placement.get_rect()
		x,y = rect_.size
		placement = pygame.transform.scale(placement, (int(x*0.7), int(y*0.7)))
		rect = placement.get_rect()
		for i in tower_placements:
			rect.center = i.as_tuple()
			self.background.blit(placement,rect)
		for i in entry_points:
			rect.center = i.as_tuple()
			self.background.blit(entry_point,rect)
		for i in bases_pos:
			rect.center = i.as_tuple()
			self.background.blit(base,rect)
		hud = pygame.image.load("graphics/hud.png")
		self.background.blit(hud,(0,0))
		screen.blit(self.background,(0,0))
	def render_hud(self,screen,manager):
		blit_background(screen,self.background,pygame.Rect((150,500),(235,30)))
		screen.blit(self.font.render(str(manager.lives),True,(255,255,255)),(213,505))
		screen.blit(self.font.render(str(manager.money),True,(255,255,255)),(298,505))
		screen.blit(self.font.render("WAVE:"+str(manager.wave_index+1)+"/"+str(manager.wave_num),True,(255,255,255)),(350,505))
		blit_background(screen,self.background,Rect(870,512,100,50))
		screen.blit(self.font.render("COST: "+str(TOWERS_COST[manager.act_tower]),True,(255,255,255)),(872,512))
		#screen.blit(self.font.render("COST: "+str(TOWERS_COST[manager.act_tower]),
		#							True,(254,254,254),(780,512)))
		blit_background(screen,self.background,Rect(787,512,35,10))
		blit_background(screen,self.background,Rect(830,512,35,10))
		max_width = 35
		progress = (time.time() - manager.last_reinforcements_call)/REINFORCEMENTS_COOLDOWN
		progress_fire = (time.time() - manager.last_fire_call)/FIRE_STORM_COOLDOWN
		if progress >= 1.0:
			pygame.draw.rect(screen, manager.call_reinforcements_color, Rect(787,512,35,10))
		else:
			rein_bar_rect = pygame.Rect(787,512,max_width*progress,10)
			screen.fill((90,20,20), rein_bar_rect)
		if progress_fire >= 1.0:
			pygame.draw.rect(screen,manager.fire_rain_color,Rect(834,512,35,10))
		else:
			rein_bar_rect = pygame.Rect(830,512,max_width*progress_fire,10)
			screen.fill((90,20,20), rein_bar_rect)
		screen.blit(self.tower_icons[manager.act_tower],(878,475))
		self.rects.append(pygame.Rect(874,475,35,35))
		self.rects.append(pygame.Rect(830,512,35,10))
		self.rects.append(pygame.Rect(787,512,35,10))
		self.rects.append(pygame.Rect(0,0,200,200))
		self.rects.append(pygame.Rect(870,512,50,15))

	def draw_background(self,screen):
		screen.blit(self.background,(0,0))
		#pygame.display.flip()
	def blit_background(self,screen,enemies,projectiles,soldiers,towers):
		for enemy in enemies:
			blit_background(screen,self.background,enemy.old_rect)
			self.rects.append(enemy.old_rect)
		for projectile in projectiles:
			blit_background(screen,self.background,projectile.old_rect)
			self.rects.append(projectile.old_rect)
		for soldier in soldiers:
			blit_background(screen,self.background,soldier.old_rect)
			self.rects.append(soldier.old_rect)
		for tower in towers:
			#if tower.isSold:
			blit_background(screen,self.background,tower.rect)
			self.rects.append(tower.rect)
	def blit_enemies(self,screen,enemies):
		#rects = [pygame.Rect(enemy.position.as_tuple(),(10,10)) for enemy in enemies]
		for enemy in enemies:
			if enemy.isAlive:
				n = int(enemy.time_alive/0.2)%10
				screen.blit(enemy.get_representation(),enemy.rect)
				self.rects.append(enemy.rect)
	def blit_soldiers(self,screen,soldiers):
			for soldier in soldiers:
				if soldier.isAlive:
					screen.blit(soldier.get_representation(),soldier.rect)

	def blit_towers(self,screen,towers):
		#rects = [pygame.Rect(tower.position.as_tuple(),(20,20)) for tower in towers]
		for tower in towers:
			if not tower.isSold:
				#pygame.draw.circle(screen,(120,0,0),tower.rect.center,tower.radius,1)
				blit_sprite(screen,tower.get_representation(),tower.position)
				self.rects.append(tower.rect)
				if tower.IsHighlighted:
					pygame.draw.rect(screen,(150,30,40),tower.rect.inflate(-5,-5),2)
				screen.blit(self.level_dic[tower.level],tower.rect)

	def blit_projectile(self,screen,projectiles):
		#rects = [pygame.Rect(bullet.position.as_tuple(),(3,3)) for bullet in projectiles]
			for projectile in projectiles:
				if projectile.isAlive:
					screen.blit(projectile.get_representation(),projectile.rect)
					self.rects.append(projectile.rect)
	def retrieve_FX(self,manager):
		"""An effect is a list where the first element is the effect animation
			the second is the position  as a rect and then other elements are auxiliries"""
		FXs = manager.events
		for FX in FXs:
			if FX[0] == "EXPLOSION":
				pos = (int(FX[1].x),int(FX[1].y))
				pygame.draw.circle(screen,(120,100,130),pos,FX[2],0)
			elif FX[0] == "DEATH":
				self.FX_list.append((FX[1],FX[2]))
	def blit_FX(self,screen):
		for FX in self.FX_list:
			screen.blit(FX[0].get_current_frame(1),FX[2])

	def draw_entities(self,screen, manager):
		#c = 0
		#d = {0:(255,255,255),1:(128,0,0),2:(0,128,0),3:(0,0,128),4:(128,128,0),5:(0,128,128)}
		#for path in manager.paths:
		#	for i in path.nodes:
		#		pygame.draw.circle(screen,d[c],(int(i.x),int(i.y)),2)
		#	c += 1

		self.blit_towers(screen,manager.towers)
		self.blit_enemies(screen,manager.enemies)
		self.blit_soldiers(screen,manager.soldiers)
		self.blit_projectile(screen,manager.projectiles)
		self.render_hud(screen,manager)
		pygame.display.flip()
		if self.c == 100:
			screen.blit(self.background,(0,0))
			self.c = 0
		else:
			self.blit_background(screen,manager.enemies,manager.projectiles,manager.soldiers,manager.towers)
		#self.retrieve_FX(manager)
		#self.blit_FX(screen)
		#self.blit_FX(screen,manager)
		# if self.frame_counter > 10:
		# 	pygame.display.flip()
		# 	return 0
		# self.frame_counter+=1
		#pygame.display.update(self.rects)
		self.rects = []
		self.c+=1
