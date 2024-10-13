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
BLUE = (0, 0, 255)

# Завантаження зображень
player_image = pygame.image.load('tank.jpg').convert()
player_image.set_colorkey(WHITE)

enemy_image = pygame.image.load('enemy.jpg').convert()
enemy_image.set_colorkey(WHITE)

bullet_image = pygame.image.load('snary.webp').convert()
bullet_image.set_colorkey(WHITE)

ammo_pack_image = pygame.image.load('ammo_pack.png').convert()
ammo_pack_image.set_colorkey(WHITE)  # Видалення білого фону аптечки

background_image = pygame.image.load('fon.webp').convert()
start_background_image = pygame.image.load('images.jpg').convert()

# Масштабування зображень до потрібних розмірів
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
bullet_image = pygame.transform.scale(bullet_image, (5, 10))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
start_background_image = pygame.transform.scale(start_background_image, (WIDTH, HEIGHT))
ammo_pack_image = pygame.transform.scale(ammo_pack_image, (30, 30))  # Масштабування аптечки

# Клас для гравця (військовий танк)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5
        self.bullets = pygame.sprite.Group()
        self.ammo = 100  # Лічильник патронів
        self.health = 100  # Здоров'я гравця

    def update(self, keys_pressed):
        # Рух у будь-якому напрямку, але не виходимо за межі екрану
        if keys_pressed[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        if self.ammo > 0:  # Стрільба можлива тільки якщо є патрони
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)
            self.ammo -= 1  # Витрачаємо патрони

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
        self.rect.y += 1
        if self.rect.top >= HEIGHT:
            self.kill()

# Клас для аптечки (поповнення патронів та здоров'я)
class AmmoPack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ammo_pack_image  # Використання зображення аптечки
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(0, HEIGHT - 100)

# Функція для малювання кнопки
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
def show_game_over_screen(message):
    screen.fill(BLACK)  # Фон чорного кольору
    font_large = pygame.font.SysFont(None, 74)
    font_medium = pygame.font.SysFont(None, 50)

    # Малюємо текст (виграш чи поразка)
    text_surface = font_large.render(message, True, RED)
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

    game_loop()  # Перезапуск гри

# Основний ігровий цикл
def game_loop():
    clock = pygame.time.Clock()

    # Створення гравця
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Створення ворогів
    enemy_group = pygame.sprite.Group()

    # Створення аптечок для патронів та здоров'я
    ammo_packs = pygame.sprite.Group()

    # Лічильник для кількості появ аптечки (максимум 3 рази)
    ammo_pack_count = 0
    max_ammo_packs = 3

    # Лічильник знищених ворогів
    enemy_kills = 0
    max_enemy_kills = 50  # Виграш після знищення 50 ворогів

    # База гравця
    base_health = 100
    font = pygame.font.SysFont(None, 36)

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

        # Оновлення стану аптечок
        ammo_packs.update()

        # Логіка гри: генерація ворогів
        if random.randint(1, 100) < 2:
            enemy = Enemy(random.randint(0, WIDTH - 50), 0)
            enemy_group.add(enemy)

        # Логіка гри: зіткнення снарядів з ворогами
        for bullet in player.bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, True)
            if hit_enemies:
                bullet.kill()
                enemy_kills += 1  # Додаємо кількість знищених ворогів

        # Перевірка на перемогу (якщо знищено 50 ворогів)
        if enemy_kills >= max_enemy_kills:
            show_game_over_screen("You Win!")  # Показати екран "You Win"
            running = False

        # Логіка гри: вороги досягли бази
        for enemy in enemy_group:
            if enemy.rect.bottom >= HEIGHT - 50:  # Ворог досягає бази
                base_health -= 10
                enemy.kill()
            if base_health <= 0:
                show_game_over_screen("Game Over")  # Показати екран "Game Over"
                running = False

        # Перевірка зіткнення гравця з ворогом (гравець втрачає здоров'я)
        if pygame.sprite.spritecollideany(player, enemy_group):
            player.health -= 10  # Зменшення здоров'я на 10 при зіткненні
            if player.health <= 0:
                show_game_over_screen("Game Over")  # Завершення гри при 0 здоров'я
                running = False

        # Поява аптечки, якщо кількість патронів < 20 або здоров'я < 50 і ще не використано всі 3 аптечки
        if (player.ammo < 20 or player.health < 50) and len(ammo_packs) == 0 and ammo_pack_count < max_ammo_packs:
            ammo_pack = AmmoPack()
            ammo_packs.add(ammo_pack)
            ammo_pack_count += 1

        # Перевірка зіткнення гравця з аптечкою (поповнення патронів та здоров'я)
        if pygame.sprite.spritecollideany(player, ammo_packs):
            player.ammo += 50  # Поповнюємо патрони на 50
            player.health += 30  # Поповнюємо здоров'я на 30
            if player.health > 100:
                player.health = 100  # Здоров'я не може бути більше 100
            ammo_packs.empty()  # Видаляємо аптечку після збору

        # Очищення екрану та малювання фону
        screen.blit(background_image, (0, 0))  # Малювання фону

        # Малювання бази
        pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 100, HEIGHT - 50, 200, 50))

        # Малювання гравця, ворогів та аптечки
        player_group.draw(screen)
        enemy_group.draw(screen)
        player.bullets.draw(screen)
        ammo_packs.draw(screen)

        # Відображення здоров'я бази, кількості патронів, здоров'я гравця та знищених ворогів
        health_text = font.render(f'Base Health: {base_health}', True, WHITE)
        screen.blit(health_text, (10, 10))
        ammo_text = font.render(f'Ammo: {player.ammo}', True, WHITE)
        screen.blit(ammo_text, (10, 50))
        player_health_text = font.render(f'Player Health: {player.health}', True, WHITE)
        screen.blit(player_health_text, (10, 90))
        enemy_kills_text = font.render(f'Enemies Killed: {enemy_kills}', True, WHITE)
        screen.blit(enemy_kills_text, (10, 130))

        # Оновлення екрану
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    show_start_screen()  # Показати заставку на початку
    game_loop()  # Основний ігровий цикл
