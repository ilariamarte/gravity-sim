#!/usr/bin/env python
import pygame
import numpy as np
from random import random
from time import sleep
from support.PlanetSystem import PlanetSystem


if __name__ == '__main__':
	
	sw,sh = 1000,400
	TIME_DELAY = 0.008
	pygame.init()
	screen = pygame.display.set_mode((sw,sh))
	clock = pygame.time.Clock()

	P1 = PlanetSystem(screen,curr_planets=0,max_planets=10,dt=TIME_DELAY,screen_width=sw/2,screen_height=sh,offset=0,script="3",variation=0.0001)
	P2 = PlanetSystem(screen,curr_planets=0,max_planets=10,dt=TIME_DELAY,screen_width=sw/2,screen_height=sh,offset=sw/2,script="3",variation=0.0002)

	loop = True
	while loop:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				loop = False

		screen.fill((0, 0, 0)) # refresh
		
		# P1.create_planet_on_click()
		# P2.create_planet_on_click()
		P1.draw()
		P2.draw()
		P1.update()
		P2.update()
		
		sleep(TIME_DELAY)
		pygame.display.flip()

pygame.quit()
