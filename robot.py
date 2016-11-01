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

    def draw(self, sensors):
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

            self.map[location[1]][location[0]] = 1

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
        if abs(move) > 0:
            for i in range(move):
                location = self.go_ahead(1)
                self. fill_wall(location)
                self.location = self.go_ahead(2)

    def make_turn(self, degree):
        dirs = dir_sensors[self.heading]
        heading = dirs[degree // 90 + 1]
        return heading

    def is_valid_move(self, move):
        if move < 0:
            heading = dir_reverse[self.heading]
        for i in range(2 * abs(move)):
            location = self.go_ahead(i + 1)
            if self.map[location[1]][location[0]] == 1:
                return False
        return True




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

        rotation = random.choice([-90, 0, 90])
        movement = 1
        print sensors
        print self.heading
        self.draw(sensors)



        for row in self.map:
             print row


        self.heading = self.make_turn(rotation)
        if self.is_valid_move(movement) == True:
            self.make_move(movement)
        return rotation, movement