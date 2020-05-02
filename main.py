import pygame
import os
import time 
import random

from objects.laser import Laser, collide
from objects.player import Player
from objects.enemy import Enemy

class Game():
    
    def __init__(self, run=True, FPS=60, level=0, lives=0):
        self.run = run
        self.FPS = FPS
        self.level = level
        self.lives = lives


pygame.font.init()

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

def play_game():
    
    game = Game() # Attention, redondance des objets de Game à gérer.

    main_font = pygame.font.SysFont("comicsans", 30)

    FPS=60
    lives = 5
    level = 0

    enemies = []
    wave_length = 5
    enemy_vel = 1
    laser_vel = 4

    player_vel = 5
    player = Player(250, 350)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    # Defaut args : redraw_window(window=WIN, background=BG, li=lives, le=level, param_font_color=(255, 255, 255), enemies_list, player, lost):
    def redraw_window(window, background, li, le, param_font_color, enemies_list, player, lost):
        
        window.blit(background, (0,0))
        lives_label = main_font.render(f"Lives : {li}", 1, param_font_color)
        level_label = main_font.render(f"Level : {le}", 1, param_font_color)
        window.blit(lives_label, (10, 10))
        window.blit(level_label, (window.get_width() - level_label.get_width() - 10, 10))
        
        for enemy in enemies_list:
            enemy.draw(window)
        
        player.draw(window)

        if lost:
            lost_font = pygame.font.SysFont("comicsans", 60)
            lost_label = lost_font.render("GAME OVER !", 1, param_font_color)
            
            window.blit(lost_label,(int(window.get_width()/2 - lost_label.get_width()/2), int(window.get_height()/2)))

        pygame.display.update()
        
    while game.run:
        clock.tick(game.FPS)
        redraw_window(window=WIN, background=BG, li=lives, le=level, param_font_color=(255, 255, 255), enemies_list=enemies, player=player, lost=lost)

        if lives <=0 or player.health <=0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > game.FPS*5:
                game.run = False
            else:
                continue 

        if len(enemies) == 0:
            level +=1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        redraw_window(window=WIN, background=BG, li=lives, le=level, param_font_color=(255, 255, 255), enemies_list=enemies, player=player, lost=lost)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and (player.x - player_vel > 0):
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and (player.x + player_vel + player.get_width() < WIDTH):
            player.x += player_vel
        if keys[pygame.K_DOWN] and (player.y + player_vel + player.get_height() < HEIGHT):
            player.y += player_vel
        if keys[pygame.K_UP] and (player.y - player_vel > 0):
            player.y -= player_vel
        
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player, HEIGHT)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
            
        player.move_lasers(-laser_vel, enemies, HEIGHT)

def main_menu():
    run = True
    title_font = pygame.font.SysFont('comicsans', 40)
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin ...", 1, (255, 255, 255))
        WIN.blit(title_label, (int(WIDTH/2 - title_label.get_width()/2), 150))
        pygame.display.update()        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run =False
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_game()
    pygame.quit()

main_menu()
