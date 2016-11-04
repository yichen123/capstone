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

#helper functions:
def dist(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return sqrt(dx ** 2 + dy ** 2)


class Map(object):
    def __init__(self, maze_dim):
        self.maze_dim = maze_dim
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
        x = maze_location[0] * 2 + 1
        y = self.dim - maze_location[1] * 2 - 2
        # print maze_location, location, self.dim
        return [x, y]


    def update_map(self, robot_location, direction, distance):
        location = self.pos_map(robot_location)
        location1 = [0, 0]
        changed = False
        y = location[0] + dir_move[direction][0] * (distance * 2 + 1)
        x = location[1] + dir_move[direction][1] * (distance * 2 + 1)
        # print location, direction, location1
        if 0 <= x < self.dim and 0 <= y < self.dim:
            if self.map[x][y] != 1:
                self.map[x][y] = 1
                changed = True
        #print changed
        return changed


    def pos_ahead(self, location, direction):
        return [location[0] + dir_move[direction][0], location[1] + dir_move[direction][1]]


    def is_valid_move(self, robot_location, direction):
        # if the wall is next to the robot in that direction, return false
        location = self.pos_map(robot_location)
        location1 = self.pos_ahead(location, direction)
        if 0 > location1[1] or self.dim <= location1[1] or 0 > location1[0] or self.dim <= location1[0]:
            return False
        if self.map[location1[1]][location1[0]] == 1:
            return False
        return True



    def is_goal(self, maz_location):
        # see if that location is in the corner of a 3 * 3 square of 0's

        # return False if not, and True otherwise
        location = self.pos_map(maz_location)
        #print location, maz_location
        # print location
        for i in range(3):
            for j in range(3):
                location1 = [location[0] + j, location[1] + i]
                if self.map[location1[1]][location1[0]] == 1:
                    return False
        # print 'good! ' + str(location)
        for i in range(3):
            for j in range(3):
                location1 = [location[0] + j, location[1] + i]
                #print location1
        return True

    def is_connect(self, pos1, pos2):
        location1 = self.pos_map(pos1)
        location2 = self.pos_map(pos2)
        location = [(location1[0] + location2[0]) / 2, (location1[1] + location2[1]) / 2]
        if self.map[location[1]][location[0]] == 0:
            return True
        else:
            return False















