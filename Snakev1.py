
import pygame
import sys
import random


SCREEN_TITLE = "SnakeQueen"
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960
GRID_SCREEN = 40
GRID_WIDTH = SCREEN_WIDTH / GRID_SCREEN
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SCREEN

UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1,0)
RIGHT = (1,0)

def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x*GRID_SCREEN,y*GRID_SCREEN),(GRID_SCREEN,GRID_SCREEN))
                pygame.draw.rect(surface,(93,216,228),r)
            else:
                rr = pygame.Rect((x*GRID_SCREEN,y*GRID_SCREEN), (GRID_SCREEN,GRID_SCREEN))
                pygame.draw.rect(surface, (84,194,205), rr)



class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP,DOWN,LEFT,RIGHT])
        self.color = (17,24,47)

    def getHeadPosition(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.getHeadPosition()
        x, y = self.direction
        new = (((cur[0] + (x*GRID_SCREEN)) % SCREEN_WIDTH), (cur[1] + (y*GRID_SCREEN)) %SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()
                
    def reset(self):
        self.lenght = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP,DOWN,LEFT,RIGHT])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SCREEN, GRID_SCREEN))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (92,216,228), r, 1)

    def handleKeys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                    


class Food(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (223, 163, 49)
        self.randomizePosition()

    def randomizePosition(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRID_SCREEN, random.randint(0, GRID_HEIGHT -1) * GRID_SCREEN)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]),(GRID_SCREEN, GRID_SCREEN))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93,216,228), r, 1)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)

surface = pygame.image.load('background.jpg')
surface = pygame.transform.scale(surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
drawGrid(surface)

snake = Snake()
food = Food()

score = 0
while(True):
    clock.tick(10)
    snake.handleKeys()
    drawGrid(surface)
    snake.move()
    if snake.getHeadPosition() == food.position:
        snake.length += 1
        score += 1
        food.randomizePosition()
    snake.draw(surface)
    food.draw(surface)
    screen.blit(surface,(0,0))
    pygame.display.update()
      

