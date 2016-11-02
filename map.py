'''
We construct map class for two reasons.
first, we need to record walls while moving. we need to expand the dimension from maze for space of walls
socond, the coordinate systems are different between the maze and oridnate system. 

Note that the odd number of coordinates are wall and cannot step into.

'''

# global dictionaries for robot movement and sensing
dir_sensors = {'u': ['l', 'u', 'r'], 'r': ['u', 'r', 'd'],
               'd': ['r', 'd', 'l'], 'l': ['d', 'l', 'u'],
               'up': ['l', 'u', 'r'], 'right': ['u', 'r', 'd'],
               'down': ['r', 'd', 'l'], 'left': ['d', 'l', 'u']}
dir_move = {'u': [0, -1], 'r': [1, 0], 'd': [0, 1], 'l': [-1, 0],
            'up': [0, -1], 'right': [1, 0], 'down': [0, 1], 'left': [-1, 0]}
dir_reverse = {'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r',
               'up': 'd', 'right': 'l', 'down': 'u', 'left': 'r'}

class Map(object):
    def __init__(self, maze_dim):
        self.dim = maze_dim * 2 + 1
        self.map = [[0 for col in range(self.dim)] \
                for row in range(self.dim)]

    def get_map(self):
        for row in self.map:
            print row


    def pos_map(self, maze_location):
        '''
        transfer from maze coordinates to map coordinate
        '''
        location = [maze_location[0] * 2 + 1, self.dim - maze_location[1] * 2 -2]
        # print maze_location, location, self.dim
        return location


    def update_map(self, robot_location, direction, distance):
        location = self.pos_map(robot_location)
        location1 = [0, 0]
        location1[0] = location[0] + dir_move[direction][0] * (distance * 2 + 1)
        location1[1] = location[1] + dir_move[direction][1] * (distance * 2 + 1)
        # print location, direction, location1
        self.map[location1[1]][location1[0]] = 1

    def fill_wall(self, robot_location, direction):
        # update walls for unsteped position

        location = self.pos_map(robot_location)
        location = self.pos_ahead(location, direction)
        dirs = dir_sensors[direction]
        location1 = [location[0] + dir_move[dirs[0]][0], location[1] + dir_move[dirs[0]][1]]
        self.map[location1[1]][location1[0]] = 1
        location1 = [location[0] + dir_move[dirs[2]][0], location[1] + dir_move[dirs[2]][1]]
        self.map[location1[1]][location1[0]] = 1


    def pos_ahead(self, location, direction):
        return [location[0] + dir_move[direction][0], location[1] + dir_move[direction][1]]


    def is_valid_move(self, robot_location, direction):
        # if the wall is next to the robot in that direction, return false
        location = self.pos_map(robot_location)
        location1 = self.pos_ahead(location, direction)
        if self.map[location1[1]][location1[0]] == 1:
            return False
        return True














