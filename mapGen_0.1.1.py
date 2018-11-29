# Procedural map generation program
# Created on 22/"1""1"/20"1"8 # Format: DD/MM/YYYY
# By: Marco Sin
# -------------------------------------
import math
import random as rand


map_file = open("map_file.txt","w+")

# 0 should represent walkable floor
# "1" should represent an impassable wall
# "2" should represent a door which can be opened
# "3" are enemies
# "P" is player

base_room = [["1","1","1","1","1","1","1","1","1","1"],
             ["1","1","1","1","1","1","1","1","1","1"],
             ["1","1","1","1","1","1","1","1","1","1"],
             ["1","1","1","1","1","1","1","1","1","1"],
             ["1","1","1","1","1","1","1","1","1","1"],
             ["1","1","1","1","1","1","1","1","1","1"],
             ["1","1","1","1","1","1","1","1","1","1"],
             ["1","1","1","1","1","1","1","1","1","1"],
             ["1","1","1","1","1","1","1","1","1","1"],
             ["1","1","1","1","1","1","1","1","1","1"]
            ]


# Walls should be "1" unit thin


def create_walk(map):  # Map_file txt should be read as (y,x) or [y][x]
    temp = map
    y_length = len(temp)
    x_length = len(temp[0])
    for i in range(1, y_length - 1):
        for k in range(1, x_length - 1):  
            temp[i][k] = "0"
    map = temp
    


def generate_map(max_rooms):
    


for line in map:
    for char in line:
        map_file.write(char)
    map_file.write("\n")
map_file.close()