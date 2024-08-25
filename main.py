import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 10
ENEMY_SPEED = 2
MAX_LIVES = 5
WIN_SCORE = 10
BACK_GROUND_COLOR = (200,255,200)
FONT_COLOR = (0, 0, 0)

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survival Game")

# Загрузка изображений и изменение их размеров
player_image = pygame.image.load('img/player_image.png')
player_image = pygame.transform.scale(player_image, (100,90))

enemy_image = pygame.image.load('img/enemy_image.png')
enemy_image = pygame.transform.scale(enemy_image, (100,90))

win_image = pygame.image.load('img/win_image.png')
win_image = pygame.transform.scale(win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

lose_image = pygame.image.load('img/rip_image.png')
lose_image = pygame.transform.scale(lose_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

fire_image = pygame.image.load('img/fire_image.png')
fire_image = pygame.transform.scale(fire_image, (100, 80))

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
        if self.rect.x < player.rect.x:
            self.rect.x += ENEMY_SPEED
        else:
            self.rect.x -= ENEMY_SPEED
        if self.rect.y < player.rect.y:
            self.rect.y += ENEMY_SPEED
        else:
            self.rect.y -= ENEMY_SPEED

# Инициализация спрайтов
player = Player()
enemies = pygame.sprite.Group()

# Переменные игры
lives = MAX_LIVES
score = 0
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
        if event.type == pygame.MOUSEBUTTONDOWN: #****
            if event.button == 1:  # Левый клик мыши
                for enemy in enemies:
                    if enemy.rect.collidepoint(event.pos):  # Проверка, попал ли клик в спрайт
                        enemies.remove(enemy)  # Удаляем спрайт (или можно просто не рисовать его)
                        score += 1
                        break  # Выходим из цикла, если спрайт удален

    # Обновление
    player.update()
    enemies.update()

    # Проверка на столкновения
    if pygame.sprite.spritecollide(player, enemies, True):
        lives -= 1
        if lives <= 0:
            pygame.time.delay(2000)
            pygame.mixer.music.stop()
            lose_sound.play()
            screen.blit(lose_image, (0, 0))
            pygame.display.flip()
            pygame.time.delay(5000)
            pygame.quit()
            sys.exit()

    if score >= WIN_SCORE:
        pygame.mixer.music.stop()
        win_sound.play()
        screen.fill(BACK_GROUND_COLOR)
        screen.blit(win_image, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5000)
        pygame.quit()
        sys.exit()

    # Появление врагов
    if len(enemies) == 0:
        enemy = Enemy()
        enemies.add(enemy)
        #enemy_spawn_timer = 0

    # Отрисовка
    screen.fill(BACK_GROUND_COLOR)
    screen.blit(player.image, player.rect)
    enemies.draw(screen)

    # Отображение жизней и счета
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f'Lives: {lives}', True, FONT_COLOR)
    score_text = font.render(f'Score: {score}', True, FONT_COLOR)
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (10, 50))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)