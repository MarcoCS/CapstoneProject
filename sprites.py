
#################################################
#CS30 Final Capstone Project
#Developers: Kale, Dallas, Marco
#
#Player and hostile sprites
#################################################
import pygame as pg
from math import atan2, degrees, pi
from random import uniform
from settings import *
import settings
from tilemap import collide_hit_rect
vec = pg.math.Vector2
from random import choice

def collide_with_walls(sprite, group, dir):
    # Handles each direction separately. This function is used for both
    # the player and mobs.
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery =  sprite.pos.y



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):

        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.weapon = "Pistol"
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        # Directional controls
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys [pg.K_s]:
            self.vel = vec(-PLAYER_SPEED, 0).rotate(-self.rot)


        if pg.mouse.get_pressed()[0] == 1: # Shooting button
            now = pg.time.get_ticks()
            if now - self.last_shot > settings.BULLET_RATE:
                self.last_shot = now
                for x in range(settings.PELLETS): # This is for things like shotguns and stuff
                    dir = vec(1, 0).rotate(-self.rot)
                    pos = self.pos + settings.BARREL_OFFSET.rotate(-self.rot)
                    Bullet(self.game, pos, dir)
                    self.vel = vec(-settings.KICKBACK, 0).rotate(-self.rot)


    def update(self):
        # Code which dictates where player is facing
        self.mouse_pos = pg.mouse.get_pos()        # Gets the point of the mouse
        dx = self.mouse_pos[0] - (self.pos.x + self.game.camera.x)               # Subtracts from center points
        dy = self.mouse_pos[1] - (self.pos.y + self.game.camera.y)
        rads = atan2(-dy,dx) # Basic trigonometry of the two points
        rads %= 2*pi # Converts to rads
        degs = degrees(rads) # Converts to degrees


        self.get_keys()
        self.rot = degs
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        #uses the new rectangle instead of the rectangle of the sprite
        self.rect.center = self.hit_rect.center

