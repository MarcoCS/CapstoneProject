##-------------------------------------------------------------------
## Tilemap
## Dallas Spendelow
## November 28, 2018
## This file loads the map and allows the camera to function.
##-------------------------------------------------------------------

import pygame as pg
from settings import *

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        
        ## Limit scrolling to map
        x = min(0, x) ## Left
        y = min(0, y) ## Top
        x = max(-(self.width - WIDTH), x)   ## Right
        y = max(-(self.height - HEIGHT), y) ## Bottom
        
        self.camera = pg.Rect(x, y, self.width, self.height)
        
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
