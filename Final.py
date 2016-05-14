import pygame
import sys
import time
import random
from pygame.locals import *

ancho = 1200
alto = 700

dim = [ancho, alto]

#Colores
azul = (0, 0, 255)
negro = (0, 0, 0)
blanco = (255, 255, 255)
naranja = (255, 128, 0)
rojo = (255, 0, 0)

class Barra(pygame.sprite.Sprite):
	def __init__(self, x, y, dimension, color):
		pygame.sprite.Sprite.__init__(self)
		self.posx = x
		self.posy = y
		self.dim = dimension
		self.color = color

	def Dibujar(self, pantalla):
		pygame.draw.rect(pantalla, self.color, pygame.Rect(self.posx, self.posy, self.dim, 20))

class Menu_Principal:
	ver = False
	def __init__(self,text, pos, pantalla, fuente):
		self.text = text
		self.pos = pos
		self.pantalla = pantalla
		self.fuente = fuente
		self.get_tam()
		self.set_rect()
		self.draw()

	def draw(self):
		self.set_rend()
		self.pantalla.blit(self.rend, self.rect)

	def set_rend(self):
		self.rend = self.fuente.render(self.text, True, self.get_color())

	def get_color(self):
		if self.ver:
			return negro
		else:
			return naranja

	def set_rect(self):
		self.set_rend()
		self.rect = self.rend.get_rect()
		self.rect.topleft = self.pos

	def get_tam(self):
		self.set_rend()
		return self.rend.get_rect()

#Interfaz usuario
if __name__ == '__main__':
	pygame.init()
	pantalla = pygame.display.set_mode(dim)

	#Fondos
	fondo_principal = pygame.image.load("Fondos/Fondo4.jpg").convert()
	fondo_principal = pygame.transform.scale(fondo_principal, dim)
	fondo_instrucciones = pygame.image.load("Fondos/Fondo5.jpg").convert()
	fondo_instrucciones = pygame.transform.scale(fondo_instrucciones, dim)
	fondo_arena = pygame.image.load("Fondos/cuadrilatero.jpg").convert()
	fondo_arena = pygame.transform.scale(fondo_arena, (ancho, alto - 50))

	#Otras imagenes
	corazon = pygame.image.load("Otras/corazon.png").convert_alpha()
	
	#Fuentes
	fuente1 = pygame.font.Font("Fuente1.ttf", 60)
	fuente2 = pygame.font.Font("Fuente1.ttf", 50)

	#Listas

	#Barras
	vida = Barra(80, 15, 250, rojo)
	ki = Barra(430, 15, 150, azul)
	

	#Menu Principal
	nueva_partida = Menu_Principal("Nueva Partida", (80, 240), pantalla, fuente1)
	nueva_tam = nueva_partida.get_tam()
	instrucciones = Menu_Principal("Instrucciones", (80, 320), pantalla, fuente1)
	instrucciones_tam = instrucciones.get_tam()
	salir_pr = Menu_Principal("Salir", (80, 400), pantalla, fuente1)
	salir_tam = salir_pr.get_tam()

	#Menu Instruciones
	iniciar_partida = Menu_Principal("Iniciar Partida", (400, 620), pantalla, fuente2)
	iniciar_tam = iniciar_partida.get_tam()
	volver_inicio = Menu_Principal("Volver", (50, 620), pantalla, fuente2)
	volver_tam = volver_inicio.get_tam()

	#Menu Pausa
	pausa = Menu_Principal("Pausa", (ancho/2, 100), pantalla, fuente1)
	pausa_tam = pausa.get_tam()
	configuar = Menu_Principal("Configurar Teclado", (ancho/2, 120), pantalla, fuente1)
	configurar_tam = configuar.get_tam()
	continuar = Menu_Principal("Continuar", (ancho/2, 130), pantalla, fuente1)
	continuar_tam = continuar.get_tam()
	salir_p = Menu_Principal("Salir", (ancho/2, 140), pantalla, fuente1)
	salir_p_tam = salir_p.get_tam()

	#Variables a usar
	terminar = False
	inicio = False
	instruc = False
	pause = False
	introduccion = False
	salir = False
	iniciar_jue = False
	fin_juego = False

	cont = 1

	m_princ = [nueva_partida, instrucciones, salir_pr]
	m_instr = [iniciar_partida, volver_inicio]
	m_pausa = [configuar, continuar, salir_p]

	pygame.display.flip()
	reloj = pygame.time.Clock()

	pantalla.blit(fondo_principal, (0, 0))

	while introduccion and cont <= 1309:
		fondo = pygame.image.load('Intro/intro ('+str(cont)+').png').convert()
		fondo = pygame.transform.scale(fondo, dim)
		pantalla.blit(fondo, (0,0))
		pygame.display.flip()
		#time.sleep(0.5)
		cont += 1

	#time.sleep(0.5)

	while not terminar:
		#Menu principal
		if not inicio and not instruc and not pause and not salir:
			pantalla.blit(fondo_principal, (0, 0))
			pygame.event.pump()
			for opc in m_princ:
				if opc.rect.collidepoint(pygame.mouse.get_pos()):
					opc.ver = True
				else:
					opc.ver = False
				opc.draw()
			pygame.display.update()

		#Eventos
		tecla = pygame.key.get_pressed()
		for event in pygame.event.get():
			if tecla[K_ESCAPE] or event.type == QUIT:
				terminar = True

			if not inicio and not instruc and not salir:
				#Boton nueva partida
				if event.type == pygame.MOUSEBUTTONDOWN and 80 <= event.pos[0] <= (80 + nueva_tam.width) and 240 <= event.pos[1] <= (240 + nueva_tam.height):
					inicio = True
					iniciar_jue = True
				#Boton instrucciones
				if event.type == pygame.MOUSEBUTTONDOWN and 80 <= event.pos[0] <= (80 + instrucciones_tam.width) and 320 <= event.pos[1] <= (320 + instrucciones_tam.height):
					instruc = True
				#Boton salir
				if event.type == pygame.MOUSEBUTTONDOWN and 80 <= event.pos[0] <= (80 + salir_tam.width) and 400 <= event.pos[1] <= (400 + salir_tam.height):
					salir = True
					terminar = True

		if instruc:
			pantalla.fill(negro)
			pantalla.blit(fondo_instrucciones, (0, 0))
			pygame.event.pump()
			for op in m_instr:
				if op.rect.collidepoint(pygame.mouse.get_pos()):
					op.ver = True
				else:
					op.ver = False
				op.draw()
			pygame.display.update()
			pygame.display.flip()

			if instruc:
				#Boton iniciar partida
				if event.type == pygame.MOUSEBUTTONDOWN and 400 <= event.pos[0] <= (400 + iniciar_tam.width) and 620 <= event.pos[1] <= (620 + iniciar_tam.height):
					inicio = True
					instruc = False
					iniciar_jue = True
				#Boton volver
				if event.type == pygame.MOUSEBUTTONDOWN and 50 <= event.pos[0] <= (50 + volver_tam.width) and 620 <= event.pos[1] <= (620 + volver_tam.height):
					instruc = False
				
		if inicio and not fin_juego:
			pantalla.fill(negro)
			pantalla.blit(fondo_arena, (0, 50))
			#barras.draw(pantalla)

			#Dibuja las barras
			pantalla.blit(corazon, (38, 7))
			vida.Dibujar(pantalla)
			ki.Dibujar(pantalla)

		
		reloj.tick(60)
		pygame.display.flip()

		#pygame.quit()