class Weapons:
    class Shotgun(pg.sprite.Sprite):
        def __init__(self, game, x, y):
            self.groups = game.allSprites, game.shotgun
            pg.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            self.def_image = game.shotgun_img
            self.size = self.def_image.get_size()
            self.image = pg.transform.scale(self.def_image, (int(self.size[0]/2), int(self.size[1]/2)))
            self.rect = pg.Rect(0, 0, 55, 35)
            self.pos = vec(x, y) * settings.TILESIZE
            self.rect.center = self.pos


        def change_var():# Gun Characteristics:
            settings.BULLET_RATE = 500      # Rate of fire, delay between bullets
            settings.BULLET_LIFETIME = 850 # When the bullet kills itself in "milliseconds"
            settings.BULLET_SPEED = 500     # How fast the bullet travels
            settings.KICKBACK = 600         # Recoil; how much shooting sends the player back.  This may be changed
            settings.GUN_SPREAD = 20         # How much the bullets deviates
            settings.BULLET_DAMAGE = 45     # Self explanatory
            settings.PELLETS = 5            # Controls how many bullets will spawn

    class Starting_pistol(pg.sprite.Sprite):
        def __init__(self,game, x, y):
            self.groups = game.allSprites, game.pistol
            pg.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            self.def_image = game.pistol_img
            self.size = self.def_image.get_size()
            self.image = pg.transform.scale(self.def_image, (int(self.size[0]/3), int(self.size[1]/3)))
            self.rect = pg.Rect(0, 0, 35, 35)
            self.pos = vec(x, y) * settings.TILESIZE
            self.rect.center = self.pos

        def change_var():
            # Gun Characteristics:
            settings.BULLET_RATE = 250      # Rate of fire; delay between bullets
            settings.BULLET_LIFETIME = 1000 # When the bullet kills itself in "milliseconds"
            settings.BULLET_SPEED = 500     # How fast the bullet travels
            settings.KICKBACK = 200         # Recoil; how much shooting sends the player back.  This may be changed
            settings.GUN_SPREAD = 8         # How much the bullets deviates
            settings.BULLET_DAMAGE = 10     # Self explanatory
            PELLETS = 1            # Controlls How many bullets will spawn per trigger pull

    class Sniper_rifle(pg.sprite.Sprite):
        def __init__(self,game, x, y):
            self.groups = game.allSprites, game.sniper
            pg.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            self.def_image = game.sniper_img
            self.size = self.def_image.get_size()
            self.image = pg.transform.scale(self.def_image, (int(self.size[0]/2), int(self.size[1]/2)))
            self.rect = pg.Rect(0, 0, 55, 35)
            self.pos = vec(x, y) * settings.TILESIZE
            self.rect.center = self.pos

        def change_var():
            # Gun Characteristics:
            settings.BULLET_RATE = 1000       # Rate of fire; delay between bullets
            settings.BULLET_LIFETIME = 2000 # When the bullet kills itself in "milliseconds"
            settings.BULLET_SPEED = 2000    # How fast the bullet travels
            settings.KICKBACK = 350          # Recoil; how much shooting sends the player back.  This may be changed
            settings.GUN_SPREAD = 1         # How much the bullets deviates
            settings.BULLET_DAMAGE = 100     # Self explanatory
            settings.PELLETS = 1            # Controlls How many bullets will spawn per trigger pull

    class Assault_rifle(pg.sprite.Sprite):
        def __init__(self,game, x, y):
            self.groups = game.allSprites, game.ar
            pg.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            self.def_image = game.ar_img
            self.size = self.def_image.get_size()
            self.image = pg.transform.scale(self.def_image, (int(self.size[0]/2), int(self.size[1]/2)))
            self.rect = pg.Rect(0, 0, 55, 35)
            self.pos = vec(x, y) * settings.TILESIZE
            self.rect.center = self.pos

        def change_var():
            # Gun Characteristics:
            settings.BULLET_RATE = 150       # Rate of fire; delay between bullets
            settings.BULLET_LIFETIME = 1500 # When the bullet kills itself in "milliseconds"
            settings.BULLET_SPEED = 900    # How fast the bullet travels
            settings.KICKBACK = 250          # Recoil; how much shooting sends the player back.  This may be changed
            settings.GUN_SPREAD = 10         # How much the bullets deviates
            settings.BULLET_DAMAGE = 25     # Self explanatory
            settings.PELLETS = 1            # Controlls How many bullets will spawn per trigger pull


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.allSprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos

        spread = uniform(-settings.GUN_SPREAD, settings.GUN_SPREAD)
        self.vel = dir.rotate(spread) * settings.BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > settings.BULLET_LIFETIME:
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mobImage
        self.rect = self.image.get_rect()
        self.hit_rect = settings.MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * settings.TILESIZE
        self.vel = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = choice(settings.MOB_SPEEDS)
        self.health = settings.MOB_HEALTH

    def avoidMobs(self):
        # This function keeps mobs spread out
        for mob in self.game.mobs:
            if mob != self:
                distance = self.pos - mob.pos
                if 0 < distance.length() < settings.AVOID_RADIUS:
                    self.acc += distance.normalize()

    def update(self):
        # Rotate mobs and update the images. They track the player.
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.mobImage, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoidMobs()
        # This self.acc.scale_to_length adjusting to speed simulates friction.
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            HPUP(self.game, self.pos)
            self.kill()

    def drawHealth(self):
        if self.health > 60:
            col = settings.GREEN
        elif self.health > 30:
            col = settings.YELLOW
        else:
            col = settings.RED
        width = int(self.rect.width * self.health / settings.MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < settings.MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)


class HPUP(pg.sprite.Sprite): # Health up
    def __init__(self, game, pos):
        self.groups = game.allSprites, game.hpups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(pos)
        self.image = game.hpupImage
        self.rect = self.image.get_rect()
        self.hit_rect = settings.MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.rect.center = self.pos


class StationaryMob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.shooters
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.shooterImage
        self.rect = self.image.get_rect()
        self.hit_rect = settings.MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * settings.TILESIZE
        self.vel = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.last_shot = 0
        self.health = SHOOTER_HEALTH

    def update(self):
        # Stationary mobs don't move so they need no position updates
        # They just rotate to get line-of-sight on the player
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.shooterImage, self.rot)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        #uses the new rectangle instead of the rectangle of the sprite
        self.rect.center = self.hit_rect.center
        now = pg.time.get_ticks()
        if now - self.last_shot > 4500:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + settings.BARREL_OFFSET.rotate(-self.rot)
            ShooterBullet(self.game, pos, dir)
        if self.health <= 0:
            self.kill()

    def drawShooterHealth(self):
        if self.health > 60:
            col = settings.GREEN
        elif self.health > 30:
            col = settings.YELLOW
        else:
            col = settings.RED
        width = int(self.rect.width * self.health / settings.SHOOTER_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < settings.SHOOTER_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

class ShooterBullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.allSprites, game.shooterBullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-settings.GUN_SPREAD, settings.GUN_SPREAD)
        self.vel = dir.rotate(spread) * settings.BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > settings.BULLET_LIFETIME:
            self.kill()
