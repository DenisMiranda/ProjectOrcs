import pygame
import settings

pygame.init()
if settings.FULL_SCREEN:
	screen = pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT),pygame.FULLSCREEN|pygame.HWSURFACE)
else:
	screen = pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT))
from stage import Stage
import stage_data

test_stage = Stage(stage_data.one_stage_data,screen)
test_stage.render.draw_background(screen)
Clock = pygame.time.Clock()
pygame.display.flip()
while True:
	result = test_stage.update(screen)
	if result == -1:
		print "GAME OVER"
		break	
	elif result == 1:
		print "VICTORY"
		break
	Clock.tick(settings.FRAME_RATE)
	#print Clock.get_fps()