import pygame
from render import sprite_sheet_loader

class Animation:
	def __init__(self,frames = None,time = 0.2):
		if frames == None:
			self.frames = []
			self.length = 0
		else:
			self.frames = frames
			self.length = len(frames)
		self.counter = 0
		self.refresh_rate = 10
		self.current_frame = 0
	def add_frame(self,frame):
		self.frames.append(frame)
	def get_frame(self,frame_index):
		return self.frames[frame_index]
	def flip(self,x_bool,y_bool):
		frames = []
		for frame in self.frames:
			frames.append(pygame.transform.flip(frame,x_bool,y_bool))
		return Animation(frames)
	def scale(self,factor):
		frames = []
		for frame in self.frames:
			x,y = frame.get_rect().size
			frames.append(pygame.transform.smoothscale(frame,(int(x*factor),int(y*factor))))
		return Animation(frames)
	def get_current_frame(self,time_alive):
		return self.frames[int(time_alive/0.1)%self.length]
	def get_next_frame(self):
		return self.frames[self.current_frame]
		self.update()
	def update(self):
		self.counter += 1
		if self.counter%self.lenght == 0:
			self.current_frame = (self.current_frame+1)%self.length
		if self.counter > self.refresh_rate*self.length:
			return None

class Animation_manager:
	def __init__(self,path,frame_size,cant, start_pos = (0,0)):
		self.sprites = sprite_sheet_loader(path,frame_size,cant,start_pos)
		self.animation_dic = {}
		self.last_animation = ""
	def get_animation(self,name):
		return self.animation_dic[name]
	def add_animation(self,name,animation):
		self.animation_dic[name] = animation
		self.last_animation = name
	def add_animation_by_frames(self,name,frames):
		sprite_list = []
		for i in frames:
			sprite_list.append(self.sprites[i])
		self.animation_dic[name] = Animation(sprite_list)
	def scale(self,factor):
		for key in self.animation_dic.keys():
			self.animation_dic[key] = self.animation_dic[key].scale(factor)
	def get_current_frame(self,animation_name):
		return self.animation_dic[animation_name].get_current_frame()
	def update(self,time_alive):
		for key in self.animation_dic.keys():
			self.animation_dic[key].update(time_alive)

