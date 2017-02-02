import numpy as np
from global_values import (dir_move, dir_reverse, dir_sensors, wall_reverse,
                              directions, wall_index, MAX_DISTANCES,
                              WALL_VALUE)
from training import Training                              



class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''

        self.location = [0, 0]
        self.heading = 'up'
        self.maze_dim = maze_dim
        
        self.moves_round_1 = 0
        self.moves_round_2 = 0
        
        center = maze_dim /2
        self.destination = [[center, center], [center-1, center],
                            [center, center-1], [center-1, center-1]]
                    
        self.reach_dest = False
        self.explore = False
        self.moves_explore = 0
        
        self.training = Training(maze_dim)
             
        self.algorithm = None        
        
        
        if str(sys.argv[2]).lower() == 'ff':
            self.algorithm = FloodFill()
        elif str(sys.argv[2]).lower() == 'rf':
            self.algorithm = RightFirst()
        elif str(sys.argv[2]).lower() == 'nf':
            self.algorithm = NewFirst()
        else:
            raise ValueError(
                "Incorrect algorithm name. Options are: "
                "\n- 'ff': flood-fill"
                "\n- 'rf': keep-right"
                "\n- 'nf': modified-right (prefers unvisited cells)"
            )        
        
        
        
        
        

    def next_move(self, sensors):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''

        rotation = 0
        movement = 0
        
        x, y, heading = self.get_current_location()
        walls = self.current_walls(x, y, heading, sensors)
        
        
        if self.is_at_centers(x, y):
            rotation = 0
            movement = -1
            
            self.training.update(x, y, heading, walls, self.explore)
            
            self.reach_dest = True
            
            self.explore = True
        
        else:
            self.training.cells_to_check.append([x,y])
            if [x,y] not in self.visited_before_reaching_destination:
                self.visited_before_reaching_destination.append([x,y])
                
            self.training.update(x,y,heading, walls, self.explore)
                
            rotation, movement = self.get_next_move(x,y,heading,sensors)
                
        
        self.update_location(rotation, movement)
        if rotation == 'Reset' and movement == 'Reset':
            self.reset_to_home()
            
        if self.location in self.destination and self.moves_round_2 != 0:
            self.report_results()
            
        return rotation, movement
        
        
    def reset_to_home(self):
        self.location = [0, 0]
        self.heading = 'up'
            
    def get_current_location(self):
        heading = self.heading
        x = self.location[0]
        y = self.location[1]
        return x, y, heading
    
    def is_starting_location(self, x, y):
        return x == 0 and y == 0
    
    def is_at_centers(self, x, y):
        return [x,y] in self.destination
    
    def is_at_deadend(self, sensors):
        x, y, heading = self.get_current_location()
        
        adj_distances, adj_visited = self.get_adjacent(x,y,heading,sensors, False)
        
        return sensors == [0,0,0] or adj_distances == MAX_DISTANCES
    
    def current_walls(self, x, y, heading, sensors):
        if self.is_starting_location(x,y):
            walls = [0,1,1,1]
            
        elif self.training.grid[x][y].visited != '':
            walls = self.training.grid[x][y].get_all_walls()
        
        else:
            walls = [0,0,0,0]
            wall_sensors = [1 if k == 0 else 0 for k in sensors]
            
            for i in range(len(sensors)):
                dir_sensor = dir_sensors(heading)[i]
                index = wall_index[dir_sensor]
                walls[index] = wall_sensors[i]
            
            index = wall_index[dir_reverse[heading]]
            walls[index] = 0
        return walls
    
    def get_new_dir(self, rotation):
        if rotation == -90:
            return dir_sensors[self.heading][0]
        elif rotation == 90:
            return dir_sensors[self.heading][2]
        else:
            return self.heading
        
    def update_location(self, rotation, movement):
        if movement == 'Reset' or rotation == 'Reset':
            return
        else:
            movement = int(movement)
            
            self.heading = self.get_new_dir(rotation)
            
            if movement == -1:
                self.location[0] -= dir_move[self.heading][0]
                self.location[1] -= dir_move[self.heading][1]
            else:
                while movement > 0:
                    self.location[0] += dir_move[self.heading][0]
                    self.location[1] += dir_move[self.heading][1]
                    movement -= 1
    
    def num_walls(self, sensors):
        num_of_walls = 0
        for sensor in sensors:
            if sensor == 0:
                num_of_walls += 1
        return num_of_walls
        
    # movement
    def get_next_move(self, x, y, heading, sensors):
        if self.reach_dest and self.explore:
            rotation, movement = self.explore(x,y,heading,sensors)
            self.moves_explore += 1
        
        elif not self.reach_dest and not self.explore:
            if self.algorithm.name  == 'flood-fill' and self.is_at_deadend(sensors):
                rotation, movement = self.act_on_deadend(x, y, heading)
            else:
                adj_distances, adj_visited = self.training.get_adjacent(x, y, heading, sensors)
                valid_index = self.algorithm.get_feasible_dir(adj_distances, adj_visited)
                rotation, movement = self.convert_index_to_dir(valid_index)
            self.move_round_1 += 1
        
        else:
            if self.move_round_2 == 0:
                print "--------- Final Report ---------"
                self.training.draw()
            rotation, movement = self.second_round(x,y,heading,sensors)
            self.move_round_2 += 1
        return rotation, movement
    
    
        
                
            
        
            
        
        
                
        
                
                
                    
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        