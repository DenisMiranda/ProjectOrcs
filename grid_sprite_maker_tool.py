import pygame
import render
from ast import literal_eval
import time
pygame.init()
sprite_sheet = pygame.image.load("graphics/skeleton_sprites.png")
rect = sprite_sheet.get_rect()
screen = pygame.display.set_mode((rect.size[0]+20,rect.size[1]+20))
from animations import *
greed_size = (100,100)
start_pos = (0,0)

#for i in xrange(16):
#	screen.fill((0,0,0))
#	screen.blit(explosion_animation.get_animation("explosion").frames[i],(0,0))
#	pygame.display.flip()
#	time.sleep(1)


def draw_greed(greed_size,start_pos):
	rect = pygame.Rect(start_pos,greed_size)
	for i in xrange(greed_size[0]):
		for j in xrange(greed_size[1]):
			pygame.draw.rect(screen,(128,0,0),rect,1)
			rect.move_ip(greed_size[0],0)
		#rect = pygame.Rect((start_pos[0],greed_size[1]*(i+1)),greed_size)
		rect = pygame.Rect((start_pos[0],start_pos[1] + greed_size[1]*(i+1)),greed_size)
Clock = pygame.time.Clock()
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
			greed_size = literal_eval(raw_input("GREED SIZE > "))
			print greed_size,start_pos
		if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
			start_pos = literal_eval(raw_input("START POS > "))
			print greed_size,start_pos
	screen.fill((0,0,0))
	pygame.draw.rect(screen,(255,255,255),rect,1)
	screen.blit(sprite_sheet,(0,0))
	draw_greed(greed_size,start_pos)
	print greed_size,start_pos
	pygame.display.flip()
	Clock.tick(1000)
	#print Clock.get_fps()
