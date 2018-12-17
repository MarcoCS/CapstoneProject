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
import random

# HUD functions
def drawPlayerHealth(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
    
class Game:
    def __init__(self):
        # Initialize pygame
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.loadData()
        self.font_name = pg.font.match_font(FONT_NAME)
        
    def loadData(self):    
        #loading graphics
        gameFolder = path.dirname("__file__")
        img_folder = path.join(gameFolder, 'img')
        self.map = Map(path.join(gameFolder, 'map.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mobImage = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.shooterImage = pg.image.load(path.join(img_folder, SHOOTER_IMG)).convert_alpha()
        healthupImages = {}
        healthupImages['normalheal'] = pg.image.load(path.join(img_folder, HEALTHUP_POWER)).convert_alpha()
        healthupImages['superheal'] = pg.image.load(path.join(img_folder, SUPERHEALTHUP_POWER)).convert_alpha()
        #load score file
        with open(path.join(gameFolder, SCORE_FILE), 'w') as f:
            try:
                self.score = int(f.read())
            except:
                self.score = 0
                
    def new(self):
        # Start a new game
        self.score = 0
        self.allSprites = pg.sprite.Group()
        self.healthPower = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.shooters = pg.sprite.Group()
        self.shooterBullets = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self, col, row)     
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'S':
                    StationaryMob(self, col, row)
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
        #player hits health powerup
        hits = pg.sprite.spritecollide(self.player, self.healthPower, True)
        for hit in hits:
            if hit.type == 'normalheal':
                if self.player.health < 100:
                    self.player.health += 20
                    if self.player.health > 100:
                        self.player.health = 100
            if hit.type == 'superheal':
                if self.player.health < 100:
                    self.player.health += 50
                    if self.player.health > 100:
                        self.player.health = 100
        #mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
            if hits:
                self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
                
        #bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)         
            self.score += 5
            if random.random() > 0.9:
                healthpower = Healthpower(self, hit.rect.center)
                allSprites.add(healthpower)
            
        # Player/shooter collisions
        hits = pg.sprite.spritecollide(self.player, self.shooterBullets, True, False)
        for hit in hits:
            self.player.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
          
        # Bullet/shooter collision
        hits = pg.sprite.groupcollide(self.shooters, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            self.score += 5
            
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
            if isinstance(sprite, StationaryMob):
                sprite.drawShooterHealth()
            if isinstance(sprite, Mob):
                sprite.drawHealth()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #testing rectangle for collisions
            #pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        #Drawing the player's health bar
        drawPlayerHealth(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text(str(self.score), 18, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        
    def drawGrid(self):
        ## Draws a grid with size equal to TILESIZE
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))           
          
    def showStartScreen(self):
        #self.draw_text("High Score: " + str(self.score), 22, WHITE, WIDTH / 2, 15)
        pass
    
    def showGameOverScreen(self):
        #self.draw_text("Your Score: " + str(self.score), 22, WHITE, WIDTH / 2, 15)
        #if self.score > self.highscore:
        #   self.highscore = self.score
        #   self.draw_text("New High Score!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)  
        #   with open(path.join(gameFolder, SCORE_FILE), 'w') as f:
        #       f.write(str(self.score))
        #else:
        #   self.draw_text("High Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pass
    
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        
        
g = Game()
g.showStartScreen()
g.running = True 
 
while g.running:
    g.new()
    g.run()
    g.showGameOverScreen()
    
pg.quit()
