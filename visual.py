'''
This class is for visualize the robot's movement inside maze.


'''

import turtle


# Setting up parameters

sq_size = 20

turtle_size = [2, 2, 2]

width_wall = 2
width_trace = sq_size / 2
width_path = sq_size / 4
width_goal = sq_size
width_background = 0

color_wall = 'black'
color_trace_round1 = 'green'
color_trace_round2 = 'red'
color_goal = 'yellow'
color_path = 'blue'
color_background = '#F2F2F2'

speed_wall = 0
speed_trace = 2
speed_goal = 0
speed_path = 4
speed_background = 0

class Visual(object):
    def __init__(self, dim_size):
        # set up the windows and background
        self.window = turtle.Screen()
        self.window.setworldcoordinates(-50, -50, sq_size * (dim_size + 2), sq_size * (dim_size + 2))
        self.draw_background(dim_size)

        # set up numbers of turtles that we will need.
        self.pen_wall = turtle.Turtle()
        self.pen_wall.hideturtle()
        self.pen_wall.speed(speed_wall)
        self.pen_wall.color(color_wall)
        self.pen_wall.width(width_wall)

        self.pen_path = turtle.Turtle()
        self.pen_path.color(color_path)
        self.pen_path.hideturtle()
        self.pen_path.speed(speed_path)
        self.pen_path.width(width_path)

        self.pen_trace2 = turtle.Turtle()
        self.pen_trace2.left(90)
        self.pen_trace2.speed(speed_trace)
        self.pen_trace2.width(width_goal)
        self.pen_trace2.color(color_trace_round2)
        self.pen_trace2.turtlesize(turtle_size[0], turtle_size[1], turtle_size[2])

        self.pen_trace1 = turtle.Turtle()
        self.pen_trace1.left(90)
        self.pen_trace1.speed(speed_trace)
        self.pen_trace1.width(width_trace)
        self.pen_trace1.color(color_trace_round1)
        self.pen_trace1.turtlesize(turtle_size[0], turtle_size[1], turtle_size[2])

        self.pen_goal = turtle.Turtle()
        self.pen_goal.color(color_goal)
        self.pen_goal.hideturtle()
        self.pen_goal.width(width_goal)        

    def draw_background(self, dim_size):
        '''
        drawing the background girds of maze
        '''
        pen_bg = turtle.Turtle()
        pen_bg.hideturtle()
        pen_bg.speed(speed_background)
        pen_bg.width(width_background)
        pen_bg.color(color_background)
        left_right = [90, -90]
        for j in range(2):
            pen_bg.pu()
            pen_bg.home()
            pen_bg.goto(-sq_size / 2, -sq_size / 2)
            pen_bg.pd()
            turn = 90
            pen_bg.left(turn * j)
            turn = left_right[j]
            for i in range(dim_size):
                pen_bg.forward(sq_size * dim_size)
                pen_bg.left(turn)
                pen_bg.forward(sq_size)
                pen_bg.left(turn)
                turn *= -1
            pen_bg.forward(sq_size * dim_size)



    def draw_wall(self, dist):
        '''
         draw wall by given distnace
        '''
        angle_walls = [90, 180, 360, 180]
        # move to the given distance
        self.pen_wall.pu()
        self.pen_wall.fd(dist * sq_size + sq_size / 2)
        # draw wall
        self.pen_wall.pd()
        for angle in angle_walls:
            self.pen_wall.left(angle)
            self.pen_wall.fd(sq_size / 2)
        self.pen_wall.pu()
        # move back to robot state
        self.pen_wall.left(90)
        self.pen_wall.fd(dist * sq_size + sq_size / 2)
        self.pen_wall.left(180)


    def draw_trace(self, angle, step, round):
        '''
        draw traces of the robot's movement based on the moving command given
        '''
        if round == 1:
            self.pen_trace1.right(angle)
            self.pen_trace1.fd(sq_size * step)
        else:
            self.pen_trace2.right(angle)
            self.pen_trace2.fd(sq_size * step)

    def draw_walls(self, detections):
        '''
        draw walls by the given sensor detections
        '''

        # move pen_wall to robot state
        pos = self.pen_trace1.pos()
        head = self.pen_trace1.heading()
        self.pen_wall.pu()
        self.pen_wall.goto(pos)
        self.pen_wall.seth(head)

        # draw walls
        self.pen_wall.left(90)
        self.draw_wall(detections[0])
        self.pen_wall.right(90)
        self.draw_wall(detections[1])
        self.pen_wall.right(90)
        self.draw_wall(detections[2])
        self.pen_wall.left(90)

    def draw_path(self, path):
        '''
        draw the given path
        '''
        self.pen_path.clear()
        self.pen_path.pu()
        self.pen_path.goto(path[0][0] * sq_size, path[0][1] * sq_size)
        self.pen_path.pd()
        for pos in path:
            x = pos[0] * sq_size
            y = pos[1] * sq_size
            self.pen_path.goto(x, y)

    def draw_goal(self, goal):
        '''
        draw the goal on Maze
        '''
        self.pen_goal.clear()
        self.pen_goal.pu()
        self.pen_goal.goto(goal[-1][0] * sq_size, goal[-1][1] * sq_size)
        self.pen_goal.pd()
        for pos in goal:
            x = pos[0] * sq_size
            y = pos[1] * sq_size
            self.pen_goal.goto(x, y)




