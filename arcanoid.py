import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1100, 700
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid")

# Классы
class Paddle:
    def __init__(self, x, y):
        self.width = 100
        self.height = 10
        self.x = x
        self.y = y
        self.speed = 10

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed

class Ball:
    def __init__(self, x, y):
        self.radius = 10
        self.x = x
        self.y = y
        self.dx = 5
        self.dy = -5

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Отскок от стен
        if self.x <= 0 or self.x >= WIDTH:
            self.dx = -self.dx
        if self.y <= 0:
            self.dy = -self.dy

    def collide_with_paddle(self, paddle):
        if self.y + self.radius >= paddle.y and paddle.x <= self.x <= paddle.x + paddle.width:
            self.dy = -self.dy

class Brick:
    def __init__(self, x, y):
        self.width = 60
        self.height = 20
        self.x = x
        self.y = y
        self.color = RED
        self.is_destroyed = False

    def draw(self, screen):
        if not self.is_destroyed:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collide_with_ball(self, ball):
        if not self.is_destroyed and self.x <= ball.x <= self.x + self.width and self.y <= ball.y <= self.y + self.height:
            self.is_destroyed = True
            ball.dy = -ball.dy

# Функция для создания кирпичиков
def create_bricks(rows, cols):
    bricks =[]
    for i in range(rows):
        for j in range(cols):
            brick = Brick(j * 70 + 35, i * 30 + 30)
            bricks.append(brick)
    return bricks

# Основной цикл игры
def main():
    clock = pygame.time.Clock()

    paddle = Paddle(WIDTH // 2 - 50, HEIGHT - 30)
    ball = Ball(WIDTH // 2, HEIGHT // 2)
    bricks = create_bricks(5, 15)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление площадкой
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")

        # Движение шарика
        ball.move()
        ball.collide_with_paddle(paddle)

        # Проверка столкновений с кирпичиками
        for brick in bricks:
            brick.collide_with_ball(ball)

        # Отрисовка
        screen.fill(BLACK)
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)

        pygame.display.flip()

        # Проверка на проигрыш
        if ball.y > HEIGHT:
            print("Game Over")
            running = False

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()