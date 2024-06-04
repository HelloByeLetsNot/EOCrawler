import pygame
import sys
import random
import threading
from movement import Character, Enemy, iso_to_cart, cart_to_iso, a_star
from map_generator import generate_map, draw_map
from combat import attack, roll_d20

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ISO_TILE_WIDTH = 64
ISO_TILE_HEIGHT = 32
FPS = 60

tile_sheet = pygame.image.load('tile.png')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Isometric Tile-Based Game')

clock = pygame.time.Clock()

player = Character(10, 10, 'sprite.png')  # Initialize player at position (10, 10)
enemies = [Enemy(random.randint(0, 19), random.randint(0, 14), 'sprite.png') for _ in range(5)]

game_map = generate_map(tile_sheet, 20, 15)

def character_update_thread():
    while running:
        player.update()
        for enemy in enemies:
            enemy.update()
        pygame.time.wait(30)

running = True
threading.Thread(target=character_update_thread, daemon=True).start()

current_target = None

while running:
    try:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                cart_x, cart_y = iso_to_cart(mouse_x, mouse_y)
                for enemy in enemies:
                    if enemy.cart_x == cart_x and enemy.cart_y == cart_y:
                        current_target = enemy
                        player.path = a_star((player.cart_x, player.cart_y), (cart_x, cart_y), game_map)
                        break
                if not current_target:
                    player.path = a_star((player.cart_x, player.cart_y), (cart_x, cart_y), game_map)

        iso_x, iso_y = cart_to_iso(player.cart_x, player.cart_y)
        offset_x = SCREEN_WIDTH // 2 - iso_x
        offset_y = SCREEN_HEIGHT // 2 - iso_y

        draw_map(game_map, offset_x, offset_y, screen)
        player.draw(screen, offset_x, offset_y)

        for enemy in enemies[:]:
            if enemy.stats['hp'] > 0:
                enemy.draw(screen, offset_x, offset_y)
            else:
                enemies.remove(enemy)
                if current_target == enemy:
                    current_target = None

        if current_target and not player.is_moving:
            attack(player, current_target)
            if current_target.stats['hp'] <= 0:
                current_target = None

        pygame.display.flip()
        clock.tick(FPS)

    except Exception as e:
        print(f"Error: {e}")
        running = False

pygame.quit()
sys.exit()