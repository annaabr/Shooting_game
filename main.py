import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 10
MAX_LIVES = 5
WIN_SCORE = 10

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survival Game")

# Загрузка изображений и изменение их размеров
player_image = pygame.image.load('img/player_image.png')

enemy_image = pygame.image.load('img/enemy_image.png')
enemy_image = pygame.transform.scale(enemy_image, (100,90))

bullet_image = pygame.image.load('img/bullet_image.png')
win_image = pygame.image.load('img/win_image.png')
lose_image = pygame.image.load('img/rip_image.png')

# Загрузка звуков
win_sound = pygame.mixer.Sound('music/winner_sound.mp3')
lose_sound = pygame.mixer.Sound('music/rip_music.mp3')
background_music = pygame.mixer.Sound('music/background_music.mp3')

# Классы
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PLAYER_SPEED

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([0, SCREEN_WIDTH])  # Случайно выбираем сторону
        self.rect.y = random.randint(0, SCREEN_HEIGHT)

    def update(self):
        if self.rect.x < SCREEN_WIDTH // 2:
            self.rect.x += ENEMY_SPEED
        else:
            self.rect.x -= ENEMY_SPEED
            if self.rect.y < SCREEN_HEIGHT // 2:
                self.rect.y += ENEMY_SPEED
            else:
                self.rect.y -= ENEMY_SPEED

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

# Инициализация спрайтов
player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Переменные игры
lives = MAX_LIVES
score = 0
enemy_spawn_timer = 0
clock = pygame.time.Clock()

# Загрузка музыки
pygame.mixer.music.load('music/background_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullets.add(bullet)

    # Обновление
    player.update()
    bullets.update()
    enemies.update()

    # Проверка на столкновения
    for bullet in bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
        if hit_enemies:
            score += 1
            bullet.kill()

    if pygame.sprite.spritecollide(player, enemies, False):
        lives -= 1
        if lives <= 0:
            pygame.mixer.music.stop()
            lose_sound.play()
            screen.blit(lose_image, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

    if score >= WIN_SCORE:
        pygame.mixer.music.stop()
        win_sound.play()
        screen.blit(win_image, (0, 0))
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    # Появление врагов
    enemy_spawn_timer += 1
    if enemy_spawn_timer > 60:  # Каждые 60 кадров
        enemy = Enemy()
        enemies.add(enemy)
        enemy_spawn_timer = 0

    # Отрисовка
    screen.fill((0,0,0))
    screen.blit(player.image, player.rect)
    enemies.draw(screen)
    bullets.draw(screen)

    # Отображение жизней и счета
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f'Lives: {lives}', True, (255, 255, 255))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (10, 50))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)