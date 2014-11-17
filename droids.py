import random
import pygame
from pygame.locals import *

pygame.init()
##clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
cycles = 0
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkblue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
colors = [red, green, blue, darkblue, black, pink]

class Board:
    def __init__(self, width=100, height=100):
        # (0, 0) is in the left top
        self.x_axis = width
        self.y_axis = height
        self.droids = []
        self.dead_droids = []

    def update(self):
        alive_droids = self.get_alive_droids()
        for d in alive_droids:
            d.update()
        self.update_dead_droids()

    def is_tile_walkable(self, droid_x, droid_y):
        if not self.check_coordinates(droid_x, droid_y):
            return False
        for d in self.droids:
            if d.x == droid_x and d.y == droid_y:
                return False
        return True
    
    def add_droid(self, droid):
        if self.is_tile_walkable(droid.x, droid.y):
            self.droids.append(droid)
            return True
        else:
            return False
    
    def get_droids(self):
        return self.droids

    def get_droids_num(self):
        return len(self.droids)

    def get_alive_droids_num(self):
        return len(self.get_alive_droids())

##    staticmethod
    def get_droids_in_range(self, droid):
        droids = self.get_droids()
        other_droids = list(set(droids) - set([droid]))
        droids_in_range = []
        for i in other_droids:
            distance = self.get_distance_two_droids(droid, i)
            if distance <= droid.range:
                droids_in_range.append(i)
        return droids_in_range

    def get_closet_droid_in_range(self, droid):
        droids_in_range = self.get_droids_in_range(droid)
        if not droids_in_range:
            return []
        closet_droid = min(droids_in_range,
                           key=lambda \
                           p: self.get_distance_two_droids(droid, p))
        return closet_droid

    def get_weeker_droid_in_range(self, droid):
        droids_in_range = self.get_droids_in_range(droid)
        if not droids_in_range:
            return []
        weeker_droid = min(droids_in_range,
                           key=lambda \
                           p: p.health)
        return weeker_droid

    def is_other_weeker(self, my_droid, other_droid):
        if my_droid.health > other_droid.health:
            return True
        else:
            return False

    def is_me_better(self, my_droid, other_droid):
        if my_droid.damage > other_droid.damage:
            return True
        else:
            return False

    def get_distance_two_droids(self, my_droid, other_droid):
        distance = pow( pow(my_droid.x - other_droid.x, 2) + \
                        pow(my_droid.y - other_droid.y, 2) , 0.5)
        return distance

    def attack_another_droid(self, my_droid, other_droid):
        # with probability
        pass

    def attack_another_droid_accurate(self, my_droid, other_droid):
        distance = self.get_distance_two_droids(my_droid, other_droid)
        if other_droid.alive and distance <= my_droid.range:
            my_droid.attacking = True
            other_droid.health = \
                            round(other_droid.health - my_droid.damage, 2)
            if (not other_droid.last_attacker is my_droid) \
               or other_droid.attacked_timing==0:
                other_droid.last_attacker = my_droid
                other_droid.attacked_timing = 100
                self.get_run_away_direction(other_droid)
        else:
            my_droid.attacking = False

    def get_run_away_direction(self, my_droid):
        if my_droid.last_attacker:
            attacker = my_droid.last_attacker
            delta_x = attacker.x - my_droid.x
            delta_y = attacker.y - my_droid.y
            my_droid.x_run = my_droid.x - delta_x
            my_droid.y_run = my_droid.y - delta_y
            my_droid.x_run, my_droid.y_run = \
                self.assert_coordinates(my_droid.x_run, my_droid.y_run)

    def assert_coordinates(self, x, y):
        if x <= 0:
            x = 1
        if x >= self.x_axis:
            x = self.x_axis - 5
        if y <= 0:
            y = 1
        if y >= self.y_axis:
            y = self.y_axis - 5
        return x,y
            
##    @staticmethod
    def update_dead_droids(self):
        for d in self.get_droids():
            if not d.alive:
                if not d in self.dead_droids:
                    self.dead_droids.append(d)

    def get_dead_droids(self):
        return self.dead_droids

    def get_alive_droids(self):
        return list(set(self.get_droids())-set(self.get_dead_droids()))
                
    def print_droids(self):
        for d in self.get_droids():
            print d.name, ':', d.get_coordinates()

    def print_alive_droids(self):
        for d in self.get_alive_droids():
            print d.name, ':', d.get_coordinates()            

##    @staticmethod
    def check_coordinates(self, x, y):
        if x > 0 and x < self.x_axis:
            if y > 0 and y < self.y_axis:
                return True
        return False

