import pygame
import random
import sys

# Ініціалізація Pygame
pygame.init()

# Змінений розмір вікна гри
WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 768
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Встановлюємо кольори
WHITE = (255, 255, 255)

# Створюємо вікно
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Battle City Remake")

# FPS для гри
FPS = 60
clock = pygame.time.Clock()

# Завантаження зображень
background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

player_image = pygame.image.load('tank.png')
player_image = pygame.transform.scale(player_image, (50, 50))

enemy_image = pygame.image.load('enemy_tank.png')
enemy_image = pygame.transform.scale(enemy_image, (60, 60))


bullet_image = pygame.Surface((8, 8))
bullet_image.fill((255, 0, 0))  # Червона куля

# Завантажуємо зображення для підсилювачів
health_image = pygame.image.load('health_boost.png')
health_image = pygame.transform.scale(health_image, (40, 40))

double_bullet_image = pygame.image.load('double_bullet_boost.png')
double_bullet_image = pygame.transform.scale(double_bullet_image, (60, 40))

# Звуки
shoot_sound = pygame.mixer.Sound('shoot.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')
pygame.mixer.music.load('background_music.mp3')

# Гравець
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
        self.speed = 6
        self.health = 100
        self.double_shot = False
        self.invincible = False
        self.invincible_timer = 0
        self.lives = 3

    def update(self, keys, obstacles):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Обмежуємо рух в межах екрану
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT

        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        if pygame.sprite.spritecollide(self, obstacles, False):
            if keys[pygame.K_LEFT]:
                self.rect.x += self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x -= self.speed
            if keys[pygame.K_UP]:
                self.rect.y += self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y -= self.speed

    def take_damage(self, damage):
        if not self.invincible:
            self.health -= damage
            if self.health <= 0:
                self.lives -= 1
                self.health = 100
                if self.lives <= 0:
                    self.health = 0
                    return True
            self.invincible = True
            self.invincible_timer = FPS * 2
        return False

    def shoot(self):
        if self.double_shot:
            bullet_left = Bullet(self.rect.centerx - 15, self.rect.top)
            bullet_right = Bullet(self.rect.centerx + 15, self.rect.top)
            return [bullet_left, bullet_right]
        else:
            return [Bullet(self.rect.centerx, self.rect.top)]

# Вороги
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - 50)
        self.rect.y = random.randint(0, WINDOW_HEIGHT // 2 - 100)
        self.speed = random.uniform(2, 4)
        self.shoot_timer = random.randint(60, 120)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.rect.y = -50
            self.rect.x = random.randint(0, WINDOW_WIDTH - 50)
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(60, 120)
            return self.shoot()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, direction=1)
        return bullet


# Кулі
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=-1):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10 * direction

    def update(self):
        self.rect.y += self.speed
        if self.rect.top < 0 or self.rect.bottom > WINDOW_HEIGHT:
            self.kill()

# Підсилювачі
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'health':
            self.image = health_image
        elif type == 'double_bullet':
            self.image = double_bullet_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - 30)
        self.rect.y = random.randint(0, WINDOW_HEIGHT // 2)
        self.speed = 1
        self.type = type

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

# Клас для перешкод
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((128, 128, 128))  # Сірий колір для перешкоди
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Функція для відображення тексту
def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Головне меню
def main_menu():
    while True:
        screen.blit(background_image, (0, 0))  # Фон
        draw_text(screen, "Battle City Remake", 64, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        draw_text(screen, "Натисніть клавішу для початку", 32, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                game_loop()

# Екран поразки
def game_over():
    while True:
        screen.blit(background_image, (0, 0))  # Фон
        draw_text(screen, "Гра закінчена", 64, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        draw_text(screen, "Натисніть клавішу для повторної гри", 32, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                game_loop()

# Основний ігровий цикл
def game_loop():
    pygame.mixer.music.play(-1)

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    enemies = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    for _ in range(5):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    bullets = pygame.sprite.Group()
    
    powerups = pygame.sprite.Group()

    obstacles = pygame.sprite.Group()
    obstacle1 = Obstacle(200, 300, 150, 50)
    obstacle2 = Obstacle(600, 500, 200, 50)
    obstacle3 = Obstacle(400, 200, 150, 50)
    all_sprites.add(obstacle1, obstacle2, obstacle3)
    obstacles.add(obstacle1, obstacle2, obstacle3)

    score = 0
    level = 1
    boss_defeated = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    new_bullets = player.shoot()
                    for bullet in new_bullets:
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                    shoot_sound.play()

        keys = pygame.key.get_pressed()
        player.update(keys, obstacles)

        for sprite in all_sprites:
            if isinstance(sprite, Player):
                continue
            elif isinstance(sprite, Enemy):
                new_enemy_bullet = sprite.update()
                if new_enemy_bullet:
                    all_sprites.add(new_enemy_bullet)
                    enemy_bullets.add(new_enemy_bullet)
            else:
                sprite.update()

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            explosion_sound.play()
            score += 1
            if not boss_defeated:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
            
            if random.random() > 0.8:
                powerup_type = random.choice(['health', 'double_bullet'])
                powerup = PowerUp(powerup_type)
                all_sprites.add(powerup)
                powerups.add(powerup)

        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            player_died = player.take_damage(20)
            if player_died:
                running = False
                game_over()

        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if hits:
            player_died = player.take_damage(10)
            if player_died:
                running = False
                game_over()
        
        powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in powerup_hits:
            if powerup.type == 'health':
                player.health = min(player.health + 20, 100)
            elif powerup.type == 'double_bullet':
                player.double_shot = True

        pygame.sprite.groupcollide(bullets, obstacles, True, False)
        pygame.sprite.groupcollide(enemy_bullets, obstacles, True, False)

        

        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {score}", 18, WINDOW_WIDTH // 2, 10)
        draw_text(screen, f"Health: {player.health}", 18, 70, 10)
        draw_text(screen, f"Lives: {player.lives}", 18, 70, 40)

        pygame.display.flip()
        clock.tick(FPS)

# Запуск головного меню
if __name__ == "__main__":
    main_menu()
