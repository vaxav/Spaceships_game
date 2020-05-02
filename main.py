import pygame
import os
import time 
import random

from objects.laser import Laser, collide
from objects.player import Player
from objects.enemy import Enemy

pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

def redraw_window(window, background, li, le, param_font_color, enemies_list, player, lost):     
    window.blit(background, (0,0))
    main_font = pygame.font.SysFont("comicsans", 30)
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

def player_moves(player, player_vel, width, height):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and (player.x - player_vel > 0):
        player.x -= player_vel
    if keys[pygame.K_RIGHT] and (player.x + player_vel + player.get_width() < width):
        player.x += player_vel
    if keys[pygame.K_DOWN] and (player.y + player_vel + player.get_height() < height):
        player.y += player_vel
    if keys[pygame.K_UP] and (player.y - player_vel > 0):
        player.y -= player_vel
    if keys[pygame.K_SPACE]:
        player.shoot()

def play_game():
    
    run = True
    FPS = 60
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
    
    while run:
        clock.tick(FPS)
        redraw_window(window=WIN, background=BG, li=lives, le=level, 
                    param_font_color=(255, 255, 255), enemies_list=enemies,
                    player=player, lost=lost)

        # Check if closes window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Check if gameover
        if lives <=0 or player.health <=0:
            lost = True
            lost_count += 1

        # if lost waiting 3 seconds before exit
        if lost:
            if lost_count > FPS*3:
                run = False
            else:
                continue 
        
        # Reloading enemy wave
        if len(enemies) == 0:
            level +=1
            wave_length += 5
            enemies = [Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                        for i in range(wave_length)]

        #redraw_window(window=WIN, background=BG, li=lives, le=level, param_font_color=(255, 255, 255), enemies_list=enemies, player=player, lost=lost)
        
        player_moves(player=player, player_vel=player_vel, width= WIDTH, height= HEIGHT)

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
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_game()
    pygame.quit()

main_menu()
