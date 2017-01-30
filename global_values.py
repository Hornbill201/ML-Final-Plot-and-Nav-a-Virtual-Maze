# the global variables that will be used in this project

# these variables are default defined. 
dir_sensors = {'u': ['l', 'u', 'r'], 'r': ['u', 'r', 'd'],
               'd': ['r', 'd', 'l'], 'l': ['d', 'l', 'u'],
               'up': ['l', 'u', 'r'], 'right': ['u', 'r', 'd'],
               'down': ['r', 'd', 'l'], 'left': ['d', 'l', 'u']}
               
               
dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
            'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}
            
            
dir_reverse = {'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r',
               'up': 'd', 'right': 'l', 'down': 'u', 'left': 'r'}
               

# direction symbols used in the Maze visualizatrion (plotting the path)

symbol_move = {'u': '^', 'r': '>', 'd': 'v', 'l': '<',
               'up': '^', 'right': '>', 'down': 'v', 'left': '<'}
               
# index of the 4-wall: more specifically it is the index of the direction

wall_index = {'u': 0, 'r': 1, 'd': 2, 'l': 3,
              'up': 0, 'right': 1, 'down': 2, 'left': 3}


WALL_VALUE = 10000
MAX_DISTANCES = [WALL_VALUE, WALL_VALUE, WALL_VALUE, WALL_VALUE]