class Droid:
    moves = [( 0, -1, 'U', 'D'),    # go up
             ( 0, 1 , 'D', 'U'),    # go down
             (-1, 0 , 'L', 'R'),    # go left
             ( 1, 0 , 'R', 'L'),    # go right
             (-1, -1, 'UL', 'DR'),  # go up left
             ( 1, -1, 'UR', 'DL'),  # go up right
             (-1, 1 , 'DL', 'UR'),  # go down left
             ( 1, 1 , 'DR', 'UL')]  # go down right
    
    def __init__(self, name, x=0, y=0, step=2,
                 health=100, damage=0.25, range=75):
        self.name = name
        self.x = x
        self.y = y
        self.step = step
        self.health = health
        self.damage = damage
        self.range = range
        self.last_move = ''
        self.x_goal = x
        self.y_goal = y
        self.go_to_goal_flag = False
        self.run = True
        self.alive = True
        self.attacking = False
        self.color = (0,0,0)    ##black
        self.last_attacker = None
        self.attacked_timing = 0
        self.x_run = x
        self.y_run = y
    
    def update(self):
        if self.health <= 0:
            self.alive = False
        if not self.alive:
            self.color = (255,255,255)    ##white
        self.attacking = False
        if self.attacked_timing > 0:
            self.attacked_timing -= 1
        
    def wander_to_direction(self, board):
        if self.attacked_timing > 0:
            self.step_to_direction(board, self.x_run, self.y_run)
        else:
            if not self.go_to_goal_flag:
                while True:
                    new_x = random.randint(0, board.x_axis - 1)
                    new_y = random.randint(0, board.y_axis - 1)
                    if board.is_tile_walkable(new_x, new_y):
                        self.x_goal = new_x
                        self.y_goal = new_y
                        self.go_to_goal_flag = True
                        break
            else:
                self.step_to_direction(board, self.x_goal, self.y_goal)

    def step_to_direction(self, board, x_goal, y_goal):
        if self.go_to_goal_flag:
            if x_goal == self.x and y_goal == self.y:
                self.go_to_goal_flag = False
                return None
            if abs(x_goal-self.x)>20 or abs(y_goal-self.y)>20:
                self.run = True
            else:
                self.run = False
            valid_move = self.get_move_from_direction(x_goal, y_goal)
            while True:
                move = random.choice(valid_move)
                if self.make_move(board, move):
                    break
            
##    @staticmethod
    def get_move_from_direction(self, x_goal, y_goal):
        if x_goal - self.x > 0 :       # +ve >> goal is right
            x_direction = 1
        elif x_goal - self.x < 0 :     # -ve >> goal is left
            x_direction = -1
        else:
            x_direction = 0
        
        if y_goal - self.y > 0 :       # +ve >> goal is down
            y_direction = 1
        elif y_goal - self.y < 0 :     # -ve >> goal is up
            y_direction = -1
        else:
            y_direction = 0

        valid_move = [i for i in self.moves
                      if i[0]==x_direction and i[1]==y_direction]
        if not valid_move:
            valid_move = [i for i in self.moves
                          if i[0]==x_direction or i[1]==y_direction]
        return valid_move
    
    def wander(self, board):
        self.go_to_goal_flag = False
        while True:
            move = random.choice(self.moves)
            if self.last_move is move[3]:
                continue
            if self.make_move(board, move):
                break

##    @staticmethod
    def make_move(self, board, move):
        if self.run:
            if self.attacked_timing > 0:
                step = 5
            else:
                step = self.step
        else:
            step = 1
        new_x = self.x + step * move[0]
        new_y = self.y + step * move[1]
        if board.is_tile_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.last_move = move[2]
            return True

    def print_droid(self):
        print 'name:', self.name
        print 'position:', (self.x, self.y)
        print 'step:', self.step
        print 'health:', self.health
        print 'damage power:', self.damage
        print 'range:', self.range
        if self.go_to_goal_flag:
            print 'goal:', (self.x_goal, self.y_goal)

    def get_coordinates(self):
        return (self.x, self.y)

    def get_distance_to(self, x, y):
        distance = pow( pow(self.x-x, 2) + pow(self.y-y, 2) , 0.5)
        return distance

    def give_color(self, color):
        self.color = color

def initialize_game(board, n):
    w = board.x_axis
    h = board.y_axis
    for i in range(n):
        x = random.choice(range(0,w))
        y = random.choice(range(0,h))
        d = Droid('d'+str(i), x, y)
        board.add_droid(d)
    
def wander_all_droids(board):
    for d in board.get_droids():
        d.wander(board)

board = Board(640, 480)
initialize_game(board, 6)

droids = board.get_alive_droids()
for i in range(len(droids)):
    d = droids[i]
    color = colors[i]
    d.give_color(color)
screen = pygame.display.set_mode((850, 500), 0, 24)
while True:
    quit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit();
             quit = True
    if quit:
        break
    screen.fill(white)
    text_height = 25
    for i in range(len(droids)):
        d = droids[i]
        board.update()
        text = font.render('%s : %f' % (d.name, d.health), True, black)
        screen.blit(text, (650, text_height))
        text_height += 25
        if d.alive: #and (i == 0):
            d_close = board.get_closet_droid_in_range(d)
            if d_close:
                if d_close.alive and i==0:
                    board.attack_another_droid_accurate(d, d_close)
                else:
                    d.wander_to_direction(board)
            else:
                d.wander_to_direction(board)
        if d.attacking:
            radius = 6
            pygame.draw.lines(screen, d.color, False,
                              [(d.x,d.y), (d_close.x,d_close.y)], 1)
        else:
            radius = 3
        pygame.draw.circle(screen, d.color, (d.x, d.y), radius, 0)
    pygame.display.update()

'''
d = board.get_droids()[0]

print 'our droid coordinates:', d.get_coordinates(); print
d_range = board.get_droids_in_range(d)
if d_range:
    print 'droids in range:'
for i in d_range:
    print i.get_coordinates(), '\t with distance:', \
          board.get_distance_two_droids(d, i)
d_close = board.get_closet_droid_in_range(d)
if d_close:
    print
    print 'closet droid coordinates:', d_close.get_coordinates()

d_range = board.get_droids_in_range(d)
if d_range:
##    d_range[-1].health = 90
    print 'droids in range health:'
for i in d_range:
    print i.health
d_weeker = board.get_weeker_droid_in_range(d)
if d_weeker:
    print
    print 'weeker droid:', d_weeker.name, \
        '\t with health:', d_weeker.health
'''
