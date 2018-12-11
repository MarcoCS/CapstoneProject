
#################################################
#CS30 Final Capstone Project
#Developers: Kale, Dallas, Marco
#
#Settings
#################################################
import pygame as pg
vec = pg.math.Vector2

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#Game Settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Top-Down Shooter"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#Gun Settings
BULLET_IMG = 'tile_187.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
BARREL_OFFSET = vec(30, 10)
KICKBACK = 200
GUN_SPREAD = 8
BULLET_DAMAGE = 10

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300.0
PLAYER_ROT_SPEED = 5
PLAYER_IMG = 'soldier1_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# Mob settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEEDS = [100, 125, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
AVOID_RADIUS = 50
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20

SHOOTER_IMG = 'robot1_gun.png'
SHOOTER_ROT_SPEED = 5
SHOOTER_HEALTH = 200
SHOOTERBULLET_RATE = 38
