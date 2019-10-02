#!/usr/bin/env python
# coding: utf-8

# from __future__ import print_function
from simpleai.search import SearchProblem, astar, depth_first, breadth_first
import math
import pygame as pg
import random as r



COSTS = {
        "up": 1.0,
        "down": 1.0,
        "left": 1.0,
        "right": 1.0
}


class SnakeGame(SearchProblem):

        def __init__(self, initial, goal):
                self.initial = initial
                self.goal = goal
                
                super(SnakeGame, self).__init__(initial_state=self.initial)

        def actions(self, state):
                actions = []
                for action in list(COSTS.keys()):
                        newx, newy = self.result(state, action)
                        if (newx >= 0) and (newx < 320) and (newy >= 0) and (newy < 320):
                                actions.append(action)
                return actions

        def result(self, state, action):
                x, y = state
                if action == "up":
                        y -= 16
                if action == ("down"):
                        y += 16
                if action == ("left"):
                        x -= 16
                if action == ("right"):
                        x += 16

                new_state = (x, y)
                return new_state

        def is_goal(self, state):
                return state == self.goal

        def cost(self, state, action, state2):
                return COSTS[action]

        def heuristic(self, state):
                x, y = state
                gx, gy = self.goal
                return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)



def moveSnake(direction, snake):
    snakeX = snake[0].rect.x
    snakeY = snake[0].rect.y
    if direction == 1:
        snakeX+=16
    if direction == 2:
        snakeY+=16
    if direction == 3:
        snakeX-=16
    if direction == 4:
        snakeY-=16
    
    tail = snake.pop()
    tail.rect.x = snakeX
    tail.rect.y = snakeY
    snake = [tail] + snake
    return snake


def insertHead(direction, snakeList):
    snakeX = snakeList[0].rect.x
    snakeY = snakeList[0].rect.y
    if direction == 1:
        snakeX+=16
    if direction == 2:
        snakeY+=16
    if direction == 3:
        snakeX-=16
    if direction == 4:
        snakeY-=16

    s =  snake()
    s.rect.x = snakeX
    s.rect.y = snakeY
    Snake.add(s)
    snakeList = [s] + snakeList
    return snakeList

def checkCollision(snakeList):
    cabezaX = snakeList[0].rect.x
    cabezaY = snakeList[0].rect.y
    for i in snakeList[1:]:
        if cabezaX == i.rect.x and cabezaY == i.rect.y:
            print("nonas")
            return True



def generateSnake():
    length = 3
    for i in range(length,-1,-1):
        snakeList.append({"x":i*16, "y": 32})
    return snakeList


# def main():
#         problem = GameWalkPuzzle(MAP)
#         print(problem.initial)
#         #result = astar(problem, graph_search=True)
#         result = depth_first(problem, graph_search=True)
#         print(result.path())
#         path = [x[1] for x in result.path()]
#         # print(path)
#         for y in range(len(MAP)):
#                 for x in range(len(MAP[y])):
#                         if (x, y) == problem.initial:
#                                 print("o", end='')
#                         elif (x, y) == problem.goal:
#                                 print("x", end='')
#                         elif (x, y) in path:
#                                 print("·", end='')
#                         else:
#                                 print(MAP[y][x], end='')
#                 print()


VIWEPORT_SIZE = (320, 320)

snakeList = []

def createProblem(listaSnake):
    problem = SnakeGame((listaSnake[0].rect.x, listaSnake[0].rect.y), (food.rect.x, food.rect.y))
    result = depth_first(problem, graph_search=True)
    path = [x[1] for x in result.path()]
    moves = result.path()
    moves = moves[1:]
    lm = []

    for i in moves:
        lm.append(i[0])

    lm.reverse()
    return lm


class snake(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([16,16])
        self.image.fill((10,20,30))
        self.rect = self.image.get_rect()
        # self.snakeList = []
        self.rect.x = 0
        self.rect.y = 0
        self.direction = 1


class Food(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([16,16])
        self.image.fill([255,0,255])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
    def generateFood(self):
        print("me genere")
        self.rect.x = r.randrange(0,320,16)
        self.rect.y = r.randrange(0,320,16)

        return [self.rect.x, self.rect.y]


if __name__ == "__main__":

    listaSnake = []
    generateSnake()
    food = Food()
    listFood = food.generateFood()
    pg.init()
    pantalla = pg.display.set_mode(VIWEPORT_SIZE)
    Snake = pg.sprite.Group()
    for i in snakeList:
        s =  snake()
        s.rect.x = i["x"]
        s.rect.y = i["y"]
        Snake.add(s)
        listaSnake.append(s)
    
    # print((listaSnake[0].rect.x,listaSnake[0].rect.y))
    
    Food = pg.sprite.Group()
    food.rect.x = listFood[0]
    food.rect.y = listFood[1]
    Food.add(food)
    reloj = pg.time.Clock()
    fin = False
    direction = 1

    lm = createProblem(listaSnake)
    
    while not fin:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fin = True
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_DOWN and direction != 4:
            #             direction = 2
            #     if event.key == pg.K_UP and direction != 2:
            #             direction = 4
            #     if event.key == pg.K_RIGHT and direction != 3:
            #             direction = 1
            #     if event.key == pg.K_LEFT and direction != 1:
            #             direction = 3

        if lm != []:

            mov = lm.pop()
            
            if mov == 'up':
                direction = 4
            if mov == 'down':
                direction = 2
            if mov == 'right':
                direction = 1
            if mov == 'left':
                direction = 3
                        
        hit = pg.sprite.spritecollide(listaSnake[0], Food, True)

        if hit:
            listaFood = food.generateFood()
            food.rect.x = listaFood[0]
            food.rect.y = listaFood[1]
            Food.add(food)
            listaSnake = insertHead(direction, listaSnake)
            print("hittie")
            lm = createProblem(listaSnake)

        else:
            listaSnake = moveSnake(direction, listaSnake)
        
        # collision = checkCollision(listaSnake)
        # if collision or listaSnake[0].rect.x < 0 or listaSnake[0].rect.x > 640 or listaSnake[0].rect.y < 0 or listaSnake[0].rect.y > 400:
        #     fin = True

        pantalla.fill((255,255,255))
        Snake.draw(pantalla)
        Food.draw(pantalla)
        pg.display.flip()
        reloj.tick(32)

        





# if __name__ == "__main__":
#         main()