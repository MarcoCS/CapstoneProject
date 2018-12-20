##-------------------------------------------------------------------
## Top Down Shooter - Main program
## Dallas Spendelow
## November 28, 2018
## This program contains the game class, that runs the game.
##-------------------------------------------------------------------

import pygame as pg
from sprites import *
from tilemap import *
from os import path
import settings 
from random import *
from settings import *

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
        
    def loadData(self):
        self.gameFolder = path.dirname("__file__")
        img_folder = path.join(self.gameFolder, 'img')
        self.map = Map(path.join(self.gameFolder, 'map.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mobImage = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.shooterImage = pg.image.load(path.join(img_folder, SHOOTER_IMG)).convert_alpha()
        # Weapon sprites:
        self.shotgun_img = pg.image.load(path.join(img_folder, "Shotgun.png")).convert_alpha()
        self.pistol_img = pg.image.load(path.join(img_folder, "ColtPixel.png")).convert_alpha()
        self.ar_img = pg.image.load(path.join(img_folder, "M16.png")).convert_alpha()
        self.sniper_img = pg.image.load(path.join(img_folder, "HuntingRifle.png")).convert_alpha()
        self.font = pg.font.match_font(FONT)
         #load score file
        with open(path.join(self.gameFolder, SCORE_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
            
    def new(self):
        # Start a new game
        self.score = 0
        self.paused = False
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.shooters = pg.sprite.Group()
        self.shooterBullets = pg.sprite.Group()      
        # Weapon sprites
        self.shotgun = pg.sprite.Group()
        self.sniper = pg.sprite.Group()
        self.pistol = pg.sprite.Group()
        self.ar = pg.sprite.Group()
        # -------

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
                if tile == 'W':
                    roll = randint(1,4)
                    if roll == 1:
                        Weapons.Shotgun(self, col, row)
                        print(col, row)
                    if roll == 3:
                        Weapons.Starting_pistol(self, col, row)
                    if roll == 2:
                        Weapons.Sniper_rifle(self, col, row)
                    if roll == 4:
                        Weapons.Assault_rifle(self, col, row)
                    
        self.camera = Camera(self.map.width, self.map.height)
                    
    def run(self):
        # Run the game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    
    def update(self):
        # Update the game 
        self.allSprites.update()
        self.camera.update(self.player)
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
            hit.health -= settings.BULLET_DAMAGE
            hit.vel = vec(0, 0)   
            self.score += 5
        
        # Bullet/shooter collision
        hits = pg.sprite.groupcollide(self.shooters, self.bullets, False, True)
        for hit in hits:
            hit.health -= settings.BULLET_DAMAGE
            self.score += 5
    
        # Player/shooter collisions
        hits = pg.sprite.spritecollide(self.player, self.shooterBullets, True, False)
        for hit in hits:
            self.player.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
                
        # Detection of weapon pickup
        hits = pg.sprite.spritecollide(self.player, self.shotgun, True, False)
        if hits:
            Weapons.Shotgun.change_var()
            
        hits = pg.sprite.spritecollide(self.player, self.pistol, True, False)
        if hits:
            Weapons.Starting_pistol.change_var()
            
        hits = pg.sprite.spritecollide(self.player, self.sniper, True, False)
        if hits:
            Weapons.Sniper_rifle.change_var()
        
        hits = pg.sprite.spritecollide(self.player, self.ar, True, False)
        if hits:
            Weapons.Assault_rifle.change_var()
    

            
    def events(self):
        # Process events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.paused = not self.paused
    
    def draw(self):
        # Draw the loop
        # This displays frame rate.
        pg.display.set_caption(TITLE)
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
        if self.paused:
            self.showPauseScreen()
        self.drawText(str(round(self.clock.get_fps(),2)), self.font, 20, WHITE, WIDTH - 50, 20)
        pg.display.flip()
        
    def drawText(self, text, fontName, size, color, x, y):
        font = pg.font.Font(fontName, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.center = (x, y)
        self.screen.blit(textSurface, textRect)
        

    def drawGrid(self):
        ## Draws a grid with size equal to TILESIZE
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))           
        
    def showStartScreen(self):
        # Draws the start screen with a colour, and displays the controls.
        # It will wait for the user to press a key, then start the game.
        self.screen.fill(BGCOLOR)
        self.drawText("Shooter Game", self.font, 72, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Up/Down or W/S to move. Left/Right or A/D to rotate.", self.font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 100)
        self.drawText("Space to fire, p to pause", self.font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 150)
        self.drawText("Press any key to play", self.font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 200)
        self.drawText("High Score: " + str(self.highscore), self.font, 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.waitForKey()
    
    def showPauseScreen(self):
        self.drawText("Paused", self.font, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawText("Current Score: " + str(self.score), self.font, 22, WHITE, WIDTH / 2, HEIGHT / 2 - 50) 
        
        
    def showGameOverScreen(self):
        # Draw the game over screen and wait for a key input to start new
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.drawText("Game Over", self.font, 72, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Press any key to play again", self.font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 100)
        if self.score > self.highscore:
           self.highscore = self.score
           self.drawText("New High Score! " + str(self.highscore), self.font, 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)  
           with open(path.join(self.gameFolder, SCORE_FILE), 'w') as f:
               f.write(str(self.highscore))
               f.close()
        else:
           self.drawText("High Score: " + str(self.highscore), self.font, 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.waitForKey()
    
    def waitForKey(self):
        # Keeps time ticking until a key is pressed. Then returns. 
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    keyPressed = True
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False              
        
g = Game()
g.showStartScreen()
g.running = True 

while g.running:
    g.new()
    g.run()
    g.showGameOverScreen()
    
pg.quit()
