import pygame
import random
import math
from queue import PriorityQueue

# Инициализация Pygame
pygame.init()

# Размеры окна
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle City Remake")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
BROWN = (139, 69, 19)

# Скорость танков и пуль
TANK_SPEED = 2
ENEMY_SPEED = 1
BULLET_SPEED = 5

# Радиус видимости врага
ENEMY_SIGHT_RADIUS = 150

# Класс Танка
class Tank:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.direction = pygame.K_UP  # Начальная позиция - вверх
        self.bullets = []

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, keys, obstacles):
        old_x, old_y = self.rect.x, self.rect.y
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= TANK_SPEED
            self.direction = pygame.K_LEFT
        if keys[pygame.K_RIGHT]:
            self.rect.x += TANK_SPEED
            self.direction = pygame.K_RIGHT
        if keys[pygame.K_UP]:
            self.rect.y -= TANK_SPEED
            self.direction = pygame.K_UP
        if keys[pygame.K_DOWN]:
            self.rect.y += TANK_SPEED
            self.direction = pygame.K_DOWN

        # Проверка на столкновение с препятствиями
        if self.check_collision(obstacles):
            self.rect.x, self.rect.y = old_x, old_y

    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                return True
        return False

    def shoot(self):
        if len(self.bullets) < 3:  # Ограничение на количество пуль
            if self.direction == pygame.K_UP:
                bullet = Bullet(self.rect.centerx, self.rect.top, 0, -BULLET_SPEED)
            elif self.direction == pygame.K_DOWN:
                bullet = Bullet(self.rect.centerx, self.rect.bottom, 0, BULLET_SPEED)
            elif self.direction == pygame.K_LEFT:
                bullet = Bullet(self.rect.left, self.rect.centery, -BULLET_SPEED, 0)
            elif self.direction == pygame.K_RIGHT:
                bullet = Bullet(self.rect.right, self.rect.centery, BULLET_SPEED, 0)
            self.bullets.append(bullet)

# Класс Пули
class Bullet:
    def __init__(self, x, y, dx, dy):
        self.rect = pygame.Rect(x, y, 5, 5)
        self.dx = dx
        self.dy = dy

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

    def is_off_screen(self):
        return (self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or 
                self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT)

# Класс Препятствия (стены)
class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = 3  # Стены могут разрушаться

    def draw(self):
        pygame.draw.rect(screen, BROWN, self.rect)

    def hit(self):
        self.health -= 1
        return self.health <= 0  # Возвращает True, если препятствие разрушено

# Функция для поиска пути A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, obstacles):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while not open_set.empty():
        _, current = open_set.get()

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Четыре направления
            neighbor = (current[0] + dx, current[1] + dy)
            if any(ob.rect.collidepoint(neighbor) for ob in obstacles):
                continue  # Игнорируем, если есть препятствие

            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                open_set.put((f_score[neighbor], neighbor))

    return None  # Путь не найден



