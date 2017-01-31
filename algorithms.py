from global_values import WALL_VALUE

class Algorithm(object):
    def __init__(self):
        self.name = None
        
    def get_feasible_dir(self, adj_distances, adj_visited):
        raise NotImplementedError('Please specify the algorithm')
        

class KeepRight(Algorithm):
    def __init__(self):
        super(KeepRight, self).__init__()
        self.name = 'keep-right'
    
    def get_feasible_dir(self, adj_distances, adj_visited):
        if adj_distances[1] != WALL_VALUE:
            valid_index = 1
        elif adj_distances[0] != WALL_VALUE:
            valid_index = 0
        elif adj_distances[3] != WALL_VALUE:
            valid_index = 3
        else:
            valid_index = 2

        return valid_index
        
