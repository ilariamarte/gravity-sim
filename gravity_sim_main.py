#!/usr/bin/env python
import pygame
import numpy as np
from random import random
from time import sleep
from support.PlanetSystem import PlanetSystem

lava_lamp = 0.0003
normal = 0.008

if __name__ == '__main__':
	
	sw,sh = 1000,600
	TIME_DELAY = normal
	pygame.init()
	screen = pygame.display.set_mode((sw,sh))
	clock = pygame.time.Clock()

	P = PlanetSystem(screen,curr_planets=0,max_planets=100,dt=TIME_DELAY,screen_width=sw,screen_height=sh,script="0",draw_cm=False,trail_length=15)

	loop = True
	while loop:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				loop = False

		screen.fill((0, 0, 0)) # refresh
		
		P.create_planet_on_click()
		P.draw()
		P.update()
		
		sleep(0.008)
		pygame.display.flip()

pygame.quit()
