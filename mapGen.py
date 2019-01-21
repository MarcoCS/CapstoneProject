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
base_room = [['1', '1', '1', '1', '.', '.', '1', '1', '1', '1'],  # This cuts down render time
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # Before, a function was located in "Rooms_tools" which carved out an area
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # We do this anyways, so it simply saves compute power to have a pre-made map.
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '1', '1', '1', '.', '.', '1', '1', '1', '1']]

base_room_top = [['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],  # This cuts down render time
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # Before, a function was located in "Rooms_tools" which carved out an area
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # We do this anyways, so it simply saves compute power to have a pre-made map.
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '1', '1', '1', '.', '.', '1', '1', '1', '1']
                ]

base_room_bottom = [['1', '1', '1', '1', '.', '.', '1', '1', '1', '1'],  # This cuts down render time
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # Before, a function was located in "Rooms_tools" which carved out an area
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # We do this anyways, so it simply saves compute power to have a pre-made map.
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
                ]

base_room_top_right = [['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],  # This cuts down render time
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # Before, a function was located in "Rooms_tools" which carved out an area
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # We do this anyways, so it simply saves compute power to have a pre-made map.
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
                ]

base_room_top_left = [['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],  # This cuts down render time
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # Before, a function was located in "Rooms_tools" which carved out an area
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # We do this anyways, so it simply saves compute power to have a pre-made map.
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '1', '1', '1', '.', '.', '1', '1', '1', '1']
                ]

base_room_bottom_left = [['1', '1', '1', '1', '.', '.', '1', '1', '1', '1'],  # This cuts down render time
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # Before, a function was located in "Rooms_tools" which carved out an area
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # We do this anyways, so it simply saves compute power to have a pre-made map.
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
                ]

base_room_bottom_right = [['1', '1', '1', '1', '.', '.', '1', '1', '1', '1'],  # This cuts down render time
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # Before, a function was located in "Rooms_tools" which carved out an area
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # We do this anyways, so it simply saves compute power to have a pre-made map.
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
                ]

base_room_bottom = [['1', '1', '1', '1', '.', '.', '1', '1', '1', '1'],  # This cuts down render time
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # Before, a function was located in "Rooms_tools" which carved out an area
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # We do this anyways, so it simply saves compute power to have a pre-made map.
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
                ]

base_room_right = [['1', '1', '1', '1', '.', '.', '1', '1', '1', '1'],  # This cuts down render time
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # Before, a function was located in "Rooms_tools" which carved out an area
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # We do this anyways, so it simply saves compute power to have a pre-made map.
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '1', '1', '1', '.', '.', '1', '1', '1', '1']
                ]

base_room_left = [['1', '1', '1', '1', '.', '.', '1', '1', '1', '1'],  # This cuts down render time
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # Before, a function was located in "Rooms_tools" which carved out an area
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],   # We do this anyways, so it simply saves compute power to have a pre-made map.
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '.', '.', '.', '.', '.', '.', '.', '.', '1'],
                ['1', '1', '1', '1', '.', '.', '1', '1', '1', '1']
                ]
# --------------------------------------------------------
class Enemy_room:
    def __init__(self, player_level, room):
        self.room = copy.deepcopy(room)
        self.room = generate_walls(self.room)
        self.room = copy.deepcopy(self.room)
        amount_of_enemies = player_level * 4
        for num_enemies in range(amount_of_enemies): # Will spawn the corresponding amount of enemies
            x_rand = rand.randint(2,len(self.room[0]) - 2)
            y_rand = rand.randint(2,len(self.room[0]) - 2)
            self.room[y_rand][x_rand] = "M"

class Spawn_room:
    def __init__(self):
        type_of_room = base_room_bottom_left
        self.room = copy.deepcopy(base_room_top_left)
        self.room[5][5] = "P" # Due to limitations with how maps are structured (even number), it is not possible to place the player spawn
        self.room[0][5] = "1"             # Exactly in the middle
        self.room[0][4] = "1"  
   
class Loot_room:
    def __init__(self, room):
        self.room = copy.deepcopy(room)
        self.room[5][5] = "W"

class Boss_room:
    def __init__(self):
        self.room = copy.deepcopy(base_room_bottom_right)
        self.room[5][5] = "B"
        self.room[9][5] = "1"             # Exactly in the middle
        self.room[9][4] = "1"

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
    return map

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
        if x > 0 and x < 3 and z > 0  and z < 3:
            type_of_room = base_room
        else:
            if x == 0:
                type_of_room = base_room_left
            else:
                type_of_room = base_room_right
            
            if z == 0:
                if x == 3:
                    type_of_room = base_room_top_right
                else:
                    type_of_room = base_room_top
            if z == 3:
                if x == 0:
                    type_of_room = base_room_bottom_left
                else:
                    type_of_room = base_room_bottom    
        if roll == 1:
            game_map[z][x] = Loot_room(type_of_room).room
        else:
            game_map[z][x] = Enemy_room(1,type_of_room).room

        
game_map[0][0] = Spawn_room().room
game_map[3][3] = Boss_room().room

map_list = []
map_list1 = []
map_list2 = []
map_list3 = []
# I did this because, I was too incompetent to do this via a forloop
map_list.append(zip(game_map[0][0],game_map[0][1],game_map[0][2],game_map[0][3]))
map_list1.append(zip(game_map[1][0],game_map[1][1],game_map[1][2],game_map[1][3]))
map_list2.append(zip(game_map[2][0],game_map[2][1],game_map[2][2],game_map[2][3]))
map_list3.append(zip(game_map[3][0],game_map[3][1],game_map[3][2],game_map[3][3]))

# Unpacking 
map_list = zip(*map_list)
map_list1 = zip(*map_list1)
map_list2 = zip(*map_list2)
map_list3 = zip(*map_list3)



for x in map_list:
    y = str(x)
    y = y.translate({ord(i): None for i in "[]()', "})
    map_file.write(y)
    print(y)
    map_file.write("\n")

for x in map_list1:
    y = str(x)
    y = y.translate({ord(i): None for i in "[]()', "})
    map_file.write(y)
    print(y)
    map_file.write("\n")

for x in map_list2:
    y = str(x)
    y = y.translate({ord(i): None for i in "[]()', "})
    map_file.write(y)
    print(y)
    map_file.write("\n")

for x in map_list3:
    y = str(x)
    y = y.translate({ord(i): None for i in "[]()', "})
    map_file.write(y)
    print(y)
    map_file.write("\n")

map_file.close()
# Writing the map to the text file
