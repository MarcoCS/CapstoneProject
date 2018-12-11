# Procedural temp generation program
# Created on 22/11/2018 # Format: DD/MM/YYYY
# By: Marco Sin
# -------------------------------------
import random as rand
import copy

map_file = open("map_file.txt","w+")

# "." should represent walkable floor
# "1" should represent an impassable wall
# "2" should represent a door which can be opened
# "E" are enemies
# "P" is player



# Debug function

def print_lst(lst): # Prints the list
    for x in lst:
        print(x)


# **** Notes from Marco:  *****
# The deep copy is required because Python utilizes an optimization technique where "copying" is actually just a reference to that object
# E.g. list_a = copy(list_b) just has the two things set to eachother.  Any change to list_a simultaneously changes list_b


# Templates of rooms:
base_room = [['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],  # This cuts down render time
            ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # Before, a function was located in "Rooms_tools" which carved out an area
            ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # We do this anyways, so it simply saves compute power to have a pre-made map.
            ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
            ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
            ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
            ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
            ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
            ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
            ]

empty_room = [[".",".",".",".",".",".",".",".",".","."],
                     [".",".",".",".",".",".",".",".",".","."],
                     [".",".",".",".",".",".",".",".",".","."],
                     [".",".",".",".",".",".",".",".",".","."],
                     [".",".",".",".",".",".",".",".",".","."],
                     [".",".",".",".",".",".",".",".",".","."],
                     [".",".",".",".",".",".",".",".",".","."],
                     [".",".",".",".",".",".",".",".",".","."],
                     [".",".",".",".",".",".",".",".",".","."],
                     [".",".",".",".",".",".",".",".",".","."]
                    ]

# --------------------------------------------------------
class Enemy_room:
    def __init__(self, player_level):
        self.room = copy.deepcopy(base_room)
        generate_walls(self.room)
        amount_of_enemies = player_level * 4
        for num_enemies in range(amount_of_enemies): # Will spawn the corresponding amount of enemies
            x_rand = rand.randint(2,len(self.room[0]) - 2)
            y_rand = rand.randint(2,len(self.room[0]) - 2)
            self.room[y_rand][x_rand] = "E"

class Spawn_room:
    def __init__(self):
        self.room = copy.deepcopy(base_room)
        self.room[5][5] = "P" # Due to limitations with how maps are structured (even number), it is not possible to place the player spawn
                     # Exactly in the middle

class Loot_room:
    def __init__(self):
        self.room = copy.deepcopy(base_room)
        self.room[5][5] = "L"

class Boss_room:
    def __init__(self):
        self.room = copy.deepcopy(base_room)
        self.room[5][5] = "B"

def generate_walls(map): # Will create line segments for cover for the player, and unfortunately enemies
    temp = copy.deepcopy(map)
    rand_walls = rand.randint(2,4)# Rolls for the amount of walls that will spawn
    for i in range(rand_walls):       # Spawns walls for the rolled amount
        random_length = rand.randint(2,4)  # Rolls for the length of the wall segment
        role_direction = rand.randint(0,1) # Rolls for a vertical or horizontal wall
        rand_point = {"y":rand.randint(2, len(temp) - 5), "x":rand.randint(2,len(temp[0]) - 5)}
        try:     # Will continue to attempt to create walls or it will just break the loop if too many attempts fail
            for x in range(random_length):
                temp[rand_point["y"]][rand_point["x"]] = "1"
                if role_direction == 1:
                    temp[rand_point["y"] + x][rand_point["x"]] = "1"
                else:
                    temp[rand_point["y"]][rand_point["x"] + x] = "1"
        except:
            print("Failed to generate")
            pass # If it fails the attempt, it will pass and deem that the room is impossible to generate given the current configuration.
    map = copy.deepcopy(temp)

#game_temp = [[],[],[],[],[],
 #           [],[],[],[],[],
  #          [],[],[],[],[],
   #         [],[],[],[],[]
    #        ]

# Generating the game map
game_map = [[[],[],[],[]],
            [[],[],[],[]],
            [[],[],[],[]],
            [[],[],[],[]]]
# This is our blank template map ^^^
omega_map = [] # This will be the final once everything is processed


# Generator
for z in range(len(game_map)):                # First layer of list
    for x in range(len(game_map[0])):         # Secondary layer of nested list
        roll = rand.randint(1,6)
        if roll == 1:
            game_map[z][x] = Loot_room().room
        else:
            game_map[z][x] = Enemy_room(1).room
game_map[0][0] = Spawn_room().room
game_map[3][3] = Boss_room().room

for z in range(len(game_map)):                # First layer of list
    for x in range(len(game_map[0])):         # Secondary layer of nested list  # Third layer
        for line in game_map[z][x]:
            print(line)

for z in range(len(game_map[0][0])): # This will change the the last element accessed game_map[?][?][z]
    temp = ""
    for x in range(len(game_map[0])): # This will change game_map[?][x][?]
        for y in range(len(game_map)):
            print(game_map[y][x][z])
            temp += "".join(game_map[y][x][z])
    map_file.write(temp)
    map_file.write("\n")
map_file.close()
# Writing the map to the text file
