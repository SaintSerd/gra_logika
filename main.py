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
GREEN = (0, 255, 0)

# Завантаження зображень
player_image = pygame.image.load('tank.jpg')
enemy_image = pygame.image.load('enemy.jpg')
bullet_image = pygame.image.load('snary.webp')

# Масштабування зображень до потрібних розмірів
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
bullet_image = pygame.transform.scale(bullet_image, (5, 10))

# Клас для гравця (військовий танк)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5
        self.bullets = pygame.sprite.Group()

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullets.add(bullet)

# Клас для снарядів
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Клас для ворогів (танки)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction = random.choice(['left', 'right'])
        
    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
            if self.rect.left <= 0:
                self.rect.left = 0
                self.direction = 'right'
        elif self.direction == 'right':
            self.rect.x += self.speed
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH
                self.direction = 'left'
                
        # Рух вниз до бази
        self.rect.y += 1
        if self.rect.top >= HEIGHT:
            self.kill()

# Ігровий цикл
def main():
    clock = pygame.time.Clock()
    
    # Створення гравця
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Створення ворогів
    enemy_group = pygame.sprite.Group()
    
    # База гравця
    base_health = 100
    font = pygame.font.SysFont(None, 36)

    # Основний цикл гри
    running = True
    while running:
        clock.tick(60)  # FPS

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot()

        # Отримання натиснутих клавіш
        keys_pressed = pygame.key.get_pressed()

        # Оновлення стану гравця
        player_group.update(keys_pressed)

        # Оновлення снарядів
        player.bullets.update()

        # Оновлення стану ворогів
        enemy_group.update()

        # Логіка гри: генерація ворогів
        if random.randint(1, 100) < 2:
            enemy = Enemy(random.randint(0, WIDTH - 50), 0)
            enemy_group.add(enemy)

        # Логіка гри: зіткнення снарядів з ворогами
        for bullet in player.bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, True)
            if hit_enemies:
                bullet.kill()

        # Логіка гри: вороги досягли бази
        for enemy in enemy_group:
            if enemy.rect.bottom >= HEIGHT - 50:  # Ворог досягає бази
                base_health -= 10
                enemy.kill()
            if base_health <= 0:
                print("Гра закінчена! Базу зруйновано.")
                running = False

        # Очищення екрану
        screen.fill(WHITE)

        # Малювання бази
        pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 100, HEIGHT - 50, 200, 50))

        # Малювання гравця та ворогів
        player_group.draw(screen)
        enemy_group.draw(screen)
        player.bullets.draw(screen)

        # Відображення здоров'я бази
        health_text = font.render(f'Base Health: {base_health}', True, BLACK)
        screen.blit(health_text, (10, 10))

        # Оновлення екрану
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
