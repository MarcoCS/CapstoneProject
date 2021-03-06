#################################################
#CS30 Final Capstone Project
#Developers: Kale, Dallas, Marco
#
#Main file. Runs the game. 
#################################################

import pygame as pg
from sprites import *
from tilemap import *
from os import path
import settings
from random import *
from settings import *
import mapGen
# HUD functions
def drawPlayerHealth(surf, x, y, pct): # Surf short for surface
    if pct < 0: # Pct short for percentage of healthbar
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x % 100, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:   
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
    
def drawBossHealth(surf, x, y, pct): # Surf short for surface
        if pct < 0: # Pct short for percentage of healthbar
            pct = 0
        BAR_LENGTH = 1000
        BAR_HEIGHT = 15
        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(WIDTH / 2, HEIGHT + 25, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x % 100, y, fill, BAR_HEIGHT)
        if pct > 0.6:
            col = GREEN
        elif pct > 0.3:   
            col = YELLOW
        else:
            col = RED
        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 4)



class Game:
    def __init__(self):
        # Initialize pygame
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.loadData()
        # Loading cursor
        pg.mouse.set_cursor(*pg.cursors.broken_x)


    def loadData(self):
        self.gameFolder = path.dirname("__file__")
        img_folder = path.join(self.gameFolder, 'img')
        self.msc_folder = path.join(self.gameFolder, 'msc')
        snd_folder = path.join(self.gameFolder, 'snd')
        # Base map is 48 x 32 tiles. 
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mobImage = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.shooterImage = pg.image.load(path.join(img_folder, SHOOTER_IMG)).convert_alpha()
        self.hpupImage = pg.image.load(path.join(img_folder, "heart.png")).convert_alpha()
        self.floorImage = pg.image.load(path.join(img_folder, "floor.png")).convert_alpha()
        self.floorImage = pg.transform.scale(self.floorImage, (TILESIZE, TILESIZE)).convert_alpha()
        self.bossImage = pg.image.load(path.join(img_folder, BOSS_IMG)).convert_alpha()
        self.fireImage = pg.image.load(path.join(img_folder, FIRE_IMG)).convert_alpha()
        self.fireImage = pg.transform.scale(self.fireImage, (50, 50))
        self.wallImage = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wallImage = pg.transform.scale(self.wallImage, (TILESIZE, TILESIZE)).convert_alpha()
        
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
         #sound loading
       
        self.pickupgun = pg.mixer.Sound(path.join(snd_folder, 'Cocking Gun-SoundBible.com-327068561.wav'))
        self.healthpickup = pg.mixer.Sound(path.join(snd_folder, 'Healing Full.wav'))
        self.healthpickup.set_volume(0.2)
        self.assaultrifleshot = pg.mixer.Sound(path.join(snd_folder, 'M4A1_Single-Kibblesbob-8540445.wav'))
        self.assaultrifleshot.set_volume(0.2)
        self.snipershot = pg.mixer.Sound(path.join(snd_folder, 'Sniper_Fire_Reload-Mike_Koenig-1309646991.wav'))
        self.snipershot.set_volume(0.2)
        self.shotgunshot = pg.mixer.Sound(path.join(snd_folder, 'ie_shot_gun-luminalace-770179786.wav'))
        self.shotgunshot.set_volume(0.2)
        self.pistolshot = pg.mixer.Sound(path.join(snd_folder, '380_gunshot_single-mike-koenig.wav'))
        self.pistolshot.set_volume(0.2)
        self.playerhitsnd = pg.mixer.Sound(path.join(snd_folder, 'Jab-SoundBible.com-1806727891.wav'))
        self.zombiehitsnd = pg.mixer.Sound(path.join(snd_folder, 'Squish 1-SoundBible.com-662226724.wav'))
        self.zombiehurt = pg.mixer.Sound(path.join(snd_folder, 'Zombie Gets Attacked-SoundBible.com-20348330.wav'))
        self.shooterhit = pg.mixer.Sound(path.join(snd_folder, 'Large Metal Pan 2-SoundBible.com-1042326277.wav'))
        self.enemysnipershot = pg.mixer.Sound(path.join(snd_folder, 'Sniper_Fire_Reload-Mike_Koenig-1309646991.wav'))
        self.enemysnipershot.set_volume(0.1)
        self.dragongrowl = pg.mixer.Sound(path.join(snd_folder, 'Dragon Roaring-SoundBible.com-213390944.wav'))
        self.fireballsound =pg.mixer.Sound(path.join(snd_folder, 'Small Fireball-SoundBible.com-1381880822.wav'))
        

    def new(self):
        # Start a new game
        mapGen.main()
        self.map = Map(path.join(self.gameFolder, 'map_file.txt'))       
        self.score = 0
        self.win = False
        self.paused = False
        self.spawnedboss = False
        self.allSprites = pg.sprite.LayeredUpdates()
        self.allSprites = pg.sprite.Group()
        self.fireballs = pg.sprite.Group()
        self.bosses = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.shooters = pg.sprite.Group()
        self.shooterBullets = pg.sprite.Group()
        self.hpups = pg.sprite.Group()
        self.floorTiles = pg.sprite.Group()
        # Weapon sprites
        self.shotgun = pg.sprite.Group()
        self.sniper = pg.sprite.Group()
        self.pistol = pg.sprite.Group()
        self.ar = pg.sprite.Group()
        # -------
        
        Weapons.Starting_pistol.change_var()
        
        # Floor tiles
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile != '1':
                    Floor(self, col, row)

        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    roll = randint(1,4)
                    if roll < 3:
                        Mob(self, col, row)
                    if roll == 4:
                        StationaryMob(self, col, row)                 
                if tile == 'W':
                    roll = randint(1,4)
                    if roll == 1:
                        Weapons.Shotgun(self, col, row)
                    if roll == 3:
                        Weapons.Starting_pistol(self, col, row)
                    if roll == 2:
                        Weapons.Sniper_rifle(self, col, row)
                    if roll == 4:
                        Weapons.Assault_rifle(self, col, row)
                    
                    

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        # Run the game loop
        pg.mixer.music.load(path.join(self.msc_folder, 'espionage.ogg'))
        pg.mixer.music.play(loops=-1)
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
            self.playerhitsnd.play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
            if hits:
                self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
                
        #FIREBALL hits player
        hits = pg.sprite.spritecollide(self.player, self.fireballs, True, False)
        for hit in hits:
            self.playerhitsnd.play()
            self.player.health -= FIREBALL_DAMAGE
            if self.player.health <= 0:
                self.playing= False
                
        #bullets hit BOSS
        hits = pg.sprite.groupcollide(self.bosses, self.bullets, False, True)
        for hit in hits:
            self.dragongrowl.play()
            hit.health -= settings.BULLET_DAMAGE
            hit.vel = vec(0,0)
            self.score += 20

        #bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            self.zombiehitsnd.play()
            self.zombiehurt.play()
            hit.health -= settings.BULLET_DAMAGE
            hit.vel = vec(0, 0)
            self.score += 5

        # Bullet/shooter collision
        hits = pg.sprite.groupcollide(self.shooters, self.bullets, False, True)
        for hit in hits:
            self.shooterhit.play()
            hit.health -= settings.BULLET_DAMAGE
            self.score += 5

        # Player/shooter collisions
        hits = pg.sprite.spritecollide(self.player, self.shooterBullets, True, False)
        for hit in hits:
            self.playerhitsnd.play()
            self.player.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False

        # Detection of weapon pickup

        hits = pg.sprite.spritecollide(self.player, self.hpups, True, False)
        if hits:
            self.healthpickup.play()
            if self.player.health + 10 > 100:
                self.player.health = 100
            else:
                self.player.health += 10
                

        hits = pg.sprite.spritecollide(self.player, self.shotgun, True, False)
        if hits:
            Weapons.Shotgun.change_var()
            self.pickupgun.play()

        hits = pg.sprite.spritecollide(self.player, self.pistol, True, False)
        if hits:
            Weapons.Starting_pistol.change_var()
            self.pickupgun.play()

        hits = pg.sprite.spritecollide(self.player, self.sniper, True, False)
        if hits:
            Weapons.Sniper_rifle.change_var()
            self.pickupgun.play()

        hits = pg.sprite.spritecollide(self.player, self.ar, True, False)
        if hits:
            Weapons.Assault_rifle.change_var()
            self.pickupgun.play()
        
        if not bool(self.mobs) and not bool(self.shooters) and self.spawnedboss == False and not bool(self.bosses) and self.playing == True: 
            self.loadBoss()
         
 
     
    def loadBoss(self):
        self.spawnedboss = True
        for row, tiles in enumerate(self.map.data):
                for col, tile, in enumerate(tiles):
                    if tile == 'B':
                        self.boss = Boss(self, col, row)


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
#        self.drawGrid()
        for sprite in self.allSprites:
            if isinstance(sprite, StationaryMob):
                sprite.drawShooterHealth()
            if isinstance(sprite, Mob):
                sprite.drawHealth()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #testing rectangle for collisions  
        #pg.draw.rect(self.screen, WHITE, self.boss.hit_rect, 2)
        #Drawing the player's health bar
        drawPlayerHealth(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        if len(self.bosses) != 0:
            drawBossHealth(self.screen, WIDTH / 2, HEIGHT -20, self.boss.health / BOSS_HEALTH)
            self.drawText("Walter", self.font, 35, WHITE, WIDTH / 2, HEIGHT -35)
        if self.paused:
            self.showPauseScreen()
        self.drawText(str(round(self.clock.get_fps(),2)), self.font, 20, WHITE, WIDTH - 50, 20)
        self.drawText("Mobs: {}".format(len(self.mobs) + len(self.shooters)), self.font, 20, WHITE, 50, 50) 
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
        pg.event.wait()
        pg.mixer.music.load(path.join(self.msc_folder, 'battleThemeA.mp3'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.drawText("Shooter Game", self.font, 72, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Up/Down or W/S to move. Left/Right or A/D to rotate.", self.font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 100)
        self.drawText("Space to fire, p to pause", self.font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 150)
        self.drawText("Press any key to play", self.font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 200)
        self.drawText("High Score: " + str(self.highscore), self.font, 22, WHITE, WIDTH / 2, 15)
        self.drawText("Control method Press 'N' for WASD or 'M' for Classic Controls", self.font, 22, WHITE, WIDTH / 2, HEIGHT / 2 + 250)
        pg.display.flip()
        self.waitForKey()
        pg.mixer.music.fadeout(500)

    def showPauseScreen(self):
        self.drawText("Paused", self.font, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawText("Current Score: " + str(self.score), self.font, 22, WHITE, WIDTH / 2, HEIGHT / 2 - 50)


    def showGameOverScreen(self):
        # Draw the game over screen and wait for a key input to start new
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.msc_folder, 'Retro_No hope.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        if self.win:
            self.drawText("YOU WIN!", self.font, 72, WHITE, WIDTH / 2, HEIGHT / 2)
        else:
            self.drawText("Game Over", self.font, 72, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Press any key to play again", self.font, 20, WHITE, WIDTH / 2, HEIGHT / 2 + 120)
        if self.score > self.highscore:
           self.highscore = self.score
           self.drawText("New High Score! " + str(self.highscore), self.font, 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
           with open(path.join(self.gameFolder, SCORE_FILE), 'w') as f:
               f.write(str(self.highscore))
               f.close()
        else:
           self.drawText("High Score: " + str(self.highscore), self.font, 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
           self.drawText("Your Score: " + str(self.score), self.font, 22, WHITE, WIDTH / 2, HEIGHT / 2 + 80)
        pg.display.flip()
        self.waitForKey()

    def waitForKey(self):
        # Keeps time ticking until a key is pressed. Then returns.
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
                    self.running = True
        
g = Game()
g.showStartScreen()

while g.running:
    g.new()
    g.run()
    g.showGameOverScreen()

pg.quit()
