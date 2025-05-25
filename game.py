import pygame
import sys

# Initialize Pygame and its font module
pygame.init()
pygame.font.init()

# Set up the game window
width, height = 800, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pikachu Volleyball")

# Define basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the game clock for controlling FPS
clock = pygame.time.Clock()

# Load and scale the background image to fit the screen
background = pygame.image.load('background.png').convert_alpha()
background = pygame.transform.scale(background, (width, height))
background.set_alpha(255)  # Set full opacity

# Define the net's position and size
net_x = width // 2
net_width = 10
net_height = 200
net_top = height - net_height

# Game state flags
paused = False  # Whether the game is paused
loser = None    # Indicates which player lost

# Display a message in the center of the screen (e.g., when a player loses)
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

# Pikachu player class for handling movement, jumping, and rendering
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

    # Draw the Pikachu on the screen
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    # Handle player input for movement and jumping
    def move(self, keys, left_key, right_key, jump_key, left_limit, right_limit):
        if keys[left_key]:
            self.x -= self.velocity
        if keys[right_key]:
            self.x += self.velocity
        if not self.jump and keys[jump_key]:
            self.jump = True
            self.y_speed = -self.jump_speed

        # Prevent moving out of the allowed bounds
        if self.x < left_limit:
            self.x = left_limit
        if self.x > right_limit - self.width:
            self.x = right_limit - self.width

    # Apply gravity and update jumping state
    def update(self):
        if self.jump:
            self.y += self.y_speed
            self.y_speed += self.gravity
            if self.y >= height - self.height:
                self.y = height - self.height
                self.jump = False

# Ball class handles physics, collisions, and rendering
class Ball:
    def __init__(self):
        self.x = width // 2
        self.y = height // 4  # Start higher
        self.radius = 40
        self.x_speed = 4
        self.y_speed = 0
        self.gravity = 0.3
        self.image = pygame.image.load('jiu.png')
        self.image = pygame.transform.smoothscale(self.image, (self.radius * 2, self.radius * 2))

    # Draw the ball on the screen
    def draw(self):
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))

    # Update ball position and apply gravity
    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.y_speed += self.gravity

        # Bounce off left and right walls
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.x_speed = abs(self.x_speed)
        if self.x + self.radius >= width:
            self.x = width - self.radius
            self.x_speed = -abs(self.x_speed)

        # Bounce off floor and ceiling
        if self.y + self.radius >= height:
            self.y = height - self.radius
            self.y_speed = -abs(self.y_speed) * 0.7
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.y_speed = abs(self.y_speed)

    # Check for collision between the ball and a Pikachu
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

    # Check for collision with the center net and bounce accordingly
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

# Create player and ball instances
pikachu1 = Pikachu(100, height - 135, flip=True)     # Player 1 (flipped image)
pikachu2 = Pikachu(650, height - 135, flip=False)    # Player 2
ball = Ball()

# Main game loop
running = True
while running:
    clock.tick(60)  # Run at 60 FPS

    # Handle events (quit, pause, restart)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if paused and event.key == pygame.K_SPACE:
                # Restart game when paused
                paused = False
                loser = None
                ball = Ball()
                pikachu1 = Pikachu(100, height - 135, flip=True)
                pikachu2 = Pikachu(650, height - 135, flip=False)

    # If game is paused, show losing message
    if paused:
        show_message("Player 1 loses!" if loser == 1 else "Player 2 loses!")
        continue

    # Handle player movement input
    keys = pygame.key.get_pressed()
    pikachu1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w, 0, width // 2)
    pikachu2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, width // 2, width)

    # Update all game entities
    pikachu1.update()
    pikachu2.update()
    ball.update()

    # Handle collisions
    ball.check_collision(pikachu1)
    ball.check_collision(pikachu2)
    ball.check_net_collision()

    # Check if the ball hits the ground (game over)
    if ball.y + ball.radius >= height:
        loser = 1 if ball.x < width // 2 else 2
        paused = True
        continue

    # Draw game scene
    screen.blit(background, (0, 0))  # Draw background
    pygame.draw.rect(screen, BLACK, (net_x - net_width//2, net_top, net_width, net_height))  # Draw net
    pikachu1.draw()
    pikachu2.draw()
    ball.draw()
    pygame.display.update()

# Clean up and exit the game
pygame.quit()
sys.exit()
