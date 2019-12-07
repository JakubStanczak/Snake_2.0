import pygame

pygame.init()

snake_start_len = 5

class Marker:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.num = None
        self.color = (0, 0, 0)
        self.prev_dir = ["x", +1]

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x * Snake.dim, self.y * Snake.dim, Snake.dim, Snake.dim), 1)

    def __repr__(self):
        return "{} {}".format(self.x, self.y)

class Snake:
    dim = 20
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.apple_inside = False

    def draw(self):
        if self.apple_inside:
            color = (160, 245, 60)
        else:
            color = (0, 255, 0)
        pygame.draw.rect(win, color, (self.x * self.dim, self.y * self.dim, self.dim, self.dim))

    def __repr__(self):
        return "{} {}".format(self.x, self.y)

board_width = 25
board_height = 15

screen_width = board_width * Snake.dim
screen_height = board_height * Snake.dim
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake by Kuba")

markers = []
snake = []
def board_init():
    for x in range(board_width):
        temp = []
        for y in range(board_height):
            temp.append(Marker(x, y))
        markers.append(temp)

    for i in range(snake_start_len):
        snake.append(Snake(board_width//2 - i, board_height // 2))


def draw():
    win.fill((255, 255, 255))
    for line in markers:
        for marker in line:
            marker.draw()
    for s in snake:
        s.draw()

    pygame.display.update()


def if_collision():
    if vars(snake[0])[snake_dir[0]] + snake_dir[1] > board_width or vars(snake[0])[snake_dir[0]] + snake_dir[1] < 0:
        print("zjebales")

def move(): #  TODO make this work
    # snake[0].direction = snake_dir
    vars(snake[0])[snake_dir[0]] += snake_dir[1]
    snake[0].prev_dir = snake_dir
    for i in range(1, len(snake)):
        vars(snake[i])[snake[i-1].prev_dir[0]] += snake[i-1].prev_dir[1]
        snake[i-2].prev_dir = snake[i-1].prev_dir

board_init()
snake_dir = ["y", +1]
run = True
while run:
    pygame.time.delay(300)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if_collision()
    move()
    # GAME
    # chose direction
    # check if collision
    # move
    draw()
