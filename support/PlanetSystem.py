import pygame
import numpy as np
from random import random
from time import sleep


class PlanetSystem:
	def __init__(self,screen,curr_planets=0,max_planets=10,dt=0.008,screen_width=1000,screen_height=600,offset=0,script=0,variation=0,draw_cm=False,trail_length=15):
		point_planet = curr_planets
		if curr_planets > max_planets: curr_planets = max_planets
		self.point_planet = point_planet
		self.curr_planets = curr_planets
		self.max_planets = max_planets
		self.mux1 = 0
		self.mux2 = 1
		self.dt = dt
		self.density = 0.5 # kg m^-3
		self.radius = 3*np.ones(max_planets)
		self.max_radius = 50
		self.G = G = 6.67408 * np.power(10.,4) # 6.67408 × 10^-11 m^3 kg^-1 s^-2
		self.softeningConstant = 100000000
		self.screen = screen
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.offset = offset
		self.draw_cm = draw_cm
		self.trail_length = trail_length
		planet_list = self.handle_script(script,variation)
		self.planet_list = planet_list
	
	def handle_script(self,scr,var):
		# self.G = G = 6.67408 * np.power(10.,3)
		# self.softeningConstant = 10
		# self.density = 0.5
		pl = list(np.zeros(self.max_planets)) # will become list of Planet class ( [self.Planet(0,0,0,0) for i in range(self.max_planets)] )
		sw,sh,os,d,tl = self.screen_width, self.screen_height, self.offset, self.density, self.trail_length
		r = 10
		if scr == "2":
			self.point_planet, self.curr_planets = 2, 2
			pl[0] = self.Planet(sw/3 + os, sh/2, d, r, tl)
			pl[1] = self.Planet(sw*2/3 + os, sh/2, d, r, tl)
		elif scr == "3":
			self.point_planet, self.curr_planets = 3, 3
			pl[0] = self.Planet(sw/2 + os + var, sh/3, d, r, tl)
			pl[1] = self.Planet(sw/3 + os, sh*2/3, d, r, tl)
			pl[2] = self.Planet(sw*2/3 + os, sh*2/3, d, r, tl)
		elif scr == "orbit":
			self.point_planet, self.curr_planets = 2, 2
			pl[0] = self.Planet(sw/2 + os, sh/2, d, self.max_radius, tl, update=False)
			pl[1] = self.Planet(sw/2 + os, sh/3, d, r, tl, vx=np.power(6 * self.G * pl[0].mass / pl[0].rad,1/3)) # escape velocity
		else:
			for i in range(self.curr_planets):
				rand_rad = 47*random()+3
				color_var = 160 + 80*rand_rad/self.max_radius # 160 --> 240 (range=80)
				pl[i] = self.Planet(sw*random(), sh*random(), d, rand_rad, tl, color_var)
		return pl
		
	class Planet:
		def __init__(self,x,y,density,rad,trail_length,color_var=230,vx=0,vy=0,update=True):
			col = pygame.Color(0)
			col.hsva = color_var,100,100,100
			self.col = col
			self.x = x
			self.y = y
			self.vx = vx
			self.vy = vy
			self.ax = 0
			self.ay = 0
			self.rad = rad
			self.mass = density * 4/3 * np.pi * (self.rad)**3
			self.density = density
			self.real_mass = self.mass # if distance between planets is < rad, use real_mass instead of mass
			self.trail = self.Trail(rad-1, trail_length, x, y)
			self.update = update
		
		def update_real_mass(self,r):
			self.real_mass = self.density * 4/3 * np.pi * (r)**3
	
		class Trail:
			def __init__(self,rad,length,x,y):
				rad = int(rad)
				if rad < 3: rad = 3
				self.x = x*np.ones(length)
				self.y = y*np.ones(length)
				self.rad =  np.arange(rad,0,-rad/length)
				self.length = length
			
			def update_trail(self,x,y):
				for i in reversed(range(1,self.length)):
					self.x[i] = self.x[i-1]
					self.y[i] = self.y[i-1]
				self.x[0], self.y[0] = x, y

	def create_planet_on_click(self):
		left_click = pygame.mouse.get_pressed()[0]
		right_click = pygame.mouse.get_pressed()[2]
		press_space = pygame.key.get_pressed()[pygame.K_SPACE]
		if left_click:
			self.mux1 = 1
		if self.mux1 and left_click:
			if self.mux2: # do it only once at the start of the click
				self.mux2 = 0
				self.radius[self.point_planet] = 3 # reset radius before substituting a Planet
			if self.radius[self.point_planet] < self.max_radius:
				self.radius[self.point_planet] += 0.5
		if left_click and self.mux1 and (right_click or press_space): # press right click or space while still pressing left click - cancel placing of Planet
			self.mux1 = 0
			self.radius[self.point_planet] = 1
		if not left_click and self.mux1: # left click is released
			self.mux1 = 0
			self.mux2 = 1
			x,y = pygame.mouse.get_pos()
			color_var = 160 + 80*self.radius[self.point_planet]/self.max_radius # 160 --> 240 (range=80)
			self.planet_list[self.point_planet] = self.Planet(x,y,self.density,self.radius[self.point_planet],self.trail_length,color_var)
			if self.point_planet < self.max_planets-1:
				self.point_planet += 1
			else:
				self.point_planet = 0
			if self.curr_planets < self.max_planets:
				self.curr_planets += 1

	def draw(self):
		if self.mux1: # left_click continuously pressed
			x,y = pygame.mouse.get_pos()
			pygame.draw.circle(self.screen, "white", (x,y), self.radius[self.point_planet])
		if self.curr_planets > 0:
			p = self.planet_list
			cm_x, cm_y, m_tot = 0,0,0
			for i in range(self.curr_planets):
				for j in range(p[i].trail.length):
					pygame.draw.circle(self.screen, p[i].col, (p[i].trail.x[j], p[i].trail.y[j]), p[i].trail.rad[j])
				pygame.draw.circle(self.screen, p[i].col, (p[i].x, p[i].y), p[i].rad)
				cm_x += p[i].mass * p[i].x
				cm_y += p[i].mass * p[i].y
				m_tot += p[i].mass
			cm_x = cm_x/m_tot
			cm_y = cm_y/m_tot
			if self.draw_cm:
				pygame.draw.circle(self.screen, "red", (cm_x, cm_y), 2)

	def update(self):
		if self.curr_planets > 1: # at least 2 planets
			p = self.planet_list
			G = self.G
			dt = self.dt
			softeningConstant = self.softeningConstant
			for i in range(self.curr_planets):
				if p[i].update == True:
					p[i].ax = 0
					p[i].ay = 0
					for j in range(self.curr_planets):
						if j != i:
							xi,xj = p[i].x, p[j].x
							yi,yj = p[i].y, p[j].y
							dx,dy = xj-xi, yj-yi
							dSq = np.power(dx,2) + np.power(dy,2)
							r = np.power(dSq, 1/2) # sqrt((xj-xi)^2 + (yj-yi)^2)
							f = 0
							if r != 0:
								if r < p[i].rad + p[j].rad: # the distance between two planets is less than the sum of their radius
									d = r / (p[i].rad + p[j].rad)
									p[i].update_real_mass(p[i].rad * d)
									p[j].update_real_mass(p[j].rad * d)
									massI = p[i].real_mass
									massJ = p[j].real_mass
								else:
									massI = p[i].mass
									massJ = p[j].mass
								f = G * massJ / (dSq * np.power(dSq + softeningConstant, 1/2)) # G * m1 * m2 / r^2 --> G * m1 * m2 / (r^2 + sqrt(r^2 + s))
								p[i].ax += f * dx # fx
								p[i].ay += f * dy # fy
			for i in range(self.curr_planets):
				if p[i].update == True:
					p[i].vx += p[i].ax * dt
					p[i].vy += p[i].ay * dt
					p[i].x += p[i].vx * dt
					p[i].y += p[i].vy * dt
					if p[i].trail.length > 0: p[i].trail.update_trail(p[i].x, p[i].y)
			self.planet_list = p
