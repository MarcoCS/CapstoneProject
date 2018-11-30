##-------------------------------------------------------------------
## Player Sprite 
## Dallas Spendelow
## November 28, 2018
## This program has the player sprite, as well as camera movement.
##-------------------------------------------------------------------

import pygame as pg
from settings import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.velX, self.velY = 0, 0
        self.x = x
        self.y = y       
    
    def checkKeys(self):
        self.velX, self.velY = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.velX = -PLAYER_SPEED
        if keys[pg.K_RIGHT]:
            self.velX = PLAYER_SPEED
        if keys[pg.K_UP]:
            self.velY = -PLAYER_SPEED
        if keys[pg.K_DOWN]:
            self.velY = PLAYER_SPEED
        if self.velX != 0 and self.velY != 0:   ## Diagonally, we have to
            self.velX *= 0.7071              ## adjust speed using sqrt 2.
            self.velY *= 0.7071
    
    def update(self):
        self.checkKeys()
        self.x += self.velX * self.game.dt 
        self.y += self.velY * self.game.dt
        self.rect.topleft = (self.x, self.y)