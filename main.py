##-------------------------------------------------------------------
## Top Down Shooter - Main program
## Dallas Spendelow
## November 28, 2018
## This program contains the game class, that runs the game.
##-------------------------------------------------------------------

import pygame as pg
from settings import *
from sprites import *
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
        gameFolder = path.dirname("__file__")
        img_folder = path.join(gameFolder, 'img')
        self.map = Map(path.join(gameFolder, 'map.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mobImage = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
                
    def new(self):
        # Start a new game
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self, col, row)     
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
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
        #bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
        # Player/mob collsions. 
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        if hits:
            self.playing = False
    
    def events(self):
        # Process events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    
    def draw(self):
        # Draw the loop
        # This displays frame rate.
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BLACK)
        self.drawGrid()
        for sprite in self.allSprites:
            if isinstance(sprite, Mob):
                sprite.drawHealth()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #testing rectangle for collisions
        #pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()
        
    def drawGrid(self):
        ## Draws a grid with size equal to TILESIZE
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))           
        
        
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
