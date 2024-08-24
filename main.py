import pygame
import random
import json

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 10
MAX_LIVES = 5
WIN_SCORE = 10
ENEMY_SPAWN_RATE = 30  # частота появления врагов

# Классы
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Survival Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.volume = 0.5
        self.player = Player(self)
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.lives = MAX_LIVES
        self.font = pygame.font.SysFont("Arial", 30)
        self.load_settings()
        self.music_playing = False

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.volume = settings.get('volume', 0.5)
                pygame.mixer.music.set_volume(self.volume)
        except FileNotFoundError:
            pass

    def save_settings(self):
        settings = {'volume': self.volume}
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def run(self):
        self.main_menu()
        self.main_loop()

    def main_menu(self):
        # Меню игры для настройки громкости и имени игрока
        while True:
            self.screen.fill((0, 0, 0))
            title = self.font.render("Survival Game", True, (255, 255, 255))
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

            # Настройки громкости
            volume_text = self.font.render(f"Volume: {self.volume:.2f}", True, (255, 255, 255))
            self.screen.blit(volume_text, (SCREEN_WIDTH // 2 - volume_text.get_width() // 2, 200))

            # Кнопки для управления
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.volume < 1.0:
                        self.volume += 0.1
                        pygame.mixer.music.set_volume(self.volume)
                    if event.key == pygame.K_DOWN and self.volume > 0.0:
                        self.volume -= 0.1
                        pygame.mixer.music.set_volume(self.volume)
                    if event.key == pygame.K_RETURN:
                        self.save_settings()
                        return

            pygame.display.flip()
            self.clock.tick(30)

    def main_loop(self):
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.play(-1)

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        if random.randint(1, ENEMY_SPAWN_RATE) == 1:
            self.enemies.append(Enemy())

        self.player.update()
        for bullet in self.bullets:
            bullet.update()
        for enemy in self.enemies:
            enemy.update()

        # Проверка столкновений
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 1
                    break

        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.running = False
                    self.game_over()

        if self.score >= WIN_SCORE:
            self.running = False
            self.win()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # Отображение счета и жизней
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))

        pygame.display.flip()

    def win(self):
        # Показать поздравление
        self.show_message("You Win!", "win_image.png", "fanfare_sound.mp3")

    def game_over(self):
        # Показать сообщение о проигрыше
        self.show_message("Game Over", "game_over_image.png", "rip_music.mp3")

    def show_message(self, message, image_file, sound_file):
        image = pygame.image.load(image_file)
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

        while True:
            self.screen.fill((0, 0, 0))
            msg_text = self.font.render(message, True, (255, 255, 255))
            self.screen.blit(msg_text, (SCREEN_WIDTH // 2 - msg_text.get_width() // 2, 100))
            self.screen.blit(image, (SCREEN_WIDTH // 2 - image.get_width() // 2, 150))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            pygame.display.flip()
            self.clock.tick(30)

class Player:
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load("player_image.png")
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Ограничение передвижения игрока по экрану
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y))

    def shoot(self):
        if len(self.game.bullets) < 5:  # ограничение на количество пуль
            bullet = Bullet(self.rect.center)
            self.game.bullets.append(bullet)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy:
    def __init__(self):
        self.image = pygame.image.load("enemy_image.png")
        self.rect = self.image.get_rect(x=random.randint(0, SCREEN_WIDTH - self.image.get_width()), y=0)

    def update(self):
        self.rect.y += ENEMY_SPEED
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.image.get_width())

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Bullet:
    def __init__(self, position):
        self.image = pygame.image.load("bullet_image.png")
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.y < 0:
            self.rect.y = -10  # удаление пули, если она вышла за экран

    def draw(self, surface):
        surface.blit(self.image, self.rect)


game = Game()
game.run()
pygame.quit()
