import pygame
import sys
from pygame.locals import QUIT, KEYDOWN, K_SPACE

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 400
FPS = 40
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 100
HORSE_WIDTH, HORSE_HEIGHT = 10, 50
GROUND_HEIGHT = 10
SPEED_INCREMENT_INTERVAL = 1000  # 10 секунд

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horse Jump Game")

# Класс лошади
class Horse:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT - GROUND_HEIGHT - HORSE_HEIGHT, HORSE_WIDTH, HORSE_HEIGHT)
        self.is_jumping = False
        self.jump_count = 0
        self.double_jump = False

    def jump(self):
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 0
                self.double_jump = False

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            if not self.is_jumping:
                self.is_jumping = True
            elif not self.double_jump:
                self.jump_count = 10
                self.double_jump = True

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)

# Класс препятствия
class Obstacle:
    def __init__(self, x, height):
        self.rect = pygame.Rect(x, HEIGHT - GROUND_HEIGHT - height, OBSTACLE_WIDTH, height)

    def move(self, speed):
        self.rect.x -= speed

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect)

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    horse = Horse()
    obstacles = []
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 2000)

    speed = 5
    score = 0
    start_ticks = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == obstacle_timer:
                height = OBSTACLE_HEIGHT if pygame.time.get_ticks() % 4000 < 2000 else OBSTACLE_HEIGHT // 2
                obstacles.append(Obstacle(WIDTH, height))

        screen.fill(WHITE)

        # Обработка клавиш
        horse.handle_keys()

        # Обновление и отрисовка лошади
        horse.jump()
        horse.draw(screen)

        # Обновление и отрисовка препятствий
        for obstacle in obstacles:
            obstacle.move(speed)
            obstacle.draw(screen)
            if horse.rect.colliderect(obstacle.rect):
                pygame.quit()
                sys.exit()

        # Увеличение скорости каждые 10 секунд
        if pygame.time.get_ticks() - start_ticks > SPEED_INCREMENT_INTERVAL:
            speed += 1
            start_ticks = pygame.time.get_ticks()

        # Отображение счета
        score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (WIDTH - 150, 10))

        # Увеличение счета
        score += 1

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
