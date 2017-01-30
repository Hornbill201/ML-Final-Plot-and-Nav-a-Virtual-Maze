from global_values import WALL_VALUE

class Cell: 
    ''' 
    This class stands for the cell in the maze. 
    We generate the real-wall and virtual-wall for the the cell
    The cell also has a distance to the destination, and a flag indicates
    whether this cell has been visited before(visited),
    visited: ^,>,v,<, d: deadend, *:visited
    '''
    
    def __inf__(self, real_walls = None, distance = 0, visited = ''):
        '''
        real_wall: list of '0'(no wall) and '1'(real wall) [u,r,d,l]
        distance: (int) distance from the current cell to the destination
        visited: (Boolean) indicate whether this cell has been visited 
        '''
        if not real_walls:
            real_walls = [0,0,0,0]
        
        self.real_walls = real_walls # the real walls in the maze
        self.virtual_walls = [0,0,0,0] # virtual walls added to avoid deadend
        self.distance = distance
        self.visited = visited
    
    def get_all_walls(self):
        '''
        return all the walls of the cell
        including all the real walls and the virtual walls
        '''
        all_walls = [0,0,0,0]
        for i in range(len(self.real_walls)):
            if self.real_walls[i] == 1 or self.virtual_walls[i] == 1:
                all_walls[i] = 1
        return all_walls
    '''
    Structure of the cell
    + --- +   ---> roof: --- (real wall), ... (virtual wall)
    | dis |   ---> frame: | (real wall), : (virtual wall)
    + --- +   ---> floor (same as roof)      
    '''
        
    def roof(self, overlap = False):
        '''
        Constructure the roof of the cell
        overlap: (boolean) only True if we want to print the individual cell
        Flase when we print the entire maze (adjacent cells share walls)
        return: return the strucure of the roof
        '''
        roof_line = '+'
        if self.real_walls[0]:
            roof_line += ' --- '
        elif self.virtual_walls[0]:
            roof_line += ' ... '
        else:
            roof_line += '     '
        if overlap:
            roof_line += '+'
        return roof_line
    
    def frame(self, overlap = False):
        '''
        Constructure the frame of the cell
        overlap: (boolean) only True if we want to print the individual cell
        Flase when we print the entire maze (adjacent cells share walls)
        return: return the strucure of the frame
        '''
        
        if self.distance == WALL_VALUE:
            distance = 'x'
        else:
            distance = str(self.distance)
        
        frame_wall = ''
        if self.real_walls[3]:
            frame_wall += '|'
        elif self.virtual_walls[3]:
            frame_wall += ':'
        else:
            frame_wall += ' '
        
        frame_wall += ' '
        if len(distance) == 1:
            frame_wall += ' '
        
        frame_wall += distance
        if len(self.visited)==0:
            frame_wall += ' '
        frame_wall += self.visited
        frame_wall += ' '
            
        if overlap:
            if self.real_walls[1]:
                frame_wall += '|'
            elif self.virtual_walls[1]:
                frame_wall += ':'
            else:
                frame_wall += ' '
        
        return frame_wall
    
    def floor(self, overlap = False):
        '''
        Constructure the floor of the cell
        overlap: (boolean) only True if we want to print the individual cell
        Flase when we print the entire maze (adjacent cells share walls)
        return: return the strucure of the floor
        '''
        floor_line = '+'
        if self.real_walls[2]:
            floor_line += ' --- '
        elif self.virtual_walls[2]:
            floor_line += ' ... '
        else:
            floor_line += '     '
        if overlap:
            floor_line += '+'
        return floor_line
        
    def __str__(self):
        '''
        assemble for an individual cell with all its walls 
        '''
        cell = '\n'
        cell += self.roof(overlap = True)
        cell += '\n'
        cell += self.frame(overlap = True)
        cell += '\n'
        cell += self.floor(overlap = True)
        cell += '\n'
        return cell