##########################################
basic_enemy_animations = Animation_manager("graphics/basic_enemy_sprites.png",(76,55),(5,11))
basic_enemy_animations.add_animation_by_frames("walking_up",(0,5,10,15,20))
basic_enemy_animations.add_animation_by_frames("walking_right_up",(1,6,11,16,21))
basic_enemy_animations.add_animation_by_frames("walking_right",(2,7,12,17,22))
basic_enemy_animations.add_animation_by_frames("walking_right_down",(3,8,13,18,23))
basic_enemy_animations.add_animation_by_frames("walking_down",(4,9,14,19,24))
walking_left_down_anim = basic_enemy_animations.get_animation("walking_right_down").flip(1,0)
basic_enemy_animations.add_animation("walking_left_down",walking_left_down_anim)
walking_left_anim = basic_enemy_animations.get_animation("walking_right").flip(1,0)
basic_enemy_animations.add_animation("walking_left",walking_left_anim)
walking_left_up_anim = basic_enemy_animations.get_animation("walking_right_up").flip(1,0)
basic_enemy_animations.add_animation("walking_left_up",walking_left_up_anim)
############basic enemy fighting animations
basic_enemy_animations.add_animation_by_frames("fighting_up",(25,30,35,40))
basic_enemy_animations.add_animation_by_frames("fighting_right_up",(26,31,36,41))
basic_enemy_animations.add_animation_by_frames("fighting_right",(27,32,37,42))
basic_enemy_animations.add_animation_by_frames("fighting_right_down",(28,33,38,43))
basic_enemy_animations.add_animation_by_frames("fighting_down",(29,34,39,44))
fighting_left_down_anim = basic_enemy_animations.get_animation("fighting_right_down").flip(1,0)
basic_enemy_animations.add_animation("fighting_left_down",fighting_left_down_anim)
fighting_left_anim = basic_enemy_animations.get_animation("fighting_right").flip(1,0)
basic_enemy_animations.add_animation("fighting_left",fighting_left_anim)
fighting_left_up_anim = basic_enemy_animations.get_animation("fighting_right_up").flip(1,0)
basic_enemy_animations.add_animation("fighting_left_up",fighting_left_up_anim)
basic_enemy_animations.add_animation_by_frames("dead",(45,46,47,48,49))
#############################################################################
skeleton_enemy_animations = Animation_manager("graphics/skeleton_sprites.png",(61,48),(5,10))
skeleton_enemy_animations.add_animation_by_frames("walking_up",(0,5,10,15,20))
skeleton_enemy_animations.add_animation_by_frames("walking_right_up",(1,6,11,16,21))
skeleton_enemy_animations.add_animation_by_frames("walking_right",(2,7,12,17,22))
skeleton_enemy_animations.add_animation_by_frames("walking_right_down",(3,8,13,18,23))
skeleton_enemy_animations.add_animation_by_frames("walking_down",(4,9,14,19,24))
walking_left_down_anim = skeleton_enemy_animations.get_animation("walking_right_down").flip(1,0)
skeleton_enemy_animations.add_animation("walking_left_down",walking_left_down_anim)
walking_left_anim = skeleton_enemy_animations.get_animation("walking_right").flip(1,0)
skeleton_enemy_animations.add_animation("walking_left",walking_left_anim)
walking_left_up_anim = skeleton_enemy_animations.get_animation("walking_right_up").flip(1,0)
skeleton_enemy_animations.add_animation("walking_left_up",walking_left_up_anim)
############basic enemy fighting animations
skeleton_enemy_animations.add_animation_by_frames("fighting_up",(25,30,35,40))
skeleton_enemy_animations.add_animation_by_frames("fighting_right_up",(26,31,36,41))
skeleton_enemy_animations.add_animation_by_frames("fighting_right",(27,32,37,42))
skeleton_enemy_animations.add_animation_by_frames("fighting_right_down",(28,33,38,43))
skeleton_enemy_animations.add_animation_by_frames("fighting_down",(29,34,39,44))
fighting_left_down_anim = skeleton_enemy_animations.get_animation("fighting_right_down").flip(1,0)
skeleton_enemy_animations.add_animation("fighting_left_down",fighting_left_down_anim)
fighting_left_anim = skeleton_enemy_animations.get_animation("fighting_right").flip(1,0)
skeleton_enemy_animations.add_animation("fighting_left",fighting_left_anim)
fighting_left_up_anim = skeleton_enemy_animations.get_animation("fighting_right_up").flip(1,0)
skeleton_enemy_animations.add_animation("fighting_left_up",fighting_left_up_anim)
skeleton_enemy_animations.add_animation_by_frames("dead",(45,46,47,48,49))

####################################################################

