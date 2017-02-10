from global_values import WALL_VALUE

class Algorithm(object):
    def __init__(self):
        self.name = None
        
    def get_feasible_dir(self, adj_distances, adj_visited):
        raise NotImplementedError('Please specify the algorithm')
        

class RightFirst(Algorithm):
    def __init__(self):
        super(RightFirst, self).__init__()
        self.name = 'right-first'
    
    def get_feasible_dir(self, adj_distances, adj_visited):
        if adj_distances[2] != WALL_VALUE:
            valid_index = 2
        elif adj_distances[1] != WALL_VALUE:
            valid_index = 1
        elif adj_distances[0] != WALL_VALUE:
            valid_index = 0
        else:
            valid_index = 3

        return valid_index
        
class NewFirst(Algorithm):
    def __init__(self):
        super(NewFirst, self).__init__()
        self.name = 'new-first'
        
    def get_feasible_dir(self, adj_distances, adj_visited):
        if adj_distances[2] != WALL_VALUE and adj_visited[2] != '*':
            valid_index = 2
        elif adj_distances[1] != WALL_VALUE and adj_visited[1] != '*':
            valid_index = 1
        elif adj_distances[0] != WALL_VALUE and adj_visited[0] != '*':
            valid_index = 0
        elif adj_distances[2] != WALL_VALUE:
            valid_index = 2
        elif adj_distances[1] != WALL_VALUE:
            valid_index = 1
        elif adj_distances[0] != WALL_VALUE:
            valid_index = 0
        else:
            valid_index = 3
        
        return valid_index
    
    
class FloodFill(Algorithm):
    
    def __init__(self):
        super(FloodFill, self).__init__()
        self.name = 'flood-fill'
        
    def get_feasible_dir(self, adj_distances, adj_visited):
        valid_dir= adj_distances.index(min(adj_distances))
        possible_distance = WALL_VALUE
        for i, dist in enumerate(adj_distances):
                # Prefer unvisited cells
            if dist != WALL_VALUE and adj_visited[i] is '':
                if dist <= possible_distance:
                    valid_dir = i
                    smallest_distance = dist
                    possible_distance = smallest_distance
                    # Index 1: forwarding
                    # go forward as much as possible 
                    if valid_dir == 1:
                        break
        return valid_dir
    