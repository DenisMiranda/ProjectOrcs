import pygame
from pygame.locals import *
import sys, random
from path_following import Path
from render import blit_sprite
from collections import OrderedDict
from settings import *

def unique_everseen(seq):
	unique = []
	a =  [unique.append(item) for item in seq if item not in unique]
	print a
	print
	return a
pygame.init()
Clock = pygame.time.Clock()
height = 960
width = 540
screen = pygame.display.set_mode((height, width))
from enemies import *
path_ = Path([])
tower_placements = []
fondo = pygame.image.load("graphics/mapa_5.png").convert()
run = True
start = False
targets_i = []
targets_f = []
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			#path_.nodes = tuple(unique_everseen(path_.nodes))
			print path_
			print tower_placements
			print targets_i, "inicio"
			print targets_f, "final"
			quit()
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			x, y = event.pos
			path_.add_node((x,y))
		if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
			x, y = pygame.mouse.get_pos()
			tower_placements.append((x,y))
		if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
			try:
				path_.pop_node()
			except IndexError:
				pass
		if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
			try:
				tower_placements.pop()
			except IndexError:
				pass
		if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
			x, y = pygame.mouse.get_pos()
			targets_i.append((x,y))
		if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
			x, y = pygame.mouse.get_pos()
			targets_f.append((x,y))
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			run = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
			start = not start
	if start:
		path_.add_node((pygame.mouse.get_pos()))
	screen.blit(fondo,(0,0))
	for i in path_.nodes:
		pygame.draw.circle(screen,(255,255,255),(i.x,i.y),4)
	for i in tower_placements:
		pygame.draw.circle(screen,(0,30,128),i,25)
	for i in targets_i:
		pygame.draw.circle(screen,(255,0,0),i,25)
	for i in targets_f:
		pygame.draw.circle(screen,(0,120,0),i,25)
	pygame.display.flip()
	Clock.tick(60)
	#print Clock.get_fps()

enemy = Enemy(basic_enemy_breed,path_)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			#enemy.path.nodes = tuple(unique_everseen(enemy.path.nodes))
			print tower_placements
			print enemy.path
			quit()
	try:
		enemy.update()
	except TypeError:
		enemy.node_index = 0
	screen.blit(fondo,(0,0))
	for i in enemy.path.nodes:
		pygame.draw.circle(screen,(255,255,255),(i.x,i.y),2)
	screen.blit(enemy.get_representation(),enemy.rect)
	pygame.display.flip()
	Clock.tick(60)
