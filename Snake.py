import pygame
import random
pygame.init()

snake_start_len = 5
marker_font = pygame.font.SysFont("calibri", 10, bold=True)

class Marker:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.num = None
        self.color = (0, 0, 0)

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x * Snake.dim, self.y * Snake.dim, Snake.dim, Snake.dim), 1)
        rendered_num = marker_font.render(str(self.num), True, self.color)
        win.blit(rendered_num, (self.x * Snake.dim + Snake.dim // 2, self.y * Snake.dim + Snake.dim // 2))


    def __repr__(self):
        return "{} {} number {}".format(self.x, self.y, self.num)

class Snake:
    dim = 30
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.apple_inside = False
        self.prev_dir = ["x", +1]

    def draw(self):
        if not alive:
            color = (255, 0, 0)
        elif self.apple_inside:
            color = (160, 245, 60)
        else:
            color = (0, 255, 0)
        pygame.draw.rect(win, color, (self.x * self.dim, self.y * self.dim, self.dim, self.dim))

    def __repr__(self):
        return "{} {}".format(self.x, self.y)

class Apple:
    dim = 7

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (250, 200, 0)

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x * Snake.dim + Snake.dim // 2, self.y * Snake.dim + Snake.dim // 2), self.dim)


board_width = 30
board_height = 25

screen_width = board_width * Snake.dim
screen_height = board_height * Snake.dim
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake by Kuba")

markers = []
snake = []
apples = []
def board_init():
    for x in range(board_width):
        temp = []
        for y in range(board_height):
            temp.append(Marker(x, y))
        markers.append(temp)

    for i in range(snake_start_len):
        snake.append(Snake(board_width//2 - i, board_height // 2))
    new_apple()

    i = 1
    for x in range(board_width):
        ys = range(1, board_height)
        if x % 2 == 1:
            ys = reversed(ys)
        for y in ys:
            markers[x][y].num = i
            i += 1
    for x in range(1, board_width):
        markers[-x][0].num = i
        i += 1
    markers[0][0].num = 0


def new_apple():
    good_choice = False
    while not good_choice:
        good_choice = True
        x = random.randint(0, board_width - 1)
        y = random.randint(0, board_height - 1)
        for s in snake:
            if s.x == x and s.y == y:
                good_choice = False
    apples.append(Apple(x, y))


def draw():
    win.fill((255, 255, 255))
    for line in markers:
        for marker in line:
            marker.draw()
    for s in snake:
        s.draw()
    for apple in apples:
        apple.draw()

    pygame.display.update()


def if_collision():
    board_dim = {"x": board_width, "y": board_height}
    if vars(snake[0])[snake_dir[0]] + snake_dir[1] >= board_dim[snake_dir[0]] or vars(snake[0])[snake_dir[0]] + snake_dir[1] <= 0:
        return True
    for s in snake:
        if vars(snake[0])[snake_dir[0]] + snake_dir[1] == vars(s)[snake_dir[0]] and vars(snake[0])[other_dir[snake_dir[0]]] == vars(s)[other_dir[snake_dir[0]]]:
            return True


def if_ate_apple():
    for apple in apples:
        if apple.x == snake[0].x and apple.y == snake[0].y:
            apples.pop(apples.index(apple))
            snake[0].apple_inside = True
            new_apple()
            break


def move():
    vars(snake[0])[snake_dir[0]] += snake_dir[1]
    for i in range(1, len(snake)):
        vars(snake[i])[snake[i-1].prev_dir[0]] += snake[i-1].prev_dir[1]

    #  extending snake if apple reached its end
    if snake[-1].apple_inside:
        snake[-1].apple_inside = False
        snake.append(Snake(snake[-1].x, snake[-1].y))
        vars(snake[-1])[snake[-3].prev_dir[0]] -= snake[-3].prev_dir[1]

    #  updating in reverse: previous direction and apple inside
    for i in reversed(range(1, len(snake))):
        snake[i].prev_dir = snake[i-1].prev_dir
        if snake[i - 1].apple_inside:
            snake[i].apple_inside = True
            snake[i - 1].apple_inside = False
    snake[0].prev_dir = snake_dir


def change_dir(new_dir):
    print(new_dir)
    global next_dir
    if new_dir[0] == snake_dir[0] and new_dir[1] == snake_dir[1] * - 1:
        return False
    else:
        next_dir = new_dir
        return True

def pick_dir():
    adj_markers = adjacent_markers(snake[0].x, snake[0].y)
    apple_num = markers[apples[0].x][apples[0].y].num
    picked_marker = adj_markers[-1]

    picked_dir = []
    if snake[0].x - picked_marker.x == 0:
        picked_dir.append("y")
    else:
        picked_dir.append("x")
    if picked_marker.x - snake[0].x < 0 or picked_marker.y - snake[0].y < 0:
        picked_dir.append(-1)
    else:
        picked_dir.append(1)
    print(adj_markers)
    print(picked_dir)
    return picked_dir


def adjacent_markers(x, y):
    adjacent_markers = []
    for column in markers:
        for marker in column:
            if abs(x - marker.x) <= 1 and abs(y - marker.y) <= 1:
                if (x - marker.x == 0 or y - marker.y == 0) and not (x == marker.x and y == marker.y):
                    adjacent_markers.append(marker)
    return adjacent_markers

board_init()
snake_dir = ["x", +1]
next_dir = ["x", +1]
other_dir = {"x": "y", "y": "x"}
run = True
alive = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_dir(["x", -1])
            elif event.key == pygame.K_RIGHT:
                change_dir(["x", +1])
            elif event.key == pygame.K_UP:
                change_dir(["y", -1])
            elif event.key == pygame.K_DOWN:
                change_dir(["y", +1])

    pygame.time.delay(200)
    if alive:

        snake_dir = pick_dir()
        if if_collision():
            alive = False
        move()
        if_ate_apple()


    # GAME
    # chose direction
    # check if collision
    # check if ate apple
    # move
    draw()