armored_enemy_animations = Animation_manager("graphics/armored_enemy_sprites.png",(74,73),(5,11))
armored_enemy_animations.add_animation_by_frames("walking_up",(0,5,10,15,20))
armored_enemy_animations.add_animation_by_frames("walking_right_up",(1,6,11,16,21))
armored_enemy_animations.add_animation_by_frames("walking_right",(2,7,12,17,22))
armored_enemy_animations.add_animation_by_frames("walking_right_down",(3,8,13,18,23))
armored_enemy_animations.add_animation_by_frames("walking_down",(4,9,14,19,24))
walking_left_down_anim = armored_enemy_animations.get_animation("walking_right_down").flip(1,0)
armored_enemy_animations.add_animation("walking_left_down",walking_left_down_anim)
walking_left_anim = armored_enemy_animations.get_animation("walking_right").flip(1,0)
armored_enemy_animations.add_animation("walking_left",walking_left_anim)
walking_left_up_anim = armored_enemy_animations.get_animation("walking_right_up").flip(1,0)
armored_enemy_animations.add_animation("walking_left_up",walking_left_up_anim)
############armored enemy fighting animations
armored_enemy_animations.add_animation_by_frames("fighting_up",(25,30,35,40))
armored_enemy_animations.add_animation_by_frames("fighting_right_up",(26,31,36,41))
armored_enemy_animations.add_animation_by_frames("fighting_right",(27,32,37,42))
armored_enemy_animations.add_animation_by_frames("fighting_right_down",(28,33,38,43))
armored_enemy_animations.add_animation_by_frames("fighting_down",(29,34,39,44))
fighting_left_down_anim = armored_enemy_animations.get_animation("fighting_right_down").flip(1,0)
armored_enemy_animations.add_animation("fighting_left_down",fighting_left_down_anim)
fighting_left_anim = armored_enemy_animations.get_animation("fighting_right").flip(1,0)
armored_enemy_animations.add_animation("fighting_left",fighting_left_anim)
fighting_left_up_anim = armored_enemy_animations.get_animation("fighting_right_up").flip(1,0)
armored_enemy_animations.add_animation("fighting_left_up",fighting_left_up_anim)
armored_enemy_animations.add_animation_by_frames("dead",(50,51,47,48))
#skeleton_enemy_animations.scale(0.6)
########################################
fast_enemy_animations = Animation_manager("graphics/fast_enemy_sprites.png",(67,67),(5,10))
fast_enemy_animations.add_animation_by_frames("walking_up",(0,5,10,15,20))
fast_enemy_animations.add_animation_by_frames("walking_right_up",(1,6,11,16,21))
fast_enemy_animations.add_animation_by_frames("walking_right",(2,7,12,17,22))
fast_enemy_animations.add_animation_by_frames("walking_right_down",(3,8,13,18,23))
fast_enemy_animations.add_animation_by_frames("walking_down",(4,9,14,19,24))
walking_left_down_anim = fast_enemy_animations.get_animation("walking_right_down").flip(1,0)
fast_enemy_animations.add_animation("walking_left_down",walking_left_down_anim)
walking_left_anim = fast_enemy_animations.get_animation("walking_right").flip(1,0)
fast_enemy_animations.add_animation("walking_left",walking_left_anim)
walking_left_up_anim = fast_enemy_animations.get_animation("walking_right_up").flip(1,0)
fast_enemy_animations.add_animation("walking_left_up",walking_left_up_anim)
############basic enemy fighting animations
fast_enemy_animations.add_animation_by_frames("fighting_up",(25,30,35,40))
fast_enemy_animations.add_animation_by_frames("fighting_right_up",(26,31,36,41))
fast_enemy_animations.add_animation_by_frames("fighting_right",(27,32,37,42))
fast_enemy_animations.add_animation_by_frames("fighting_right_down",(28,33,38,43))
fast_enemy_animations.add_animation_by_frames("fighting_down",(29,34,39,44))
fighting_left_down_anim = fast_enemy_animations.get_animation("fighting_right_down").flip(1,0)
fast_enemy_animations.add_animation("fighting_left_down",fighting_left_down_anim)
fighting_left_anim = fast_enemy_animations.get_animation("fighting_right").flip(1,0)
fast_enemy_animations.add_animation("fighting_left",fighting_left_anim)
fighting_left_up_anim = fast_enemy_animations.get_animation("fighting_right_up").flip(1,0)
fast_enemy_animations.add_animation("fighting_left_up",fighting_left_up_anim)
fast_enemy_animations.add_animation_by_frames("dead",(45,46,47,48,49))
#fast_enemy_animations.scale(0.6)
##################################################333

boss_enemy_animations = Animation_manager("graphics/boss.png",(89,83),(5,6))
boss_enemy_animations.add_animation_by_frames("walking_up",(0,5,10,15))
boss_enemy_animations.add_animation_by_frames("walking_right_up",(1,6,11,16))
boss_enemy_animations.add_animation_by_frames("walking_right",(2,7,12,17))
boss_enemy_animations.add_animation_by_frames("walking_right_down",(3,8,13,18))
boss_enemy_animations.add_animation_by_frames("walking_down",(4,9,14,19))
walking_left_down_anim = boss_enemy_animations.get_animation("walking_right_down").flip(1,0)
boss_enemy_animations.add_animation("walking_left_down",walking_left_down_anim)
walking_left_anim = boss_enemy_animations.get_animation("walking_right").flip(1,0)
boss_enemy_animations.add_animation("walking_left",walking_left_anim)
walking_left_up_anim = boss_enemy_animations.get_animation("walking_right_up").flip(1,0)
boss_enemy_animations.add_animation("walking_left_up",walking_left_up_anim)
############basic enemy fighting animations
boss_enemy_animations.add_animation_by_frames("fighting_up",(20,))
boss_enemy_animations.add_animation_by_frames("fighting_right_up",(21,))
boss_enemy_animations.add_animation_by_frames("fighting_right",(22,))
boss_enemy_animations.add_animation_by_frames("fighting_right_down",(23,))
boss_enemy_animations.add_animation_by_frames("fighting_down",(24,))
fighting_left_down_anim = boss_enemy_animations.get_animation("fighting_right_down").flip(1,0)
boss_enemy_animations.add_animation("fighting_left_down",fighting_left_down_anim)
fighting_left_anim = boss_enemy_animations.get_animation("fighting_right").flip(1,0)
boss_enemy_animations.add_animation("fighting_left",fighting_left_anim)
fighting_left_up_anim = boss_enemy_animations.get_animation("fighting_right_up").flip(1,0)
boss_enemy_animations.add_animation("fighting_left_up",fighting_left_up_anim)
boss_enemy_animations.add_animation_by_frames("dead",(25,26,27,28,29))
boss_enemy_animations.scale(2.5)


