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
    def __init__(self, x, y, tip):
        self.x = x
        self.y = y
        self.tip = tip
        pygame.sprite.Sprite.__init__(self)
        if tip == 1:
            self.image = pygame.image.load("world/piso1.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 2:
            self.image = pygame.image.load("world/piso2.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 3:
            self.image = pygame.image.load("world/piso3.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 4:
            self.image = pygame.image.load("world/muro.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 5:
            self.image = pygame.image.load("world/nube1.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 6:
            self.image = pygame.image.load("world/nube2.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        if tip == 7:
            self.image = pygame.image.load("world/nube3.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]
        

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

    def update(self, arriba, izq, der, world):
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
        self.colision(self.movx, 0, world)

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
                if movx > 0:
                    self.rect.right = o.rect.left
                if movx < 0:
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
        self.all_sprite = pygame.sprite.Group()
        self.level = open(open_level, "r")

    def create_level(self, x, y):
        for l in self.level:
            self.level1.append(l)

        for fila in self.level1:
            for col in fila:
                if col == "X":
                    obstaculo = Obstaculo(x, y, 2)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "V":
                    obstaculo = Obstaculo(x, y, 2)
                    #self.world.append(obstaculo)
                    self.all_sprite.add(obstaculo)
                if col == "Z":
                    obstaculo = Obstaculo(x, y, 1)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "z":
                    obstaculo = Obstaculo(x, y, 3)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "H":
                    obstaculo = Obstaculo(x, y, 4)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "B":
                    obstaculo = Obstaculo(x, y, 5)
                    #self.world.append(obstaculo)
                    self.all_sprite.add(obstaculo)
                if col == "N":
                    obstaculo = Obstaculo(x, y, 6)
                    #self.world.append(obstaculo)
                    self.all_sprite.add(obstaculo)
                if col == "b":
                    obstaculo = Obstaculo(x, y, 7)
                    #self.world.append(obstaculo)
                    self.all_sprite.add(obstaculo)
                if col == "A":
                    obstaculo = Obstaculo(x, y, 5)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "C":
                    obstaculo = Obstaculo(x, y, 6)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "a":
                    obstaculo = Obstaculo(x, y, 7)
                    self.world.append(obstaculo)
                    self.all_sprite.add(self.world)
                if col == "P":
                    self.jugador = Jugador(x,y)
                    self.all_sprite.add(self.jugador)
                x += 32
            y += 32
            x = 0

    def get_size(self):
        lines = self.level1
        #line = lines[0]
        line = max(lines, key=len)
        self.width = (len(line))*32
        self.height = (len(lines))*32
        return (self.width, self.height)

