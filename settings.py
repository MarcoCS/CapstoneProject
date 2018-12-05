#################################################
#CS30 Final Capstone Project
#Developers: Kale, Dallas, Marco
#
#Settings
#################################################
import pygame as pg
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

# Player settings
PLAYER_SPEED = 300.0
PLAYER_ROT_SPEED = 5
PLAYER_IMG = 'hitman1_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
