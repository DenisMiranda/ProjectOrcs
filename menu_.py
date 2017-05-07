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
#screen = pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT))
font_title = pygame.font.Font("Heavy_Gothik.ttf",60)
font_body = pygame.font.SysFont("Algerian",50)

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


class TitleScreen:
    def __init__(self):
        self.background = pygame.image.load("title_screen_background.jpg")
        #self.team_logo = pygame.image.load("creativegames.png")
        #self.game_logo = pygame.image.load("creativegames.png")
        self.state = "TITLESCREEN"
        self.clock = pygame.time.Clock()
    def run(self, screen, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.state = "STAGESCREEN"
        screen.blit(self.background,(0,0))
        message("Project Orcs", (255,106,0,), "title", settings.SCREEN_WIDTH*0.5, settings.SCREEN_HEIGHT*0.2)
        message("Press Space to start", (255,106,0), "body", settings.SCREEN_WIDTH*0.5, settings.SCREEN_HEIGHT*0.6)
        pygame.display.update()
        self.clock.tick(15)
        print self.clock.get_fps()
        return self.state

class StageScreen:
    def __init__(self):
        self.background = pygame.image.load("title_screen_background.jpg")
        self.pos = 0
        self.location = [0.25, 0.5, 0.75, 0.35, 0.65, 0.9, 0.4, 0.4, 0.4, 0.7, 0.7, 0.9]
        self.state = "STAGESCREEN"
        self.clock = pygame.time.Clock()
    def run(self, screen, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.pos += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.pos -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.pos -= 3
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.pos += 3
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.pos == 5:
                        self.state = "OPTIONSCREEN"
                    elif not self.pos == 5:
                        self.state = "FILLERMESSAGE"

        screen.blit(self.background,(0,0))
        message("Select Stage:",(255,106,0,),"title", settings.SCREEN_WIDTH*0.5, settings.SCREEN_HEIGHT*0.1)
        message("Stage 1",(255,106,0,), "body", settings.SCREEN_WIDTH*self.location[0], settings.SCREEN_HEIGHT*self.location[6])
        message("Stage 2",(255,106,0,), "body", settings.SCREEN_WIDTH*self.location[1], settings.SCREEN_HEIGHT*self.location[7])
        message("Stage 3",(255,106,0,), "body", settings.SCREEN_WIDTH*self.location[2], settings.SCREEN_HEIGHT*self.location[8])
        message("Stage 4",(255,106,0,), "body", settings.SCREEN_WIDTH*self.location[3], settings.SCREEN_HEIGHT*self.location[9])
        message("Stage 5",(255,106,0,), "body", settings.SCREEN_WIDTH*self.location[4], settings.SCREEN_HEIGHT*self.location[10])
        message("Options", (200,0,200), "body", settings.SCREEN_WIDTH*self.location[5], settings.SCREEN_HEIGHT*self.location[11])

        if self.pos > 5:
            self.pos = 0
        if self.pos < 0:
            self.pos = 5

        message("v",(255,0,0,), "body", (settings.SCREEN_WIDTH*self.location[self.pos]), (settings.SCREEN_HEIGHT*(self.location[self.pos+6] - 0.1)))
        pygame.display.update()
        self.clock.tick(15)
        print self.clock.get_fps()
        return self.state

class OptionScreen:
    def __init__(self):
        self.background = pygame.image.load("title_screen_background.jpg")
        self.pos = 0
        self.location = [0.3, 0.2, 0.5, 0.8, 0.3, 0.5, 0.8]
        self.state = "OPTIONSCREEN"
        self.clock = pygame.time.Clock()
    def run(self, screen, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.pos += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.pos -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.pos -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.pos += 1

        screen.blit(self.background,(0,0))
        message("Options",(255,106,0,),"title", settings.SCREEN_WIDTH*0.5, settings.SCREEN_HEIGHT*0.1)
        message("Main Volume",(255,106,0,), "body", settings.SCREEN_WIDTH*self.location[0], settings.SCREEN_HEIGHT*self.location[4])
        message("BGM Volume",(255,106,0,), "body", settings.SCREEN_WIDTH*self.location[0], settings.SCREEN_HEIGHT*self.location[5])
        message("Towers",(255,106,0,), "body", settings.SCREEN_WIDTH*self.location[1], settings.SCREEN_HEIGHT*self.location[6])
        message("Enemies",(255,106,0,), "body", settings.SCREEN_WIDTH*self.location[2], settings.SCREEN_HEIGHT*self.location[6])
        message("Back",(255,106,0,), "body", settings.SCREEN_WIDTH*self.location[3], settings.SCREEN_HEIGHT*self.location[6])

        if self.pos > 5:
            self.pos = 0
        if self.pos < 0:
            self.pos = 5
        message("____",(255,0,0,), "body", (settings.SCREEN_WIDTH*(self.location[self.pos])), (settings.SCREEN_HEIGHT*(self.location[self.pos])))
        pygame.display.update()
        self.clock.tick(15)
        print self.clock.get_fps()
        return self.state

state = "TITLESCREEN"
title_screen = TitleScreen()
stage_screen = StageScreen()
option_screen = OptionScreen()

while True:
    if state == "TITLESCREEN":
        state = title_screen.run(screen, state)
    elif state == "STAGESCREEN":
        state = stage_screen.run(screen, state)
    elif state == "OPTIONSCREEN":
        state = option_screen.run(screen, state)
    elif state == "FILLERMESSAGE":
        test_stage = Stage(stage_data.one_stage_data,screen)
        test_stage.render.draw_background(screen)
        Clock = pygame.time.Clock()
        sounda= pygame.mixer.Sound("theme.ogg")
        sounda.set_volume(0.3)
        pygame.display.flip()
        while True:
            sounda.play()
            result = test_stage.update(screen)
            if result == -1:
                print "GAME OVER"
                break   
            elif result == 1:
                print "VICTORY"
                break
            Clock.tick(settings.FRAME_RATE)
            print Clock.get_fps()

