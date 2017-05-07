# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 13:28:04 2016

@author: Marcelo
"""
import pygame
import settings

pygame.init()

if settings.FULL_SCREEN:
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT),pygame.FULLSCREEN|pygame.HWSURFACE)
else:
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT))

from stage import Stage
import stage_data
font_title = pygame.font.Font("Heavy_Gothik.ttf",60)
font_body = pygame.font.SysFont("Algerian",50)
error_sound = pygame.mixer.Sound("sounds/error.ogg")
def objectText(text, color, sice):
    if sice == "body":
        screenText = font_body.render(text, True, color)
    if sice == "title":
        screenText = font_title.render(text, True, color)
    return screenText, screenText.get_rect()

def message(mesg, color, sice="body", posx=0, posy=0):
    screenText, textRect = objectText(mesg, color, sice)
    textRect.center = posx, posy
    screen.blit(screenText, textRect)
    return textRect


class TitleScreen:
    def __init__(self):
        self.background = pygame.image.load("graphics/title_screen_background.jpg")
    def run(self, screen, state, clock):
        self.state = state
        self.clock = clock
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    quit()
            if pygame.mouse.get_pressed()[0]:
                    self.state = "STAGESCREEN"
                         
        screen.blit(self.background,(0,0))
        message("Project Orcs", (255,106,0,), "title", settings.SCREEN_WIDTH*0.5, settings.SCREEN_HEIGHT*0.2)
        message("Click to start", (255,106,0), "body", settings.SCREEN_WIDTH*0.5, settings.SCREEN_HEIGHT*0.6)
        pygame.display.update()
        self.clock.tick(15)
        return self.state

class StageScreen:
    def __init__(self):
        self.background = pygame.image.load("graphics/title_screen_background.jpg")
        self.location = [0.25, 0.5, 0.75, 0.35, 0.65, 0.9, 0.4, 0.4, 0.4, 0.7, 0.7, 0.9]
        self.level = 0
        self.color_dict = {False:(128,128,128),True:(255,106,0)}
    def run(self, screen, state, clock):
        self.state = state
        self.clock = clock
        screen.blit(self.background,(0,0))
        message("Select Stage:",(255,106,0,),"title", settings.SCREEN_WIDTH*0.5, settings.SCREEN_HEIGHT*0.1)
        self.m_S1 = message("Stage 1",(255,106,0,), "body", settings.SCREEN_WIDTH*self.location[0], settings.SCREEN_HEIGHT*self.location[6])
        self.m_S2 = message("Stage 2",self.color_dict[save>=1], "body", settings.SCREEN_WIDTH*self.location[1], settings.SCREEN_HEIGHT*self.location[7])
        self.m_S3 = message("Stage 3",self.color_dict[save>=2], "body", settings.SCREEN_WIDTH*self.location[2], settings.SCREEN_HEIGHT*self.location[8])
        self.m_S4 = message("Stage 4",self.color_dict[save>=3], "body", settings.SCREEN_WIDTH*self.location[3], settings.SCREEN_HEIGHT*self.location[9])
        self.m_S5 = message("Stage 5",self.color_dict[save>=4], "body", settings.SCREEN_WIDTH*self.location[4], settings.SCREEN_HEIGHT*self.location[10])
        self.m_Op = message("Options", (200,0,200), "body", settings.SCREEN_WIDTH*self.location[5], settings.SCREEN_HEIGHT*self.location[11])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    quit()
                    
        if self.m_Op.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.state = "OPTIONSCREEN"
        if self.m_S1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.level = 0
                self.state = "STAGE"
        if self.m_S2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if not save >= 1:
                        error_sound.play()
                        return self.state
                self.level = 1
                self.state = "STAGE"
        if self.m_S3.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if not save >= 2:
                        error_sound.play()
                        return self.state                
                self.level = 2
                self.state = "STAGE"
        if self.m_S4.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if not save >= 3:
                        error_sound.play()
                        return self.state
                self.level = 3
                self.state = "STAGE"
        if self.m_S5.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if not save >= 4:
                        error_sound.play()
                        return self.state                
                self.level = 4
                self.state = "STAGE"

        pygame.display.update()
        self.clock.tick(15)
        return self.state

class OptionScreen:
    def __init__(self):
        self.background = pygame.image.load("graphics/title_screen_background.jpg")
        self.rigth_arrow = pygame.image.load("graphics/arrow.png")
        self.rigth_arrow = pygame.transform.scale(self.rigth_arrow,(int(settings.SCREEN_WIDTH*0.07),50))
        self.left_arrow = pygame.transform.flip(self.rigth_arrow, True, False)
        self.location = [0.3, 0.3, 0.2, 0.5, 0.8, 0.3, 0.5, 0.8, 0.8, 0.8]
        self.clock = pygame.time.Clock()
        
    def run(self, screen, state, clock):
        self.state = state
        self.clock = clock
        screen.blit(self.background,(0,0))
        message("Options",(255,106,0,),"title", settings.SCREEN_WIDTH*0.5, settings.SCREEN_HEIGHT*0.1)
        message("Main Volume",(255,106,0), "body", settings.SCREEN_WIDTH*self.location[0], settings.SCREEN_HEIGHT*self.location[5])
        message("BGM Volume",(255,106,0), "body", settings.SCREEN_WIDTH*self.location[1], settings.SCREEN_HEIGHT*self.location[6])
        #self.m_UN = message("Units",(255,106,0), "body", settings.SCREEN_WIDTH*self.location[2], settings.SCREEN_HEIGHT*self.location[7])
        #self.m_CR = message("Controls",(255,106,0), "body", settings.SCREEN_WIDTH*self.location[3], settings.SCREEN_HEIGHT*self.location[8])
        self.m_BK = message("Back",(200,0,200), "body", settings.SCREEN_WIDTH*self.location[4], settings.SCREEN_HEIGHT*self.location[9])
        self.MV_L = screen.blit(self.rigth_arrow,(settings.SCREEN_WIDTH*0.55, settings.SCREEN_HEIGHT*0.25))
        self.MV_R = screen.blit(self.left_arrow,(settings.SCREEN_WIDTH*0.80, settings.SCREEN_HEIGHT*0.25))
        self.BV_L = screen.blit(self.rigth_arrow,(settings.SCREEN_WIDTH*0.55, settings.SCREEN_HEIGHT*0.5))
        self.BV_R = screen.blit(self.left_arrow,(settings.SCREEN_WIDTH*0.80, settings.SCREEN_HEIGHT*0.5))
        message(str(settings.MAIN_VOLUME),(255,0,0),"body",settings.SCREEN_WIDTH*0.7, settings.SCREEN_HEIGHT*0.3)
        message(str(settings.BGM_VOLUME),(255,0,0),"body",settings.SCREEN_WIDTH*0.7, settings.SCREEN_HEIGHT*0.55)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    quit()
            if self.MV_L.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    settings.MAIN_VOLUME -= 1
            if self.MV_R.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    settings.MAIN_VOLUME += 1
            if self.BV_L.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    settings.BGM_VOLUME -= 1
            if self.BV_R.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    settings.BGM_VOLUME += 1
            #if self.m_UN.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            #        self.state = "FILLERSCREEN"
            #if self.m_CR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            #        self.state = "FILLERMESSAGE"
            if self.m_BK.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    self.state = "STAGESCREEN"
            if settings.MAIN_VOLUME > 10:
                settings.MAIN_VOLUME = 10
            if settings.MAIN_VOLUME < 0:
                settings.MAIN_VOLUME = 0
            if settings.BGM_VOLUME > 10:
                settings.BGM_VOLUME = 10
            if settings.BGM_VOLUME < 0:
                settings.BGM_VOLUME = 0
        
        pygame.display.update()
        self.clock.tick(15)
        return self.state


state = "TITLESCREEN"
clock = pygame.time.Clock()
title_screen = TitleScreen()
stage_screen = StageScreen()
option_screen = OptionScreen()
team_logo = pygame.image.load("graphics/creative_games_logo.png")
team_logo = pygame.transform.scale(team_logo,(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
game_over = pygame.image.load("graphics/game_over.png")
game_over = pygame.transform.scale(game_over,(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

storyi = []
for i in xrange(1,6):
    storyi.append(pygame.image.load("graphics/Principio"+str(i)+".png"))
storyi.append(pygame.image.load("graphics/Principio1_2.png"))

storyf = []
for i in xrange(1,6):
    storyf.append(pygame.image.load("graphics/Final"+str(i)+".png"))

save = int(open("saves","r").read())
level = 0

def story_screen(screen, image, foo = False):
    done = True
    if stage_screen.level == 0 and not foo:
        stage_screen_level = -1
        story_screen(screen,storyi[0],True)
        stage_screen.level = 0
        image = storyi[-1]
    while done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                done = False
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
        screen.blit(image,(0,0))
        pygame.display.flip()

menu_sound = pygame.mixer.Sound("sounds/menu_music.ogg")
creative_games_sound = pygame.mixer.Sound("sounds/CreativeGames.ogg")
creative_games_sound.play()
for i in range(9):    
    screen.blit(team_logo,(0,0))
    clock.tick(1)
    pygame.display.flip()

menu_sound.play(-1)
while True:
    if state == "TITLESCREEN":
        state = title_screen.run(screen, state, clock)
    elif state == "STAGESCREEN":
        state = stage_screen.run(screen, state, clock)
    elif state == "OPTIONSCREEN":
        state = option_screen.run(screen, state, clock)
        menu_sound.set_volume(settings.MAIN_VOLUME/10.0)
    elif state == "FILLERSCREEN":
        print "no implementado"
        state = "OPTIONSCREEN"
    elif state == "STAGE":
        story_screen(screen,storyi[stage_screen.level])
        test_stage = Stage(stage_data.stage_list[stage_screen.level],screen)
        test_stage.render.draw_background(screen)
        pygame.display.flip()
        menu_sound.fadeout(300)
        while True:
            result = test_stage.update(screen)
            if result == -1:
                print "GAME OVER"
                story_screen(screen,game_over,True)
                break
            elif result == 1:
                if save == stage_screen.level:
                    save += 1
                    open("saves","w").write(str(save))
                print "YOU WIN"
                story_screen(screen,storyf[stage_screen.level],True)
                break
            clock.tick(settings.FRAME_RATE)
        pygame.mixer.fadeout(200)
        
        menu_sound.play(-1)
        state = "TITLESCREEN"
    #print pygame.mouse.get_pos()

