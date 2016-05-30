import pygame
from pygame.locals import *
import sys

screen_size = (1280, 720) #resolution of the game
global FPS
global clock
global time_spent

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
        self.image = pygame.image.load('idle_right.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.frame = 0
        self.vel = 10

    def update(self, arriba, izq, der):
        if arriba:
            if self.contacto:
                self.saltar = True
                self.movy -= 20

        if izq:
            self.movx = -self.vel
            

        if der:
            self.movx = +self.vel

        if not (izq or der):
            self.movx = 0
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
                x += 25
            y += 25
            x = 0

    def get_size(self):
        lines = self.level1
        #line = lines[0]
        line = max(lines, key=len)
        self.width = (len(line))*25
        self.height = (len(lines))*25
        return (self.width, self.height)



def tps(orologio,fps):
    temp = orologio.tick(fps)
    tps = temp / 1000.
    return tps


pygame.init()
pantalla = pygame.display.set_mode(screen_size, FULLSCREEN, 32)
pantalla_rect = pantalla.get_rect()
fondo = pygame.image.load("world/background2.jpg").convert_alpha()
fondo_rect = fondo.get_rect()
level = Level("level/level")
level.create_level(0,0)
world = level.world
jugador = level.jugador
pygame.mouse.set_visible(0)

camara = Camara(pantalla, jugador.rect, level.get_size()[0], level.get_size()[1])
all_sprite = level.all_sprite

FPS = 30
clock = pygame.time.Clock()

arriba = izq = der = False
x, y = 0, 0
while True:

    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

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

    asize = ((pantalla_rect.w // fondo_rect.w + 1) * fondo_rect.w, (pantalla_rect.h // fondo_rect.h + 1) * fondo_rect.h)
    bg = pygame.Surface(asize)

    for x in range(0, asize[0], fondo_rect.w):
        for y in range(0, asize[1], fondo_rect.h):
            pantalla.blit(fondo, (x, y))

    time_spent = tps(clock, FPS)
    camara.dibujar_sprites(pantalla, all_sprite)

    jugador.update(arriba, izq, der)
    camara.update()
    pygame.display.flip()
