import pygame
from queue import PriorityQueue

def cart_to_iso(cart_x, cart_y):
    iso_x = (cart_x - cart_y) * 64 // 2
    iso_y = (cart_x + cart_y) * 32 // 2
    return iso_x, iso_y

def iso_to_cart(iso_x, iso_y):
    cart_x = (iso_x // (64 // 2) + iso_y // (32 // 2)) // 2
    cart_y = (iso_y // (32 // 2) - iso_x // (64 // 2)) // 2
    return cart_x, cart_y

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, grid):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = PriorityQueue()
    oheap.put((fscore[start], start))

    while not oheap.empty():
        current = oheap.get()[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + 1

            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]):
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
            else:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap.queue]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                oheap.put((fscore[neighbor], neighbor))

    return []

class Character:
    def __init__(self, x, y, sprite_path):
        self.cart_x = x
        self.cart_y = y
        self.speed = 0.1
        self.frame = 0
        self.direction = 'down'
        self.animations = self.load_animations(sprite_path)
        self.path = []
        self.is_moving = False
        self.animation_delay = 0
        self.stats = {
            'str': 1,
            'def': 1,
            'acc': 1,
            'hp': 10
        }

    def load_animations(self, sprite_path):
        sprite_sheet = pygame.image.load(sprite_path)
        sprite_sheet_width, sprite_sheet_height = sprite_sheet.get_size()
        columns = 11
        rows = 2
        CHARACTER_WIDTH = sprite_sheet_width // columns
        CHARACTER_HEIGHT = sprite_sheet_height // rows

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

    def move_to_target(self):
        if self.path:
            next_pos = self.path.pop(0)
            dx = next_pos[0] - self.cart_x
            dy = next_pos[1] - self.cart_y
            self.cart_x = next_pos[0]
            self.cart_y = next_pos[1]

            if dx > 0:
                self.direction = 'right'
            elif dx < 0:
                self.direction = 'left'
            elif dy > 0:
                self.direction = 'down'
            elif dy < 0:
                self.direction = 'up'

            self.is_moving = True
        else:
            self.is_moving = False

    def update(self):
        if self.is_moving:
            self.animation_delay += 1
            if self.animation_delay % 10 == 0:
                self.frame = (self.frame + 1) % len(self.animations[self.direction])
        else:
            self.frame = 0
            if 'idle_' not in self.direction:
                self.direction = 'idle_' + self.direction
        self.move_to_target()

    def draw(self, screen, offset_x, offset_y):
        iso_x, iso_y = cart_to_iso(self.cart_x, self.cart_y)
        CHARACTER_WIDTH, CHARACTER_HEIGHT = self.animations[self.direction][self.frame].get_size()
        screen.blit(self.animations[self.direction][self.frame], (iso_x + offset_x, iso_y + offset_y - CHARACTER_HEIGHT // 2))

class Enemy(Character):
    def __init__(self, x, y, sprite_path):
        super().__init__(x, y, sprite_path)
        self.stats = {
            'str': 0,
            'def': 0,
            'acc': 0,
            'hp': 5
        }