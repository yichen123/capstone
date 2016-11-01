import numpy as np
import random
# global dictionaries for robot movement and sensing
dir_sensors = {'u': ['l', 'u', 'r'], 'r': ['u', 'r', 'd'],
               'd': ['r', 'd', 'l'], 'l': ['d', 'l', 'u'],
               'up': ['l', 'u', 'r'], 'right': ['u', 'r', 'd'],
               'down': ['r', 'd', 'l'], 'left': ['d', 'l', 'u']}
dir_move = {'u': [0, -1], 'r': [1, 0], 'd': [0, 1], 'l': [-1, 0],
            'up': [0, -1], 'right': [1, 0], 'down': [0, 1], 'left': [-1, 0]}
dir_reverse = {'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r',
               'up': 'd', 'right': 'l', 'down': 'u', 'left': 'r'}

class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''

        self.heading = 'up'
        self.maze_dim = maze_dim
        self.map = [[0 for col in range(self.maze_dim * 2 + 1)] \
                for row in range(self.maze_dim * 2 + 1)]
        self.visited = [[0 for col in range(self.maze_dim * 2 + 1)] \
                for row in range(self.maze_dim * 2 + 1)]
        self.location = [1, 2 * self.maze_dim - 1]
        self.map[self.location[1]][self.location[0]] = 0

    def update_map(self, sensors):
        '''
        Use this function to record sensor result for constructing map.
        '''
        dirs = dir_sensors[self.heading]
        for i in range(len(sensors)):
            location = [0, 0]
            location[0] = self.location[0]+ dir_move[dirs[i]][0] * (2 * sensors[i] + 1)
            location[1] = self.location[1]+ dir_move[dirs[i]][1] * (2 * sensors[i] + 1)
            # print dirs[i], sensors[i]
            # print location
            #print location, sensors[i], self.location, dirs[i]
            self.map[location[1]][location[0]] = 1

    def get_map(self):
        for row in self.map:
            print row
    def get_location(self):
        location = [self.location[0] // 2, (self.maze_dim * 2 - self.location[1]) // 2]
        return location

    def go_ahead(self, step):
        location = [0, 0]
        location[0] = self.location[0] + dir_move[self.heading][0] * step
        location[1] = self.location[1] + dir_move[self.heading][1] * step
        return location

    def fill_wall(self, location):
        dirs = dir_sensors[self.heading]
        location2 = [0, 0]
        location3 = [0, 0]
        location2[0] = location[0] + dir_move[dirs[0]][0]
        location2[1] = location[1] + dir_move[dirs[0]][1]
        location3[0] = location[0] + dir_move[dirs[2]][0]
        location3[1] = location[1] + dir_move[dirs[2]][1]
        self.map[location2[1]][location2[0]] = 1
        self.map[location3[1]][location3[0]] = 1

    def make_move(self, move):
        location = self.go_ahead(1)
        self.fill_wall(location)
        self.location = self.go_ahead(2)

    def make_turn(self, degree):
        dirs = dir_sensors[self.heading]
        heading = dirs[degree // 90 + 1]
        return heading

    def execute(self, rotation, movement):
        self.heading = self.make_turn(rotation)
        if movement < 0:
            self.heading = dir_reverse[self.heading]
        for i in range(abs(movement)):
            if self.is_valid_move(1) == True:
                self.make_move(1)
        if movement < 0:
            self.heading = dir_reverse[self.heading]

    def is_valid_move(self, move):
        location = self.go_ahead(1)
        if 0 > location[0] or location[0] > self.maze_dim * 2 or 0 > location[1] or location[1] > self.maze_dim * 2:
            return False
        if self.map[location[1]][location[0]] == 1:
            return False
        location = self.go_ahead(2)
        if 0 > location[0] or location[0] > self.maze_dim * 2 or 0 > location[1] or location[1] > self.maze_dim * 2:
            return False

        return True

    def walk_randomly(self):
        rotation = random.choice([-90, 0, 90])
        #rotation = 0
        movement = random.choice([-3, -2, -1, 0, 1, 2, 3])
        return [rotation, movement]




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

        rotation, movement = self.walk_randomly()
        # print 'location: ' +  str(self.get_location())
        # print 'heading: ' + self.heading
        self.update_map(sensors)
        self.execute(rotation, movement)

        return rotation, movement