# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 14:22:59 2017

@author: Chao Wang
"""


from cell import Cell
from global_values import (dir_reverse, dir_sensors, wall_reverse,
                              directions, wall_index, MAX_DISTANCES,
                              WALL_VALUE)
                              
                              
class Train:
    def __init__(self, maze_dim):
        self.maze_dim = maze_dim
        self.grid = [[Cell() for i in range(maze_dim)] for j in range(maze_dim)]
        self.init_distances()
        self.last_visited_cell = None
        self.cells_to_check = []
        self.visited_before_reaching_destination = []
        
        
    
    def init_distance(self):
        '''
        initial the distance of the maze assuming there are no walls. 
        '''
        center = self.maze_dim/2
        max_dist = self.maze_dim - 2
        
        # top left half 
        for i in range(center):
            for j in range(center):
                self.grid[i][j].distance = max_dist - i - j
        
        # lower left half
        for i in range(center, self.maze_dim):
            for j in range(center):
                self.grid[i][j].distance = self.grid[self.maze_dim - i - 1][j]
                
        # right half
        for i in range(self.maze_dim):
            for j in range(center, self.maze_dim):
                self.grid[i][j].distance = self.grid[i][self.maze_dim - j - 1]
    

    # update the cell 
    def update(self, x, y, heading, walls, explore):
        '''
        Here we update the cell
        '''
        cell = self.grid[x][y]
        
        # record the real walls if the cell is frist time visited
        if cell.visited == '':
            cell.real_walls = walls
            # hear we updated the walls of the adjacent's wall
            # since two adjacent cells share the wall
            self.update_adj_walls(x,y,walls,'real')
            
        cell.visited = directions[heading]
            
        self.change_visual_prev_cell(cell, explore)
            
        self.last_visited_cell = cell
            
        self.update_dist()
            
    
    def change_visual_prev_cell(self, cur_cell, explore):
        if self.last_visited_cell is not None \
                and self.last_visited_cell != cur_cell \
                and self.last_visited_cell.visited is not 'd':
                    if not explore:
                        self.last_visited_cell.visited = '*'
                    else:
                        self.last_visited_cell.visited = 'e'
    
    def update_virtual_walls(self, x, y, virtual_walls):
        cell = self.grid[x][y]
        
        cell.virtual_walls = virtual_walls
        self.update_adj_walls(x, y, virtual_walls, 'virtual')
        
        self.update_dist()
        
    def get_dist(self, x, y, direction, steps = 1):
        walls = self.grid[x][y].get_all_walls()
        dist = WALL_VALUE
        
        # up
        if direction == '0' or direction == 'up':
            if walls[wall_index['u']] == 0 and self.is_valid_togo(x,y+steps):
                cell = self.grid[x][y+steps]
                dist = cell.distance
        
        # right
        if direction == '1' or direction == 'right':
            if walls[wall_index['r']] == 0 and self.is_valid_togo(x+steps,y):
                cell = self.grid[x+steps][y]
                dist = cell.distance
        
        # down
        if direction == '2' or direction == 'down':
            if walls[wall_index['d']] == 0 and self.is_valid_togo(x,y-steps):
                cell = self.grid[x][y-steps]
                dist = cell.distance
        
        # left
        if direction == '3' or direction == 'left':
            if walls[wall_index['l']] == 0 and self.is_valid_togo(x-steps,y):
                cell = self.grid[x-steps][y]
                dist = cell.distance
        
        return dist
                







    def is_valid_togo(self, x, y):
        return 0 <= x <= self.maze_dim - 1 and 0 <= y <= self.maze_dim - 1












        
                