# Procedural map generation program
# Created on 22/"1""1"/20"1"8 # Format: DD/MM/YYYY
# By: Marco Sin
# -------------------------------------
import random as rand


map_file = open("map_file.txt","w+")

# "." should represent walkable floor
# "1" should represent an impassable wall
# "2" should represent a door which can be opened
# "E" are enemies
# "P" is player

# Templates of rooms:

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
class Rooms:
    def __init__(self):
        self.room = []
    
    class Enemy_room:
        def __init__(self, player_level):
            self.room = base_room  # Creates a copy of the base room
            Rooms.create_walk(self.room) # Carves areas into the base room
            Rooms.generate_walls(self.room)
            amount_of_enemies = player_level * 4
            for num_enemies in range(amount_of_enemies): # Will spawn the corresponding amount of enemies
                x_rand = rand.randint(2,len(self.room[0]) - 2)
                y_rand = rand.randint(2,len(self.room[0]) - 2)
                self.room[y_rand][x_rand] = "E"
    
    class Spawn_room:
        def __init__(self):
            self.room = base_room
            Rooms.create_walk(self.room)
            self.room[5][5] = "P" # Due to limitations with how maps are structured, it is not possible to place the player spawn
                                  # Exactly in the middle
    
    
    
    def create_walk(map):  # Map_file txt should be read as (y,x) or [y][x]  In reality, this shouldn't matter tho
        temp = map
        y_length = len(temp)
        x_length = len(temp[0]) 
        for i in range(1, y_length - 1):         # Carves out a basic room
            for k in range(1, x_length - 1):     # Iterates between the first and last element of each line
                temp[i][k] = "."
        map = temp
  
    def generate_walls(map): # Will create line segments for cover for the player, and unfortunately enemies
        temp = map
        rand_walls = rand.randint(2,4)    # Rolls for the amount of walls that will spawn
        print(rand_walls)
        for i in range(rand_walls):       # Spawns walls for the rolled amount
            random_length = rand.randint(2,4)  # Rolls for the length of the wall segment
            role_direction = rand.randint(0,1) # Rolls for a vertical or horizontal wall
            rand_point = {"y":rand.randint(2, len(temp) - 5), "x":rand.randint(2,len(temp[0]) - 3)}
            try:     # Will continue to attempt to create walls or it will just break the loop if too many attempts fail
                for x in range(random_length):
                    map[rand_point["y"]][rand_point["x"]] = "1"
                    if role_direction == 1:
                        map[rand_point["y"] + x][rand_point["x"]] = "1"
                    else:
                        map[rand_point["y"]][rand_point["x"] + x] = "1"
            except:   
                pass # If it fails the attempt, it will pass and deem that the room is impossible to generate.
                
            
        
        



roomx = Rooms.Spawn_room()
for x in roomx.room:
    print(x)
    


for line in roomx.room:
    for char in line:
        map_file.write(char)
    map_file.write("\n")
map_file.close()