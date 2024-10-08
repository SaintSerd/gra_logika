import pygame
import sys
import random

# Ініціалізація Pygame
pygame.init()

# Налаштування екрану
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle City Remake")

# Налаштування кольорів
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Клас для гравця (військова машина)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Обмеження руху в межах екрану
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Клас для ворогів
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 0))  # Чорний колір для ворогів
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.change_direction_time = pygame.time.get_ticks() + random.randint(1000, 3000)
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time > self.change_direction_time:
            self.direction = random.choice(['left', 'right', 'up', 'down'])
            self.change_direction_time = current_time + random.randint(1000, 3000)

        # Рух ворога
        if self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed

# Зміна напрямку при досягненні краю екрану
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 'right'
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.direction = 'left'
        elif self.rect.top < 0:
            self.rect.top = 0
            self.direction = 'down'
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.direction = 'up'

# Ігровий цикл
def main():
    clock = pygame.time.Clock()

    # Створення гравця
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Створення ворогів
    enemy_group = pygame.sprite.Group()
    for i in range(5):
        enemy = Enemy(i * 100 + 50, 0)
        enemy_group.add(enemy)

    # Основний цикл гри
    running = True
    while running:
        clock.tick(60)  # FPS

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Отримання натиснутих клавіш
        keys_pressed = pygame.key.get_pressed()

        # Оновлення стану гравця
        player_group.update(keys_pressed)

        # Оновлення стану ворогів
        enemy_group.update()

        # Логіка гри (зіткнення)
        if pygame.sprite.spritecollide(player, enemy_group, False):
            print("Гравець зіткнувся з ворогом!")

        # Очищення екрану
        screen.fill(WHITE)

        # Малювання об'єктів
        player_group.draw(screen)
        enemy_group.draw(screen)

        # Оновлення екрану
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
