import pygame
import os
import time
import random
pygame.font.init()

from pygame.constants import WINDOWCLOSE

WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space War")

# Load images enemy
BLACK_SHIP01 = pygame.image.load(os.path.join("pic", "ENEMY01.png"))
BLACK_SHIP02 = pygame.image.load(os.path.join("pic", "ENEMY02.png"))

# Player
BLACK_SHIP = pygame.image.load(os.path.join("pic", "BLACK_SHIP.png"))

# Laser
BLUE_LASER = pygame.image.load(os.path.join("pic", "bluelaser.png"))
PURPLE_LASER = pygame.image.load(os.path.join("pic", "purplelaser.png"))

# Background
Bg = pygame.image.load(os.path.join("pic", "bg.png"))

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.player_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.player_img, (self.x, self.y))


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.player_img = BLACK_SHIP
        self.laser_img = BLUE_LASER
        self.mask = pygame.mask.from_surface(self.player_img)
        self.max_health = health

class Enemy(Ship):
    COLOR_MAP = {
                "red": (BLACK_SHIP01, PURPLE_LASER),
                "blue": (BLACK_SHIP02, PURPLE_LASER)
                }                

    def __init__(self, x, y, color, health=100): 
        super().__init__(x, y, health)
        self.player_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.player_img)

    def move(self, vel):
        self.y += vel

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 40)
       
    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5

    player = Player(200, 350)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(Bg, (0,0))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(10, WIDTH-10), random.randrange(-1000, -300), random.choice(["red", "blue"]))
                enemies.append(enemy)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + 80 < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + 100 < HEIGHT:
            player.y += player_vel

        for enemy in enemies:
            enemy.move(enemy_vel)

        redraw_window()

main()