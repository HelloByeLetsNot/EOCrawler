import pygame
from movement import cart_to_iso

def generate_map(tile_sheet, map_width, map_height):
    game_map = [[None for _ in range(map_width)] for _ in range(map_height)]

    grass_tile = tile_sheet.subsurface(pygame.Rect(0, 0, 32, 32))
    road_tile = tile_sheet.subsurface(pygame.Rect(32, 0, 32, 32))
    water_tile = tile_sheet.subsurface(pygame.Rect(64, 0, 32, 32))
    building_tile = tile_sheet.subsurface(pygame.Rect(96, 0, 32, 32))
    tree_tile = tile_sheet.subsurface(pygame.Rect(128, 0, 32, 32))

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

def draw_map(game_map, offset_x, offset_y, screen):
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile:
                iso_x, iso_y = cart_to_iso(x, y)
                screen.blit(tile, (iso_x + offset_x, iso_y + offset_y))