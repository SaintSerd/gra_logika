import pygame
import sys

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
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

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
