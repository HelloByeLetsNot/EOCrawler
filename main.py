import pygame
import sys
import random
import threading

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
ISO_TILE_WIDTH = TILE_SIZE * 2
ISO_TILE_HEIGHT = TILE_SIZE
FPS = 60

tile_sheet = pygame.image.load('tile.png')
sprite_sheet = pygame.image.load('sprite.png')

sprite_sheet_width, sprite_sheet_height = sprite_sheet.get_size()

columns = 11
rows = 2

CHARACTER_WIDTH = sprite_sheet_width // columns
CHARACTER_HEIGHT = sprite_sheet_height // rows

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Isometric Tile-Based Game')

clock = pygame.time.Clock()

def cart_to_iso(cart_x, cart_y):
    iso_x = (cart_x - cart_y) * ISO_TILE_WIDTH // 2
    iso_y = (cart_x + cart_y) * ISO_TILE_HEIGHT // 2
    return iso_x, iso_y

def iso_to_cart(iso_x, iso_y):
    cart_x = (iso_x // (ISO_TILE_WIDTH // 2) + iso_y // (ISO_TILE_HEIGHT // 2)) // 2
    cart_y = (iso_y // (ISO_TILE_HEIGHT // 2) - iso_x // (ISO_TILE_WIDTH // 2)) // 2
    return cart_x, cart_y

class Character:
    def __init__(self, x, y):
        self.cart_x = x
        self.cart_y = y
        self.speed = 0.2
        self.frame = 0
        self.direction = 'down'
        self.animations = self.load_animations()
        self.target_pos = None
        self.is_moving = False
        self.animation_delay = 0
        self.stats = {
            'str': 1,
            'def': 1,
            'acc': 1,
            'hp': 10
        }

    def load_animations(self):
        animations = {
            'down': [sprite_sheet.subsurface(pygame.Rect(i * CHARACTER_WIDTH, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)) for i in range(1, 6)],
            'up': [sprite_sheet.subsurface(pygame.Rect(i * CHARACTER_WIDTH, CHARACTER_HEIGHT, CHARACTER_WIDTH, CHARACTER_HEIGHT)) for i in range(1, 6)],
            'left': [sprite_sheet.subsurface(pygame.Rect(i * CHARACTER_WIDTH, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)) for i in range(1, 6)],
            'right': [pygame.transform.flip(sprite_sheet.subsurface(pygame.Rect(i * CHARACTER_WIDTH, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)), True, False) for i in range(1, 6)],
            'idle_down': [sprite_sheet.subsurface(pygame.Rect(0, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT))],
            'idle_up': [sprite_sheet.subsurface(pygame.Rect(0, CHARACTER_HEIGHT, CHARACTER_WIDTH, CHARACTER_HEIGHT))],
            'idle_left': [sprite_sheet.subsurface(pygame.Rect(0, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT))],
            'idle_right': [pygame.transform.flip(sprite_sheet.subsurface(pygame.Rect(0, 0, CHARACTER_WIDTH, CHARACTER_HEIGHT)), True, False)]
        }
        return animations

    def move(self, dx, dy):
        self.cart_x += dx * self.speed
        self.cart_y += dy * self.speed
        self.is_moving = True
        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'

    def move_to_target(self):
        if self.target_pos:
            target_cart_x, target_cart_y = self.target_pos
            dx = target_cart_x - self.cart_x
            dy = target_cart_y - self.cart_y
            dist = (dx**2 + dy**2) ** 0.5
            if dist < self.speed:
                self.cart_x, self.cart_y = target_cart_x, target_cart_y
                self.target_pos = None
                self.is_moving = False
            else:
                dx /= dist
                dy /= dist
                self.move(dx, dy)
        else:
            self.is_moving = False

    def update(self):
        if self.is_moving:
            self.animation_delay += 1
            if self.animation_delay % 20 == 0:
                self.frame = (self.frame + 1) % len(self.animations[self.direction])
        else:
            self.frame = 0
            if 'idle_' not in self.direction:
                self.direction = 'idle_' + self.direction
        self.move_to_target()

    def draw(self, screen, offset_x, offset_y):
        iso_x, iso_y = cart_to_iso(self.cart_x, self.cart_y)
        screen.blit(self.animations[self.direction][self.frame], (iso_x + offset_x, iso_y + offset_y - CHARACTER_HEIGHT // 2))

class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.stats = {
            'str': 0,
            'def': 0,
            'acc': 0,
            'hp': 5
        }

def generate_map():
    map_width = 20
    map_height = 15
    game_map = [[None for _ in range(map_width)] for _ in range(map_height)]

    grass_tile = tile_sheet.subsurface(pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE))
    road_tile = tile_sheet.subsurface(pygame.Rect(TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
    water_tile = tile_sheet.subsurface(pygame.Rect(2 * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
    building_tile = tile_sheet.subsurface(pygame.Rect(3 * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
    tree_tile = tile_sheet.subsurface(pygame.Rect(4 * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))

    for y in range(map_height):
        for x in range(map_width):
            if (x + y) % 2 == 0:
                game_map[y][x] = grass_tile
            elif (x + y) % 3 == 0:
                game_map[y][x] = road_tile
            elif (x + y) % 5 == 0:
                game_map[y][x] = water_tile
            else:
                game_map[y][x] = grass_tile

    return game_map

def draw_map(game_map, offset_x, offset_y):
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile:
                iso_x, iso_y = cart_to_iso(x, y)
                screen.blit(tile, (iso_x + offset_x, iso_y + offset_y))

def roll_d20():
    return random.randint(1, 20)

def attack(attacker, defender):
    attack_roll = roll_d20() + attacker.stats['str']
    defense_roll = roll_d20() + defender.stats['def']
    damage = max(0, attack_roll - defense_roll)
    defender.stats['hp'] -= damage

player = Character(SCREEN_WIDTH // (2 * ISO_TILE_WIDTH), SCREEN_HEIGHT // (2 * ISO_TILE_HEIGHT))
enemies = [Enemy(random.randint(0, 19), random.randint(0, 14)) for _ in range(5)]

game_map = generate_map()

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
                    break
            if not current_target:
                player.target_pos = (cart_x, cart_y)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.move(0, -1)
    if keys[pygame.K_s]:
        player.move(0, 1)
    if keys[pygame.K_a]:
        player.move(-1, 0)
    if keys[pygame.K_d]:
        player.move(1, 0)

    iso_x, iso_y = cart_to_iso(player.cart_x, player.cart_y)
    offset_x = SCREEN_WIDTH // 2 - iso_x
    offset_y = SCREEN_HEIGHT // 2 - iso_y

    draw_map(game_map, offset_x, offset_y)
    player.draw(screen, offset_x, offset_y)

    for enemy in enemies:
        if enemy.stats['hp'] > 0:
            enemy.draw(screen, offset_x, offset_y)
        else:
            enemies.remove(enemy)
            if current_target == enemy:
                current_target = None

    if current_target:
        attack(player, current_target)
        if current_target.stats['hp'] <= 0:
            current_target = None

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()