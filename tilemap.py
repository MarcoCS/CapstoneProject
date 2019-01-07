##-------------------------------------------------------------------
## Tilemap
## Dallas Spendelow
## November 28, 2018
## This file loads the map and allows the camera to function.
##-------------------------------------------------------------------

import pygame as pg
from settings import *

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def update(self, target):
        self.x = -target.rect.centerx + int(WIDTH / 2)
        self.y = -target.rect.centery + int(HEIGHT / 2)
        print("Camera",self.x,self.y)
        
        ## Limit scrolling to map
        self.x = min(0, self.x) ## Left
        self.y = min(0, self.y) ## Top
        self.x = max(-(self.width - WIDTH), self.x)   ## Right
        self.y = max(-(self.height - HEIGHT), self.y) ## Bottom
        
        self.camera = pg.Rect(self.x, self.y, self.width, self.height)
        
class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
    
        self.tileWidth = len(self.data[0])
        self.tileHeight = len(self.data)
        self.width = self.tileWidth * TILESIZE
        self.height = self.tileHeight * TILESIZE
