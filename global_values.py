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

directions = {'u': '^', 'r': '>', 'd': 'v', 'l': '<',
               'up': '^', 'right': '>', 'down': 'v', 'left': '<'}
               
# index of the 4-wall: more specifically it is the index of the direction

wall_index = {'l': 0, 'u': 1, 'r': 2, 'd': 3,
              'left': 0, 'up': 1, 'right': 2, 'down': 3}


wall_reverse = {'u': 3, 'r': 0, 'd': 1, 'l': 2,
              'up': 3, 'right': 0, 'down': 1, 'left': 2}

WALL_VALUE = 10000
MAX_DISTANCES = [WALL_VALUE, WALL_VALUE, WALL_VALUE, WALL_VALUE]

rotations = {'0': -90, '1': 0, '2': 90}