import pygame
from pygame.locals import *
import sys

def RelRect(actor, camara):
    return pygame.Rect(actor.rect.x-camara.rect.x, actor.rect.y-camara.rect.y, actor.rect.w, actor.rect.h)

class Camara(object):
    '''Clase para centrar la camara en el jugador jugador'''
    def __init__(self, pantalla, jugador, level_width, level_height):
        self.jugador = jugador
        self.rect = pantalla.get_rect()
        self.rect.center = self.jugador.center
        self.world_rect = Rect(0, 0, level_width, level_height)

    def update(self):
      if self.jugador.centerx > self.rect.centerx + 25:
          self.rect.centerx = self.jugador.centerx - 25
      if self.jugador.centerx < self.rect.centerx - 25:
          self.rect.centerx = self.jugador.centerx + 25
      if self.jugador.centery > self.rect.centery + 25:
          self.rect.centery = self.jugador.centery - 25
      if self.jugador.centery < self.rect.centery - 25:
          self.rect.centery = self.jugador.centery + 25
      self.rect.clamp_ip(self.world_rect)

    def dibujar_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, RelRect(s, self))


class Obstaculo(pygame.sprite.Sprite):
    '''Clase para crear los obstaculos'''
    def __init__(self, x, y, tip, lvl):
        self.x = x
        self.y = y
        self.tip = tip
        self.lvl = lvl
        pygame.sprite.Sprite.__init__(self)
        if tip == 1:
            self.image = pygame.image.load("Mundo/Nivel"+str(lvl)+"/pisovol1.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 2:
            self.image = pygame.image.load("Mundo/Nivel"+str(lvl)+"/piso.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 3:
            self.image = pygame.image.load("Mundo/Nivel"+str(lvl)+"/pisovol2.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 4:
            self.image = pygame.image.load("Mundo/Nivel"+str(lvl)+"/tierra.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 5:
            self.image = pygame.image.load("Mundo/agua1.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 6:
            self.image = pygame.image.load("Mundo/agua2.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 7:
            self.image = pygame.image.load("Mundo/puas.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 8:
            self.image = pygame.image.load("Mundo/muro.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 9:
            self.image = pygame.image.load("Mundo/Nivel"+str(lvl)+"/pisoba1.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 10:
            self.image = pygame.image.load("Mundo/Nivel"+str(lvl)+"/pisoba2.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 11:
            self.image = pygame.image.load("Mundo/Nivel"+str(lvl)+"/pisosu1.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 12:
            self.image = pygame.image.load("Mundo/Nivel"+str(lvl)+"/pisosu2.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 13:
            self.image = pygame.image.load("Mundo/muroG.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]

class Enemigo(pygame.sprite.Sprite):
    '''Clase para el jugador y las colisiones'''
    def __init__(self, x, y, tip):
        pygame.sprite.Sprite.__init__(self)
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.tipo = tip
        self.contacto = False
        self.saltar = True
        self.image = pygame.image.load('Enemigos/enemder.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.frame = 0
        self.vel = 10
        self.izq = False

    def update(self, world):
        if self.tipo == 1:
            if not self.izq:
                self.image = pygame.image.load("Enemigos/enemder.png").convert_alpha()
                self.movx = +self.vel
            else:
                self.image = pygame.image.load("Enemigos/enemizq.png").convert_alpha()
                self.movx = -self.vel

        self.rect.right += self.movx
        self.colision(self.movx, 0, world)

        if self.tipo == 2:
            if self.contacto:
                self.image = pygame.image.load("goku/gokuarr.png").convert_alpha()
                self.saltar = True
                self.movy -= 20

        #if self.tipo == 2:
        if not self.contacto:
            self.movy += 0.3
            if self.movy > 10:
                self.movy = 10
            self.rect.top += self.movy

        if self.saltar:
            self.movy += 2
            self.rect.top += self.movy
            if self.contacto == True:
                self.saltar = False

        self.contacto = False
        self.colision(0, self.movy, world)


    def colision(self, movx, movy, world):
        self.contacto = False
        for o in world:
            if self.rect.colliderect(o):
                if self.tipo == 1:
                    if movx > 0:
                        self.izq = True
                        self.rect.right = o.rect.left
                    if movx < 0:
                        self.izq = False
                        self.rect.left = o.rect.right
                if movy > 0:
                    self.rect.bottom = o.rect.top
                    self.movy = 0
                    self.contacto = True
                    self.saltar = True
                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0
                    self.saltar = False

class Jugador(pygame.sprite.Sprite):
    '''Clase para el jugador y las colisiones'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.contacto = False
        self.saltar = False
        self.image = pygame.image.load('goku/goku.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.frame = 0
        self.vel = 10
        self.nivel = False

    def update(self, arriba, izq, der, world, sig_lvl):
        if arriba:
            if self.contacto:
                self.image = pygame.image.load("goku/gokuarr.png").convert_alpha()
                self.saltar = True
                self.movy -= 20

        if izq:
            self.image = pygame.image.load("goku/gokuatr.png").convert_alpha()
            self.movx = -self.vel
            
        if der:
            self.image = pygame.image.load("goku/gokuder.png").convert_alpha()
            self.movx = +self.vel

        if not (izq or der):
            self.movx = 0
            self.image = pygame.image.load('goku/goku.png').convert_alpha()

        self.rect.right += self.movx
        self.colision(self.movx, 0, world, sig_lvl)

        if not self.contacto:
            self.movy += 0.3
            if self.movy > 10:
                self.movy = 10
            self.rect.top += self.movy

        if self.saltar:
            self.movy += 2
            self.rect.top += self.movy
            if self.contacto == True:
                self.saltar = False

        self.contacto = False
        self.colision(0, self.movy, world, sig_lvl)


    def colision(self, movx, movy, world, sig_lvl):
        self.contacto = False
        for i in sig_lvl:
            if self.rect.colliderect(i):
                if movx > 0:
                    self.nivel = True
                    self.image = pygame.image.load('goku/goku.png').convert_alpha()
                    self.rect.right = i.rect.left
                if movx < 0:
                    self.nivel = True
                    self.image = pygame.image.load('goku/goku.png').convert_alpha()
                    self.rect.left = i.rect.right

        for o in world:
            if self.rect.colliderect(o):
                if movx > 0:
                    self.image = pygame.image.load('goku/goku.png').convert_alpha()
                    self.rect.right = o.rect.left
                if movx < 0:
                    self.image = pygame.image.load('goku/goku.png').convert_alpha()
                    self.rect.left = o.rect.right
                if movy > 0:
                    self.rect.bottom = o.rect.top
                    self.movy = 0
                    self.contacto = True
                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0

class Level(object):
    '''Read a map and create a level'''
    def __init__(self, open_level):
        self.level1 = []
        self.world = []
        self.obstac = []
        self.enem = pygame.sprite.Group()
        self.sig_lvl = pygame.sprite.Group()
        self.all_sprite = pygame.sprite.Group()
        self.level = open(open_level, "r")

    def create_level(self, x, y, lvl):
        for l in self.level:
            self.level1.append(l)

        for fila in self.level1:
            for col in fila:
                if col == "X":
                    obstaculo = Obstaculo(x, y, 2, lvl)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "V":
                    obstaculo = Obstaculo(x, y, 2, lvl)
                    #self.world.append(obstaculo)
                    self.all_sprite.add(obstaculo)
                if col == "Z":
                    obstaculo = Obstaculo(x, y, 1, lvl)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "z":
                    obstaculo = Obstaculo(x, y, 3, lvl)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "H":
                    obstaculo = Obstaculo(x, y, 8, lvl)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "L":
                    obstaculo = Obstaculo(x, y, 4, lvl)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "m":
                    obstaculo = Obstaculo(x, y, 5, lvl)
                    #self.world.append(obstaculo)
                    self.all_sprite.add(obstaculo)
                if col == "M" or col == "T":
                    obstaculo = Obstaculo(x, y, 6, lvl)
                    #self.world.append(obstaculo)
                    self.all_sprite.add(obstaculo)
                if col == "T":
                    obstaculo = Obstaculo(x, y, 7, lvl)
                    self.obstac.append(obstaculo)
                    self.all_sprite.add(self.obstac)
                if col == "B":
                    obstaculo = Obstaculo(x, y, 9, lvl)
                    #self.world.append(obstaculo)
                    self.all_sprite.add(obstaculo)
                if col == "b":
                    obstaculo = Obstaculo(x, y, 10, lvl)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "S":
                    obstaculo = Obstaculo(x, y, 11, lvl)
                    #self.world.append(obstaculo)
                    self.all_sprite.add(obstaculo)
                if col == "s":
                    obstaculo = Obstaculo(x, y, 12, lvl)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "G":
                    obstaculo = Obstaculo(x, y, 13, lvl)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "O":
                    obstaculo = Obstaculo(x, y, 8, lvl)
                    self.sig_lvl.add(obstaculo)
                    self.all_sprite.add(obstaculo)
                if col == "P":
                    self.jugador = Jugador(x,y)
                    self.all_sprite.add(self.jugador)
                if col == "E":
                    self.enemigo = Enemigo(x,y,1)
                    self.enem.add(self.enemigo)
                    self.all_sprite.add(self.enem)
                if col == "e":
                    self.enemigo = Enemigo(x,y,2)
                    self.enem.add(self.enemigo)
                    self.all_sprite.add(self.enem)
                x += 32
            y += 32
            x = 0

    def get_size(self):
        lines = self.level1
        line = lines[0]
        line = max(lines, key=len)
        self.width = (len(line))*32
        self.height = (len(lines))*32
        return (self.width, self.height)

