import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
width, height = 800, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pikachu Volleyball")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS 설정
clock = pygame.time.Clock()

background = pygame.image.load('background.png').convert_alpha()
background = pygame.transform.scale(background, (width, height))
background.set_alpha(255)  # 0~255 사이 (255 = 완전 불투명, 0 = 완전 투명)

net_x = width // 2
net_width = 10
net_height = 200
net_top = height - net_height
net_bottom = height


# 피카츄 클래스
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
            self.image = pygame.transform.flip(self.image, True, False)  # 가로로 뒤집기

    def draw(self):
        screen.blit(self.image, (self.x, self.y))  # 노란색 피카츄

    def move(self, keys, left_key, right_key, jump_key, left_limit, right_limit):
        if keys[left_key]:
            self.x -= self.velocity
        if keys[right_key]:
            self.x += self.velocity
        if not self.jump and keys[jump_key]:
            self.jump = True
            self.y_speed = -self.jump_speed

        # 이동 제한
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

# 공 클래스
class Ball:
    def __init__(self):
        self.x = width // 2
        self.y = height // 2
        self.radius = 40
        self.x_speed = 4
        self.y_speed = 0
        self.gravity = 0.3
        self.image = pygame.image.load('jiu.png')  # <-- 파일 이름
        self.image = pygame.transform.smoothscale(self.image, (self.radius * 2, self.radius * 2))

    def draw(self):
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.y_speed += self.gravity

        # 벽 충돌 (좌우)
        if self.x - self.radius <= 0:
            self.x = self.radius  # 벽 밖으로 안 나가게 고정
            self.x_speed = abs(self.x_speed)  # 오른쪽으로 튕기기

        if self.x + self.radius >= width:
            self.x = width - self.radius
            self.x_speed = -abs(self.x_speed)  # 왼쪽으로 튕기기

        # 땅 충돌 (아래)
        if self.y + self.radius >= height:
            self.y = height - self.radius
            self.y_speed = -abs(self.y_speed) * 0.7  # 위로 튕기기

        # 천장 충돌 (위)
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.y_speed = abs(self.y_speed)  # 아래로 튕기기

    def check_collision(self, pikachu):
        # 간단한 박스-원 충돌 감지
        if (self.x + self.radius > pikachu.x and
            self.x - self.radius < pikachu.x + pikachu.width and
            self.y + self.radius > pikachu.y and
            self.y - self.radius < pikachu.y + pikachu.height):
            # 충돌했으면 y 방향 튕기기
            self.y_speed = -10  # 위로 튕기기
            # 추가로 피카츄가 움직이는 방향으로 약간 밀어줄 수도 있음
            if self.x < pikachu.x + pikachu.width // 2:
                self.x_speed = -abs(self.x_speed)
            else:
                self.x_speed = abs(self.x_speed)

    def check_net_collision(self):
        net_x = width // 2
        net_width = 10
        net_height = 200

        # 네트 범위
        net_top = height - net_height
        net_bottom = height

        # 공과 네트 충돌 감지
        if (net_x - net_width//2 < self.x < net_x + net_width//2 and
            net_top < self.y + self.radius and self.y - self.radius < net_bottom):
            # 네트에 부딪히면 방향 바꾸기
            if self.x_speed > 0:
                self.x = net_x - net_width//2 - self.radius
                self.x_speed = -abs(self.x_speed)
            else:
                self.x = net_x + net_width//2 + self.radius
                self.x_speed = abs(self.x_speed)

            # 살짝 위로 튕기게 만들 수도 있음
            self.y_speed = -abs(self.y_speed) * 0.7


# 객체 생성
pikachu1 = Pikachu(100, height - 135, flip=True)
pikachu2 = Pikachu(650, height - 135, flip=False)
ball = Ball()

# 게임 루프
running = True
while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False   

    keys = pygame.key.get_pressed()
    pikachu1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w, 0, width // 2)  # 왼쪽 피카츄: 0 ~ 화면 중앙
    pikachu2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, width // 2, width)  # 오른쪽 피카츄: 화면 중앙 ~ 끝


    pikachu1.update()
    pikachu2.update()
    ball.update()

    ball.check_collision(pikachu1)
    ball.check_collision(pikachu2)
    ball.check_net_collision()


    screen.blit(background, (0, 0))
    # 네트 그리기
    pygame.draw.rect(screen, BLACK, (net_x - net_width//2, net_top, net_width, net_height))

    pikachu1.draw()
    pikachu2.draw()
    ball.draw()

    pygame.display.update()

pygame.quit()
sys.exit()
