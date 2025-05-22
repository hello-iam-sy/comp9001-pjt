import pygame
import sys

# init
pygame.init()
pygame.font.init()

# screen setup
width, height = 800, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pikachu Volleyball")

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS
clock = pygame.time.Clock()

# background setup
background = pygame.image.load('background.png').convert_alpha()
background = pygame.transform.scale(background, (width, height))
background.set_alpha(255)

# net setup
net_x = width // 2
net_width = 10
net_height = 200
net_top = height - net_height

# game flag
paused = False
loser = None

# show message function
def show_message(text):
    font_main = pygame.font.SysFont(None, 60)
    font_sub = pygame.font.SysFont(None, 30)

    main_msg = font_main.render(text, True, BLACK)
    sub_msg = font_sub.render("Press SPACE to play again", True, BLACK)

    main_rect = main_msg.get_rect(center=(width // 2, height // 2 - 20))
    sub_rect = sub_msg.get_rect(center=(width // 2, height // 2 + 30))

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, BLACK, (net_x - net_width//2, net_top, net_width, net_height))
    pikachu1.draw()
    pikachu2.draw()
    screen.blit(main_msg, main_rect)
    screen.blit(sub_msg, sub_rect)
    pygame.display.update()

# pikachu class
class Pikachu:
    def __init__(self, x, y, flip=False):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 135
        self.velocity = 5
        self.jump = False
        self.jump_speed = 10
        self.gravity = 0.5
        self.y_speed = 0
        self.image = pygame.image.load('pika.png')
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, keys, left_key, right_key, jump_key, left_limit, right_limit):
        if keys[left_key]:
            self.x -= self.velocity
        if keys[right_key]:
            self.x += self.velocity
        if not self.jump and keys[jump_key]:
            self.jump = True
            self.y_speed = -self.jump_speed

        if self.x < left_limit:
            self.x = left_limit
        if self.x > right_limit - self.width:
            self.x = right_limit - self.width

    def update(self):
        if self.jump:
            self.y += self.y_speed
            self.y_speed += self.gravity
            if self.y >= height - self.height:
                self.y = height - self.height
                self.jump = False

# ball class
class Ball:
    def __init__(self):
        self.x = width // 2
        self.y = height // 4  # 더 높이 시작
        self.radius = 40
        self.x_speed = 4
        self.y_speed = 0
        self.gravity = 0.3
        self.image = pygame.image.load('jiu.png')
        self.image = pygame.transform.smoothscale(self.image, (self.radius * 2, self.radius * 2))

    def draw(self):
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.y_speed += self.gravity

        if self.x - self.radius <= 0:
            self.x = self.radius
            self.x_speed = abs(self.x_speed)
        if self.x + self.radius >= width:
            self.x = width - self.radius
            self.x_speed = -abs(self.x_speed)
        if self.y + self.radius >= height:
            self.y = height - self.radius
            self.y_speed = -abs(self.y_speed) * 0.7
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.y_speed = abs(self.y_speed)

    def check_collision(self, pikachu):
        margin = 10
        if (self.x + self.radius > pikachu.x + margin and
            self.x - self.radius < pikachu.x + pikachu.width - margin and
            self.y + self.radius > pikachu.y + margin and
            self.y - self.radius < pikachu.y + pikachu.height - margin):
            self.y_speed = -10
            if self.x < pikachu.x + pikachu.width // 2:
                self.x_speed = -abs(self.x_speed)
            else:
                self.x_speed = abs(self.x_speed)

    def check_net_collision(self):
        if (net_x - net_width//2 < self.x < net_x + net_width//2 and
            net_top < self.y + self.radius and self.y - self.radius < height):
            if self.x_speed > 0:
                self.x = net_x - net_width//2 - self.radius
                self.x_speed = -abs(self.x_speed)
            else:
                self.x = net_x + net_width//2 + self.radius
                self.x_speed = abs(self.x_speed)
            self.y_speed = -abs(self.y_speed) * 0.7

# pikachu object
pikachu1 = Pikachu(100, height - 135, flip=True)
pikachu2 = Pikachu(650, height - 135, flip=False)
ball = Ball()

# start game
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if paused and event.key == pygame.K_SPACE:
                paused = False
                loser = None
                ball = Ball()
                pikachu1 = Pikachu(100, height - 135, flip=True)
                pikachu2 = Pikachu(650, height - 135, flip=False)

    if paused:
        show_message("Player 1 loses!" if loser == 1 else "Player 2 loses!")
        continue

    keys = pygame.key.get_pressed()
    pikachu1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w, 0, width // 2)
    pikachu2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, width // 2, width)

    pikachu1.update()
    pikachu2.update()
    ball.update()

    ball.check_collision(pikachu1)
    ball.check_collision(pikachu2)
    ball.check_net_collision()

    if ball.y + ball.radius >= height:
        if ball.x < width // 2:
            loser = 1
        else:
            loser = 2
        paused = True
        continue

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, BLACK, (net_x - net_width//2, net_top, net_width, net_height))
    pikachu1.draw()
    pikachu2.draw()
    ball.draw()
    pygame.display.update()

pygame.quit()
sys.exit()
