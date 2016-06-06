import pygame
import sys
import time
import random
from pygame.locals import *
from mapa import *

ancho = 1200
alto = 700

dim = [ancho, alto]
screen_size = (1280, 720)

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

def introduccion(pantalla, intro, cont):
	while intro and cont <= 1309:
		fondo = pygame.image.load('Intro/intro ('+str(cont)+').png').convert()
		fondo = pygame.transform.scale(fondo, dim)
		pantalla.blit(fondo, (0,0))
		pygame.display.flip()
		#time.sleep(0.5)
		cont += 1

#Interfaz usuario
if __name__ == '__main__':
	pygame.init()
	pantalla = pygame.display.set_mode(dim)
	pantalla_rect = pantalla.get_rect()

	#Fondos
	fondo_principal = pygame.image.load("Fondos/Fondo4.jpg").convert()
	fondo_principal = pygame.transform.scale(fondo_principal, dim)
	fondo_instrucciones = pygame.image.load("Fondos/Fondo5.jpg").convert()
	fondo_instrucciones = pygame.transform.scale(fondo_instrucciones, dim)
	fondo_nivel1 = pygame.image.load("Fondos/Nivel1.png").convert()
	fondo_nivel1 = pygame.transform.scale(fondo_nivel1, (ancho, alto))
	fondo_nivel1_rect = fondo_nivel1.get_rect()
	fondo_nivel2 = pygame.image.load("Fondos/Nivel2.png").convert()
	fondo_nivel2 = pygame.transform.scale(fondo_nivel2, (ancho, alto))
	fondo_nivel2_rect = fondo_nivel2.get_rect()

	#Nivel
	level = Level("level/level")
	level.create_level(0,0)
	world = level.world

	#Otras imagenes
	corazon = pygame.image.load("Otras/corazon.png").convert_alpha()
	rayo = pygame.image.load("Otras/rayo.png").convert_alpha()
	
	#Fuentes
	fuente1 = pygame.font.Font("Fuente1.ttf", 60)
	fuente2 = pygame.font.Font("Fuente1.ttf", 50)

	#Listas
	ls_jugador = pygame.sprite.Group()
	ls_todos = pygame.sprite.Group()

	#Barras
	vida = Barra(80, 15, 250, rojo)
	ki = Barra(430, 15, 150, azul)

	#Jugador
	jugador = level.jugador

	#Enemigos
	enemigo = level.enem

	camara = Camara(pantalla, jugador.rect, level.get_size()[0], level.get_size()[1])
	all_sprite = level.all_sprite
	
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
	intro = False
	salir = False
	iniciar_jue = False
	fin_juego = False

	cont = 1

	m_princ = [nueva_partida, instrucciones, salir_pr]
	m_instr = [iniciar_partida, volver_inicio]
	m_pausa = [configuar, continuar, salir_p]

	pygame.display.flip()
	reloj = pygame.time.Clock()

	arriba = izq = der = False
	x, y = 0, 0

	pantalla.blit(fondo_principal, (0, 0))

	introduccion(pantalla, intro, cont)

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
				pygame.quit()
				sys.exit()

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
			#pantalla.blit(fondo_nivel1, (0, 50))
			#barras.draw(pantalla)

			#Dibuja las barras

			if event.type == KEYDOWN and event.key == K_UP:
				arriba = True
			if event.type == KEYDOWN and event.key == K_LEFT:
				izq = True
			if event.type == KEYDOWN and event.key == K_RIGHT:
				der = True

			if event.type == KEYUP and event.key == K_UP:
				arriba = False
			if event.type == KEYUP and event.key == K_LEFT:
				izq = False
			if event.type == KEYUP and event.key == K_RIGHT:
				der = False

			asize = ((pantalla_rect.w // fondo_nivel1_rect.w + 1) * fondo_nivel1_rect.w, (pantalla_rect.h // fondo_nivel1_rect.h + 1) * fondo_nivel1_rect.h)
			bg = pygame.Surface(asize)

			for x in range(0, asize[0], fondo_nivel1_rect.w):
				for y in range(0, asize[1], fondo_nivel1_rect.h):
					pantalla.blit(fondo_nivel1, (x, y))

			camara.dibujar_sprites(pantalla, all_sprite)
			jugador.update(arriba, izq, der, world)
			
			pantalla.blit(corazon, (38, 7))
			pantalla.blit(rayo, (390, 7))
			vida.Dibujar(pantalla)
			ki.Dibujar(pantalla)
			camara.update()

        	#ls_todos.draw(pantalla)
		
		reloj.tick(60)
		pygame.display.flip()

		#pygame.quit()