class Enemy(Tank):
    def __init__(self, x, y, color, patrol_points):
        super().__init__(x, y, color)
        self.patrol_points = patrol_points
        self.current_target_index = 0
        self.patrolling = True
        self.path = []
        self.player_last_seen = None
        self.player_visible = False
        self.player_in_sight = False

    def distance_to_player(self, player):
        """Рассчитывает расстояние до игрока"""
        return math.sqrt((self.rect.centerx - player.rect.centerx) ** 2 + 
                         (self.rect.centery - player.rect.centery) ** 2)

    def is_player_visible(self, player, obstacles):
        """Проверка, видит ли враг игрока, учитывая стены"""
        for obstacle in obstacles:
            # Создаем линию (отличается от той что мы видим) от врага до игрока
            line_rect = pygame.Rect(self.rect.center, (player.rect.x - self.rect.x, player.rect.y - self.rect.y))
            if obstacle.rect.colliderect(line_rect):
                return False  # Если есть препятствие, враг не видит игрока
        return True  # Игрок виден, если нет препятствий

    def update_behavior(self, player, obstacles):
        """Обновляет поведение врага"""
        # Проверка расстояния до игрока
        distance = self.distance_to_player(player)
        if distance <= ENEMY_SIGHT_RADIUS:
            self.player_visible = self.is_player_visible(player, obstacles)
            if self.player_visible:
                # Если игрок виден, запоминаем его координаты
                self.player_in_sight = True
                self.player_last_seen = (player.rect.x, player.rect.y)
                self.move_towards_last_seen_player(obstacles)
            else:
                # Игрок не виден, продолжаем патрулировать
                self.player_in_sight = True
                self.patrolling = True
                self.move_to_next_patrol_point()
        else:
            # Игрок вне радиуса видимости
            self.player_in_sight = False
            self.patrolling = True
            self.move_to_next_patrol_point()

    def move_towards_last_seen_player(self, obstacles):
        """Движется к последним известным координатам игрока"""
        if self.player_last_seen:
            target = self.player_last_seen
            self.move_to_point(target, obstacles)

    def move_to_point(self, point, obstacles):
        """Движение к точке"""
        old_x, old_y = self.rect.x, self.rect.y

        if point[0] < self.rect.x:
            self.rect.x -= ENEMY_SPEED
        elif point[0] > self.rect.x:
            self.rect.x += ENEMY_SPEED

        if point[1] < self.rect.y:
            self.rect.y -= ENEMY_SPEED
        elif point[1] > self.rect.y:
            self.rect.y += ENEMY_SPEED

        if self.check_collision(obstacles):
            self.rect.x, self.rect.y = old_x, old_y

    def move_to_next_patrol_point(self):
        """Перемещается к следующей точке патрулирования"""
        target = self.patrol_points[self.current_target_index]
        self.move_to_point(target, [])

        if abs(self.rect.x - target[0]) < 5 and abs(self.rect.y - target[1]) < 5:
            self.current_target_index = (self.current_target_index + 1) % len(self.patrol_points)

    def move_towards_player(self, player, obstacles):
        """Преследование игрока"""
        if self.is_player_visible(player, obstacles):
            if self.player_last_seen != (player.rect.x, player.rect.y):
                self.path = a_star((self.rect.x, self.rect.y), (player.rect.x, player.rect.y), obstacles)
                self.player_last_seen = (player.rect.x, player.rect.y)

            if self.path:
                next_node = self.path[0]  # Получаем следующую точку пути
                self.move_to_point((next_node[0], next_node[1]), obstacles)
        else:
            self.move_to_next_patrol_point()  # Игрок не виден, продолжаем патрулировать




# Главный цикл игры
def main():
    clock = pygame.time.Clock()
    player = Tank(300, 200, GREEN)

    # Определение патрульных точек для двух врагов
    patrol_points_1 = [(50, 50), (50, 350), (550, 350), (550, 50)]  # Против часовой стрелки (пример)
    patrol_points_2 = [(550, 50), (550, 350), (50, 350), (50, 50)]  # По часовой стрелке (пример)

    # Создание двух врагов
    enemies = [
        Enemy(50, 50, RED, patrol_points_1),
        Enemy(550, 50, BLUE, patrol_points_2)  # Новый враг с другим цветом и патрульными точками
    ]

    obstacles = [Obstacle(200, 100, 50, 200), Obstacle(400, 100, 50, 200)]  # Примеры препятствий

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        keys = pygame.key.get_pressed()
        player.move(keys, obstacles)

        # Обновление врагов
        for enemy in enemies:
            enemy.update_behavior(player, obstacles)

        # Обновление пуль
        for bullet in player.bullets:
            bullet.move()
            if bullet.is_off_screen():
                player.bullets.remove(bullet)

        # Отрисовка
        screen.fill(WHITE)
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for obstacle in obstacles:
            obstacle.draw()
        for bullet in player.bullets:
            bullet.draw()

        # Отрисовка радиуса видимости врага
        for enemy in enemies:
            pygame.draw.circle(screen, GRAY, (enemy.rect.centerx, enemy.rect.centery), ENEMY_SIGHT_RADIUS, 1)
            if enemy.player_in_sight:
                pygame.draw.line(screen, BLACK, enemy.rect.center, player.rect.center, 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
