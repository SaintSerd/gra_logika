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
RED = (255, 0, 0)

# Завантаження зображень
player_image = pygame.image.load('tank.jpg').convert()  # Використовуємо convert для оптимізації
player_image.set_colorkey(WHITE)  # Видаляємо білий фон

enemy_image = pygame.image.load('enemy.jpg').convert()
enemy_image.set_colorkey(WHITE)  # Видаляємо білий фон

bullet_image = pygame.image.load('snary.webp').convert()
bullet_image.set_colorkey(WHITE)  # Видаляємо білий фон

background_image = pygame.image.load('Foyn.webp').convert()  # Завантаження фону гри (фон без прозорості)
start_background_image = pygame.image.load('images.jpg').convert()  # Фон заставки

# Масштабування зображень до потрібних розмірів
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
bullet_image = pygame.transform.scale(bullet_image, (5, 10))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Масштабування фону гри
start_background_image = pygame.transform.scale(start_background_image, (WIDTH, HEIGHT))  # Масштабування фону заставки

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

# Функція для кнопки "Play"
def draw_button(surface, color, x, y, width, height, text, font):
    pygame.draw.rect(surface, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)

# Екран заставки з кнопкою "Play"
def show_start_screen():
    screen.blit(start_background_image, (0, 0))  # Малюємо фонове зображення
    font_large = pygame.font.SysFont(None, 74)
    font_medium = pygame.font.SysFont(None, 50)

    # Малюємо текст "Battle City Remake"
    text_surface = font_large.render("Battle City Remake", True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(text_surface, text_rect)

    # Малюємо кнопку "Play"
    play_button_rect = draw_button(screen, GREEN, WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 70, "Play", font_medium)

    pygame.display.flip()

    # Чекаємо натискання кнопки "Play"
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    waiting = False  # Кнопку натиснули, починаємо гру

# Екран "Game Over"
def show_game_over_screen():
    screen.fill(BLACK)  # Фон чорного кольору
    font_large = pygame.font.SysFont(None, 74)
    font_medium = pygame.font.SysFont(None, 50)

    # Малюємо текст "Game Over"
    text_surface = font_large.render("Game Over", True, RED)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text_surface, text_rect)

    # Малюємо кнопку "Restart" для перезапуску гри
    restart_button_rect = draw_button(screen, GREEN, WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 70, "Restart", font_medium)

    pygame.display.flip()

    # Чекаємо дій користувача (натискання кнопки або закриття гри)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    waiting = False  # Кнопку натиснули, перезапускаємо гру

# Основний ігровий цикл
def main():
    clock = pygame.time.Clock()

    # Показати заставку перед початком гри
    show_start_screen()

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
                show_game_over_screen()  # Показати екран "Game Over"
                running = False

        # Очищення екрану та малювання фону
        screen.blit(background_image, (0, 0))  # Малювання фону

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

