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
SCORE_FILE = "score.txt"
FONT = 'Arial'

CONTROLS = "Classic"


TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
WALL_IMG = 'wall.png'


#Gun Settings
BULLET_IMG = 'tile_187.png'
BULLET_SPEED = 500     # How fast the bullet travels
BULLET_LIFETIME = 1000 # When the bullet kills itself in "milliseconds"
BULLET_RATE = 150      # Delay between shots
BARREL_OFFSET = vec(30, 10) # Don't change this, this controls where the bullet spawn relative to player
KICKBACK = 200         # Recoil; how much shooting sends the player back.  This may be changed
GUN_SPREAD = 8         # How much the bullets deviates
BULLET_DAMAGE = 10     # Self explanatory
PELLETS = 1
CURRENT_GUN = "pistol"

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
MOB_SCORE = 10
MOB_LAYER = 1

SHOOTER_IMG = 'robot1_gun.png'
SHOOTER_ROT_SPEED = 5
SHOOTER_HEALTH = 200
SHOOTER_SCORE = 15

#BOSS settings
BOSS_IMG = 'Dragon50percent.png'
BOSS_HEALTH = 2500
BOSS_HIT_RECT = pg.Rect(0, 0, 125, 125)
FIRE_IMG = 'fireball.png'
EXPLOSION_KNOCKBACK = 50
FIREBALL_SPEED = 200
FIREBALL_OFFSET = vec(50, 0) #controls where fireball spawns
FIREBALL_DAMAGE = 30
FIREBALL_SPREAD = 2
FIREBALL_LAYER = 2
