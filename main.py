##-------------------------------------------------------------------
## Top Down Shooter - Main program
## Dallas Spendelow
## November 28, 2018
## This program contains the game class, that runs the game.
##-------------------------------------------------------------------

import pygame as pg
from settings import *
from player import *
from tilemap import *
from os import path

class Game:
    def __init__(self):
        # Initialize pygame
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.loadData()
        
    def loadData(self):
        gameFolder = path.dirname(__file__)
        self.map = Map(path.join(gameFolder, 'map.txt'))
                
    def new(self):
        # Start a new game
        self.allSprites = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile =='P':
                    self.player = Player(self, col, row)            
        self.camera = Camera(self.map.width, self.map.height)
                    

    def run(self):
        # Run the game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        # Update the game 
        self.allSprites.update()
        self.camera.update(self.player)
    
    def events(self):
        # Process events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    
    def draw(self):
        # Draw the loop
        self.screen.fill(BLACK)
        self.drawGrid()
        for sprite in self.allSprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()
        
    def drawGrid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))
            
        
        
    def showStartScreen(self):
        pass
    
    def showGameOverScreen(self):
        pass
        
g = Game()
g.showStartScreen()
g.running = True 
 
while g.running:
    g.new()
    g.run()
    g.showGameOverScreen()
    
pg.quit()