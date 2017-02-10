from cell import Cell
from global_values import (dir_reverse, dir_sensors, wall_reverse, directions, wall_index, MAX_DISTANCES, WALL_VALUE)

                              
                              
class Training:
    def __init__(self, maze_dim):
        self.maze_dim = maze_dim
        self.grid = [[Cell() for i in range(maze_dim)] for j in range(maze_dim)]
        self.initial_distance()
        self.last_visited_cell = None
        self.cells_to_check = []
        self.visited_before_reaching_destination = []
        
        
    
    def initial_distance(self):
        '''
        initial the distance of the maze assuming there are no walls. 
        '''
        
        center = self.maze_dim/2
        max_dist = self.maze_dim - 2
        
        # lower left half 
        for i in range(center):
            for j in range(center):
                self.grid[i][j].distance = max_dist - i - j
        
        # top left half
        for i in range(center, self.maze_dim):
            for j in range(center):
                self.grid[i][j].distance = self.grid[self.maze_dim - i - 1][j].distance
                
        # right half
        for i in range(self.maze_dim):
            for j in range(center, self.maze_dim):
                self.grid[i][j].distance = self.grid[i][self.maze_dim - j - 1].distance


    # update the cell 
    def update(self, x, y, heading, walls, explore):
        '''
        Here we update the cell's information
        '''
        cell = self.grid[x][y]
        
        # record the real walls if the cell is frist time visited
        if cell.visited == '':
            cell.real_walls = walls
            # here we updated the walls of the adjacent's wall
            # since two adjacent cells share the wall
            self.update_adj_walls(x,y,walls,'real')            
        cell.visited = directions[heading]            
        self.change_visual_prev_cell(cell, explore)           
        self.last_visited_cell = cell            
        self.update_dist()
            
    # drawing the maze
    
    def print_row(self, cells, include_delimiters = True):
        if include_delimiters:
            roof = ''
            frame = '\n'
            floor = '\n'
            
            for cell in cells:
                roof += cell.roof()
                frame += cell.frame()
                floor += cell.floor()
            res = roof + frame + floor
        else:
            frame = ''
            for cell in cells:
                frame += cell.frame()
            res = frame
        
        print(res)
        
    def print_row_overlap(self, cells):
        roof = ''
        frame = '\n'
        floor = '\n'
            
        for cell in cells:
            roof += cell.roof()
            frame += cell.frame()
            floor += cell.floor()
        res = roof + frame + floor
    
        print(res)
    
    def draw(self):
        rows = []
        for i in range(self.maze_dim):
            rows.append([x[i] for x in self.grid])

        print_delimiters = True
        for i, row in enumerate(reversed(rows)):
            self.print_row(row, print_delimiters)
            print_delimiters = not print_delimiters  # Flip value
            
    
    def draw_overlap(self):
        rows = []
        for i in range(self.maze_dim):
            rows.append([x[i] for x in self.grid])

        for i, row in enumerate(reversed(rows)):
            self.print_row_overlap(row)

    def get_percentage_of_maze_explored(self):
        num_cells_in_maze = self.maze_dim * self.maze_dim
        num_cells_explored = len(self.visited_before_reaching_destination)
        return (num_cells_explored * 100) / num_cells_in_maze    
    
    
    # method for updating the locations and directions
    
    def change_visual_prev_cell(self, cur_cell, explore):
        if (self.last_visited_cell is not None) and (self.last_visited_cell != cur_cell) and (self.last_visited_cell.visited is not 'd'):
            if not explore:
                self.last_visited_cell.visited = '*'
            else:
                self.last_visited_cell.visited = 'e'
    
    def update_virtual_walls(self, x, y, virtual_walls):
        cell = self.grid[x][y]
        
        cell.virtual_walls = virtual_walls
        self.update_adj_walls(x, y, virtual_walls, 'virtual')
        
        self.update_dist()
    
    def get_index_of_wall(self, direction):
        return wall_index[direction]    
    
    
    def get_dist(self, x, y, direction, steps = 1):
        # get the distance of the cell of next move
        
        #print type(cell)
        walls = self.grid[x][y].get_all_walls()        
        dist = WALL_VALUE
        
        # up
        if direction == 'u' or direction == 'up':
            if walls[wall_index['u']] == 0 and self.is_valid_togo(x,y+steps):
                cell = self.grid[x][y+steps]
                #dist = cell.distance
                dist = self.grid[x][y+steps].distance
        
        # right
        if direction == 'r' or direction == 'right':
            if walls[wall_index['r']] == 0 and self.is_valid_togo(x+steps,y):
                cell = self.grid[x+steps][y]
                #dist = cell.distance
                dist = self.grid[x+steps][y].distance
        
        # down
        if direction == 'd' or direction == 'down':
            if walls[wall_index['d']] == 0 and self.is_valid_togo(x,y-steps):
                cell = self.grid[x][y-steps]
                dist = cell.distance
                #dist = self.grid[x][y-steps].distance
        
        # left
        if direction == 'l' or direction == 'left':
            if walls[wall_index['l']] == 0 and self.is_valid_togo(x-steps,y):
                cell = self.grid[x-steps][y]
                dist = cell.distance
                #dist = self.grid[x-steps][y].distance
        
        return dist
        
    def get_visited(self, x, y, direction, steps= 1):
        # get the visited-flag of the cell of next move
        
        #print type(self.grid[x][y])
        #print x
        #print y
        #print self.grid[x][y]
        walls = self.grid[x][y].get_all_walls()
        visited = ''
        
        # up
        if direction == 'u' or direction == 'up':
            if walls[wall_index['u']] == 0 and self.is_valid_togo(x,y+steps):
                visited = self.grid[x][y+steps].visited
        
        # right
        if direction == 'r' or direction == 'right':
            if walls[wall_index['r']] == 0 and self.is_valid_togo(x+steps,y):
                visited = self.grid[x+steps][y].visited
        
        # down
        if direction == 'd' or direction == 'down':
            if walls[wall_index['d']] == 0 and self.is_valid_togo(x,y-steps):
                visited = self.grid[x][y-steps].visited
        
        # left
        if direction == 'l' or direction == 'left':
            if walls[wall_index['l']] == 0 and self.is_valid_togo(x-steps,y):
                visited = self.grid[x-steps][y].visited
        
        return visited

    def get_adjacent(self, x,y, heading, sensors, get_behind = True):
        '''
        return the information of the four adjacent cells 
        including the distance and the vistied flags
        with the visual of the robot (left, up(ahead), right, down(behind))
        relative directions
        '''
        
        distances = list(MAX_DISTANCES)
        visited = ['']*4
        
        for i in range(len(sensors)):
            if sensors[i] != 0:
                dir_sensor = dir_sensors[heading][i]
                distances[i] = self.get_dist(x,y,dir_sensor)
                visited[i] = self.get_visited(x,y,dir_sensor)
                
                
        # update the cell behind the robot
        if get_behind:
            behind = dir_reverse[heading]
            distances[3] = self.get_dist(x,y,behind)
            visited[3] = self.get_visited(x,y,behind)
                
        return distances, visited 
        
        
    def get_adj_dist(self, x, y):
        '''
        get the distances of adjacent of current cells
        absolute directions
        '''
        distances = list(MAX_DISTANCES)
        distances[0] = self.get_dist(x,y,'left')
        distances[1] = self.get_dist(x,y,'up')
        distances[2] = self.get_dist(x,y,'right')
        distances[3] = self.get_dist(x,y,'down')
        
        
        return distances
        
    
    def update_dist(self, last_update = False):
        
        if last_update:
            cells_check = list(self.visited_before_reaching_destination)
            
        else:
            cells_check = self.cells_to_check
        
        while len(cells_check) != 0:
            current_cell = cells_check.pop()
            
            x = current_cell[0]
            y = current_cell[1]
            
            cur_dist = self.grid[x][y].distance
            
            adj_distances = self.get_adj_dist(x,y)
            min_dist = min(adj_distances)
            
            if cur_dist != min_dist+1 and cur_dist != WALL_VALUE:
                self.grid[x][y].distance = min_dist+1
                
                for i, adj_distance in enumerate(adj_distances):
                    if adj_distance != WALL_VALUE:
                        # left
                        #print 'i =', i
                        if i == 0:
                            x_add = x-1
                            y_add = y
                        # up
                        elif i == 1:
                            x_add = x
                            y_add = y+1
                        # right
                        elif i == 2:
                            x_add = x+1
                            y_add = y
                        else:
                            x_add = x
                            y_add = y-1
                        
                        cell_add = self.grid[x_add][y_add]
                        if cell_add.visited != 'd' and self.is_valid_togo(x_add, y_add):
                            cell_location = [x_add, y_add]
                            self.cells_to_check.append(cell_location)
                            


    def is_valid_togo(self, x, y):
        return (0 <= x <= self.maze_dim - 1) and (0 <= y <= self.maze_dim - 1)

    
    
    def reset_visited(self):
        for x in range(self.maze_dim):
            for y in range(self.maze_dim):
                self.grid[x][y].visited = ''
    
    def update_adj_walls(self, x, y, walls, wall_type):

        # up
        if self.is_valid_togo(x,y+1):
            wall = wall_reverse['up']
            #print wall
            new_x = x
            new_y = y+1
            value = walls[1]
            self.set_wall(new_x, new_y, value, wall, wall_type)
        
        # right
        if self.is_valid_togo(x+1,y):
            wall = wall_reverse['right']
            new_x = x+1
            new_y = y
            value = walls[2]
            self.set_wall(new_x, new_y, value, wall, wall_type)
        
        # down
        if self.is_valid_togo(x,y-1):
            wall = wall_reverse['down']
            #print 'aaaa'
            new_x = x
            new_y = y-1
            value = walls[3]
            self.set_wall(new_x, new_y, value, wall, wall_type)
        
        # left
        if self.is_valid_togo(x-1,y):
            wall = wall_reverse['left']
            new_x = x-1
            new_y = y
            value = walls[0]
            self.set_wall(new_x, new_y, value, wall, wall_type)
        
        

        
    def set_wall(self, x, y, value, wall_ind, wall_type):
        '''
        set the value of rean and virtual walss for a cell
        '''
        if wall_type == 'real':
            self.grid[x][y].real_walls[wall_ind] = value
        elif wall_type == 'virtual':
            self.grid[x][y].virtual_walls[wall_ind] = value

    
    def set_virtual_walls_for_unvisited(self):
        '''
        after the first round, we all virtual walls to all the unvisited cells
        '''
        for x in range(self.maze_dim):
            for y in range(self.maze_dim):
                cell = self.grid[x][y]
                if cell.visited == '':
                    cell.distance = WALL_VALUE
                    for i in range(4):
                        cell.virtual_walls[i] = 1
    
