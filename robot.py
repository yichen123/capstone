import numpy as np
import random

from map import Map
# global dictionaries for robot movement and sensing
dirs = ['u', 'r', 'd', 'l']
dir_sensors = {'u': ['l', 'u', 'r'], 'r': ['u', 'r', 'd'],
               'd': ['r', 'd', 'l'], 'l': ['d', 'l', 'u'],
               'up': ['l', 'u', 'r'], 'right': ['u', 'r', 'd'],
               'down': ['r', 'd', 'l'], 'left': ['d', 'l', 'u']}
dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
            'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}
dir_reverse = {'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r',
               'up': 'd', 'right': 'l', 'down': 'u', 'left': 'r'}


# name of corners of goal_squares
goal_square = ['lt', 'rt', 'rb', 'lb']
# move should take when robot is at corners
goal_square_moves = ['r', 'd', 'l', 'u']

# initial parameteres
start = [0, 0]
start_heading = 'u'
cost = 1
max_step = 3

# tuning factors
beta = 0.

#helper functions:
def dist(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return sqrt(dx ** 2 + dy ** 2)

def print_list(alist):
    list2 = []
    for num in alist:
        num = str(num)
        if len(num) == 2:
            list2.append(num)
        else:
            num = '0' + num
            list2.append(num)
    list2.append('\n')
    for ele in list2:
        print ele,



class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''
        self.heading = start_heading
        self.maze_dim = maze_dim
        self.map = Map(self.maze_dim)
        self.start = start
        self.location = self.start
        self.goal = [[maze_dim - 1, maze_dim - 1]]
        self.goal_changed = False
        self.finishing = False
        self.finish_count = 4
        self.values = [[99 for row in range(self.maze_dim)] for col in range(self.maze_dim)]
        self.record = []
        self.run = 1
        self.step = 0
        self.score = 0

    def reset(self):
        '''
         reset robot's position to the initial state
        '''
        self.heading = start_heading
        self.location = [0, 0]
        self.record = []
        self.socre = 0



    def to_rotation(self, direction):
        '''
        transfer direction into rotation angles
        return -1 if dir is in behind
        '''
        dirs = dir_sensors[self.heading]

        rotations = [-90, 0, 90]
        if direction in dirs:
            return rotations[dirs.index(direction)]
        else:
            return -1

    def get_status(self):
        '''
        print out the robot's current position and heading
        '''
        print 'status is: '
        print self.location, self.heading
    
    def get_score(self):
        print 'score is: ' + str(self.score)

    ##########################
    # map and maze
    #########################

    def get_map(self):
        '''
        print out map
        '''
        self.map.get_map()

    def update_goal(self):
        '''
        Find 2 x 2 squres in the middle area of the maze, then return the four corners' position
        of that square

        Although we dont know the goal position exactly, but we have an idea 
        that it should be in the center of the maze, and we know what it should be look like.
        So we start with a rough guess of the position, and then as we update map when we moves, 
        the goal position will become clear.
        '''
        search = self.maze_dim / 2 - 2
        for i in range(3):
            search_i = search + i
            for j in range(3):
                search_j = search + j
                if self.map.is_goal([search_i, search_j]):
                    x = search + i
                    y = search + j
                    result = [[x, y], [x + 1, y], [x + 1, y - 1], [x, y - 1]]
                    if x != self.goal[0][0] or y != self.goal[0][1]:
                        self.goal_changed = True
                        self.finish_count = 4
                        self.finishing = False
                    return result



    def update_map(self, sensors):
        '''
        pass through the current location, direction, and distance to Map to update walls
        '''
        changed = False
        dirs = dir_sensors[self.heading]
        for i in range(len(sensors)):
            update = self.map.update_map(self.location, dirs[i], sensors[i])
            if update:
                changed = True
            # print update
        if changed:
            self.goal = self.update_goal()
            self.update_value(self.goal, cost)


        if self.is_reach_goal():
            self.finishing = True




    ###################
    #   execution 
    ##################


    def make_turn(self, degree):
        '''
        make a turn based on given inputs
        '''
        dirs = dir_sensors[self.heading]
        heading = dirs[degree // 90 + 1]
        return heading

    def turn_around(self):
        '''
        turn 180 degrees
        '''
        self.heading = dir_reverse[self.heading]

    def take_step(self, location, heading):
        '''
        robot move one step ahead
        '''
        x = location[0] + dir_move[heading][0]
        y = location[1] + dir_move[heading][1]
        return [x, y]


    def execute(self, rotation, movement):
        '''
        robot take turns and then moves ahead based on given movement

        For moves, the robot take a loop movement times of check movable and then move one step 
        
        For negative movements, the robot turn around first, and then move ahead, and then turn back
        '''
        move_back = False
        if movement < 0:
            move_back = True
        self.heading = self.make_turn(rotation)
        if move_back:
            self.turn_around()
        for i in range(abs(movement)):
            if self.map.is_valid_move(self.location, self.heading):
                #self.map.fill_wall(self.location, self.heading)
                if self.reverse == False:
                    self.record.append(self.heading)
                self.location = self.take_step(self.location, self.heading)
        if move_back:
            self.turn_around()

        # draw the trace of robot


    ######################
    # value table
    ##################

    def get_value_table(self):
        '''
        print out value tables
        '''
        for row in self.values:
            print_list(row)
    
    def write_value(self, location, value):
        '''
        change given position's value table's value to given input
        '''
        x = location[0]
        y = self.maze_dim - location[1] - 1
        self.values[y][x] = value

    def get_value(self, location):
        '''
        return position's value of the given location
        '''
        x = location[0]
        y = self.maze_dim - location[1] - 1
        return self.values[y][x]


    def update_value(self, target, cost):
        '''
        update value map based on the target positions as 0 value, and given cost
        '''
        self.values = [[99 for row in range(self.maze_dim)] for col in range(self.maze_dim)]
        adjs = ['u', 'r', 'd', 'l']
        changed = True
        while changed:            
            changed = False
            for row in range(self.maze_dim):
                for col in range(self.maze_dim):
                    if [row, col] in target:
                        if self.get_value([row, col]) != 0:
                            self.write_value([row, col], 0)
                            changed = True
                    for neighbour in adjs:
                        util = self.get_value([row, col]) + cost
                        location = [row + dir_move[neighbour][0], col + dir_move[neighbour][1]]
                        if 0 <= location[0] < self.maze_dim and 0 <= location[1] < self.maze_dim:
                            if self.map.is_connect(location, [row, col]):
                                # print util, location, self.values[row][col]
                                if self.get_value([location[0], location[1]]) > util:
                                    self.write_value([location[0], location[1]], util)
                                    changed = True



    #################
    # planning and searching
    ##################

    def random_walk(self):
        '''
        return execution input randomly
        '''
        rotation = random.choice([-90, 0, 90])
        movement = random.choice([0, 1, 2, 3])
        return [rotation, movement]

    def test_walk(self):
        '''
        test for debug
        '''
        return [0, 1]




    def finish_moves(self):
        if self.finish_count > 0:
            pos = self.goal.index(self.location)
            self.finish_count -= 1
            x = self.location[0] + dir_move[goal_square_moves[pos]][0]
            y = self.location[1] + dir_move[goal_square_moves[pos]][1]
            return self.find_commond(self.location, [x, y])
        else:
            self.run = 2
            return [0, 0]



    def second_run(self):
        '''
        in second, we only move through the value table, and we need to run as fast as possible
        '''
        location = self.location
        head = self.heading
        move = self.find_next_move(self.location, )
        rotation, movement = self.to_action(move)
        head = self.make_turn(rotation)
        step = self.get_longest_step(location, head)
        self.record.append([rotation, step])
        return rotation, step       



    def is_reach_goal(self):
        '''
        since there are four goal squares, and we need to check if our robot has reached either one of them.
        '''
        if self.location not in self.goal:
            return False
        else:
            if self.goal_changed:
                self.goal_changed = False
            return True



    def solve_path(self):
        '''
        find the shortest path from starting to the goal position
        '''
        path = self.find_path(self.start, self.goal)
        return path

    def find_path(self, start, goal):
        '''
        find path from start location to the target location, base on the value table
        '''
        target = goal[0]
        path = []
        path.append(start)
        x = start[0]
        y = start[1]
        while [x, y] not in goal:
            move = self.find_best_neighbour([x, y], 3)[0]
            for i in range(move[1]):
                x += dir_move[move[0]][0]
                y += dir_move[move[0]][1]
                path.append([x, y])
        return path

    def get_longest_step(self, location, direction, step):
        '''
        find the max step from the given location along the given direction
        return a list [max steps, it's location]
        '''
        util = self.get_value(location)
        for count in range(step):
            location1 = self.take_step(location, direction)
            if 0 <= location1[0] < self.maze_dim and 0 <= location1[1] < self.maze_dim and self.map.is_connect(location, location1):
                util1 = self.get_value(location1)
                if util - cost < util1:
                    return count, location1
                util = util1
                location = location1
            else:
                return count, location
        return step, location


    def find_best_neighbour(self, location, step):
        '''
        find the neighbour in 3 steps in four directions to the given location
        Return a list [action commond to there, its location]
        '''        
        x = location[0]
        y = location[1]
        min_cost = self.get_value([x, y])
        min_move = None
        best = location
        for neighbour in dirs:
            steps, pos = self.get_longest_step(location, neighbour, step)
            if steps > 0:
                if self.get_value(pos) <= min_cost:
                    min_cost = self.get_value(pos)
                    min_move = neighbour, steps
                    best = pos
        return min_move, best

    def find_commond(self, start, target):
        x = target[0] - start[0]
        y = target[1] - start[1]
        moves = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        direction = dirs[moves.index([x, y]) % 4]
        rotation = self.to_rotation(direction)
        if rotation == -1:
            return [0, -1]
        return [rotation, 1]


    def find_next_move(self, location, path):
        '''
        return the best move direction and steps that along the path
        '''
        for i in range(max_step):
            move, pos = self.find_best_neighbour(location, max_step - i)
            if pos in path:
                rotation = self.to_rotation(move[0])
                if rotation == -1:
                    return [rotation, -move[1]]
                return [rotation, move[1]]
        pos = path[path.index(location) + 1]
        return self.find_commond(location, pos)




    def reverse_move(self):
        '''
        robot move backwards along the previous actions
        '''
        self.reverse = True
        previous = self.record.pop()
        count = 1
        for i in range(2):
            if len(self.record) > 0:
                if previous == self.record[-1]:
                    self.record.pop()
                    count += 1
        previous = dir_reverse[previous]
        rotation = self.to_rotation(previous)
        if rotation == -1:
            return [0, -count]
        else:
            return [rotation, count]



    def policy_walk(self):
        '''
        return execution inputs based on two things, one is the value table, and another is the shortest path
        from starting point to that goal position. 

        The path might change after the robot sense new walls, as a result two things will happen.

        IF the robot is on the path, then it will follow it. 
        Or it moves back based on its previous moves to the starting point, until it on the path.
        '''
        self.reverse = False
        path = self.find_path(self.start, self.goal)
        if self.location not in path:
            move = self.reverse_move()
        else:
            if random.random() < beta:
                return self.random_walk()
            move = self.find_next_move(self.location, path)
        
        return move



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
        self.reverse = False
        #print self.location, self.heading

        if self.run == 1:
            self.update_map(sensors)
            if self.finishing:
                # self.get_map()

                rotation, movement = self.finish_moves()
                if [rotation, movement] == [0, 0]:
                    self.run = 2
                    self.reset()
                    return 'Reset', 'Reset'
            else:
                rotation, movement = self.policy_walk()
            if rotation not in [-90, 90]:
                rotation = 0
        else:
            rotation, movement = self.policy_walk()
        self.execute(rotation, movement)
        # print self.record
        # print ' '
        #print self.map.is_goal([4, 4])
        # print self.record
        # print self.find_path(start, self.goal)
        #print self.goal[0]


        self.score += 1
        return rotation, movement





