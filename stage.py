from input import Input
import pygame
from life_cycle_manager import Life_cycle_manager
from render import Gameplay_render
import settings
class Stage:
	def __init__(self,stage_data,screen):
		screen.blit(pygame.image.load("graphics/loading_screen.png"),(0,0))
		pygame.display.flip()
		self.waves = stage_data.waves
		self.paths = stage_data.paths
		self.background = stage_data.background
		self.tower_placements = stage_data.tower_placements
		self.entry_points = stage_data.entry_points
		self.bases_pos = stage_data.bases_pos
		self.starting_money = stage_data.starting_money
		self.timers = stage_data.timers
		self.lives = stage_data.starting_lives
		self.input = Input()
		self.life_cycle_manager = Life_cycle_manager(self.waves,self.paths,self.starting_money,self.lives,self.tower_placements,self.timers)
		self.render = Gameplay_render(self.background)
		self.render.render_static_items(screen,self.tower_placements,self.entry_points,self.bases_pos)
		self.music = stage_data.music
		self.sounds = {"horn":pygame.mixer.Sound("sounds/horn.ogg"),
						"theme":pygame.mixer.Sound(self.music),
						"battle": pygame.mixer.Sound("sounds/battle.ogg"),
						"fire":pygame.mixer.Sound("sounds/fire.ogg"),
						"error":pygame.mixer.Sound("sounds/error.ogg")}
		stage_data.waves = []
		for wave_file in stage_data.wave_files:
			stage_data.add_wave(wave_file,True)
		self.sounds["theme"].set_volume(settings.MAIN_VOLUME/10.0)
		pygame.display.flip()
		self.sounds["theme"].play(-1)
	def update(self,screen):
		if len(self.life_cycle_manager.sounds) > 0:
			self.sounds[self.life_cycle_manager.sounds.pop()].play(0)
		if self.input.handle_input(self.life_cycle_manager) == "quit":
			print "out"
			return -1
		lfc = self.life_cycle_manager.update()
		if (lfc == "VICTORY"):
			return 1
		self.lives -= lfc
		self.render.draw_entities(screen,self.life_cycle_manager)
		if self.lives <= 0:
			return -1
		else:
			return 0
	def draw(self,screen):
		#self.render.draw_background(screen)
		self.render.draw_entities(screen,self.life_cycle_manager)