soldier_animations = Animation_manager("graphics/soldier_sprites.png",(74,56),(5,11))
soldier_animations.add_animation_by_frames("walking_up",(0,5,10,15,20))
soldier_animations.add_animation_by_frames("walking_right_up",(1,6,11,16,21))
soldier_animations.add_animation_by_frames("walking_right",(2,7,12,17,22))
soldier_animations.add_animation_by_frames("walking_right_down",(3,8,13,18,23))
soldier_animations.add_animation_by_frames("walking_down",(4,9,14,19,24))
walking_left_down_anim = soldier_animations.get_animation("walking_right_down").flip(1,0)
soldier_animations.add_animation("walking_left_down",walking_left_down_anim)
walking_left_anim = soldier_animations.get_animation("walking_right").flip(1,0)
soldier_animations.add_animation("walking_left",walking_left_anim)
walking_left_up_anim = soldier_animations.get_animation("walking_right_up").flip(1,0)
soldier_animations.add_animation("walking_left_up",walking_left_up_anim)
############soldier fighting animations
soldier_animations.add_animation_by_frames("fighting_up",(25,30,35,40))
soldier_animations.add_animation_by_frames("fighting_right_up",(26,31,36,41))
soldier_animations.add_animation_by_frames("fighting_right",(27,32,37,42))
soldier_animations.add_animation_by_frames("fighting_right_down",(28,33,38,43))
soldier_animations.add_animation_by_frames("fighting_down",(29,34,39,44))
fighting_left_down_anim = soldier_animations.get_animation("fighting_right_down").flip(1,0)
soldier_animations.add_animation("fighting_left_down",fighting_left_down_anim)
fighting_left_anim = soldier_animations.get_animation("fighting_right").flip(1,0)
soldier_animations.add_animation("fighting_left",fighting_left_anim)
fighting_left_up_anim = soldier_animations.get_animation("fighting_right_up").flip(1,0)
soldier_animations.add_animation("fighting_left_up",fighting_left_up_anim)
################################### tower

artillery_tower_animation = Animation_manager("graphics/artillery_towers.png",(170,170),(3,1))
artillery_tower_animation.add_animation_by_frames("standing0",(0,))
artillery_tower_animation.add_animation_by_frames("standing1",(1,))
artillery_tower_animation.add_animation_by_frames("standing2",(2,))
artillery_tower_animation.scale(0.7)

magic_tower_animation = Animation_manager("graphics/hres_mage_tower.png",(300,550),(3,1))
magic_tower_animation.add_animation_by_frames("standing0",(0,))
magic_tower_animation.add_animation_by_frames("standing1",(1,))
magic_tower_animation.add_animation_by_frames("standing2",(2,))
magic_tower_animation.scale(0.3)

archer_tower_animation = Animation_manager("graphics/archer_towers.png",(124,155),(3,1))
archer_tower_animation.add_animation_by_frames("standing0",(0,))
archer_tower_animation.add_animation_by_frames("standing1",(1,))
archer_tower_animation.add_animation_by_frames("standing2",(2,))
archer_tower_animation.scale(0.65)

barrack_tower_animation = Animation_manager("graphics/barracks.png",(128,143),(4,1))
barrack_tower_animation.add_animation_by_frames("standing0",(0,))
barrack_tower_animation.add_animation_by_frames("standing1",(1,))
barrack_tower_animation.add_animation_by_frames("standing2",(2,))
barrack_tower_animation.add_animation_by_frames("standing3",(3,))
######################3projectiles
firep_animation = Animation_manager("graphics/fire_p.png",(20,17),(1,1))
firep_animation.add_animation_by_frames("traveling",(0,))

fireb_animation = Animation_manager("graphics/fire_b.png",(13,13),(1,1))
fireb_animation.add_animation_by_frames("traveling",(0,))

magic_missile_animation = Animation_manager("graphics/magic_missile.png",(20,20),(1,1))
magic_missile_animation.add_animation_by_frames("traveling",(0,))

fire_storm_animation = Animation_manager("graphics/fire.png",(56,54),(5,2))
fire_storm_animation.add_animation_by_frames("fire",(0,1,2,3,4,5,6,7,8,9))
fire_storm_animation.scale(1.7)

explosion_animation = Animation_manager("graphics/projectiles.png",(65,71),(16,1),(3,166))
explosion_animation.add_animation_by_frames("explosion",(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15))
explosion_animation.scale(1.6)
############################ FX


