import pygame
from screen import *

pygame.init()
SCREEN = pygame.display.set_mode(SIZE)

from matrix import MAP
from player import Player
from food import Food

from tiles import *

CLOCK = pygame.time.Clock()
DELTA = 0
FRAME_TIME = 0

PLAYER_GROUP = pygame.sprite.Group()
WALL_GROUP = pygame.sprite.Group()
FOOD_GROUP = pygame.sprite.Group()

player = Player(PLAYER_GROUP, WALL_GROUP, FOOD_GROUP, 2, SCREEN)
food = Food(FOOD_GROUP, player)

in_process = True


def generate_terrain():
    SCREEN.fill("black")

    for row, y in enumerate(MAP):
        for col, x in enumerate(y):
            match x:
                case "W":
                    tile_sprite = WALL_SPRITE
                case "U":
                    tile_sprite = UP_WALL_SPRITE
                case "L":
                    tile_sprite = LEFT_WALL_SPRITE
                case "R":
                    tile_sprite = RIGHT_WALL_SPRITE
                case "D":
                    tile_sprite = DOWN_WALL_SPRITE
                case 0:
                    continue

            tile_pos = (col, row)
            coord_pos = (col * SCALED_TILE_SIZE, row * SCALED_TILE_SIZE)

            tile = Tile(tile_sprite, coord_pos, tile_pos)

            WALL_GROUP.add(tile)


def draw_all():
    SCREEN.fill("black")
    WALL_GROUP.draw(SCREEN)
    FOOD_GROUP.draw(SCREEN)
    player.draw_parts()


def next_frame():
    global FRAME_TIME
    FRAME_TIME += DELTA

    if FRAME_TIME >= 1:
        player.move()
        player.check_collisions()
        

        FRAME_TIME = 0


def on_ready():
    generate_terrain()
    food.spawn()

on_ready()


while in_process:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_process = False

        player.get_input(event)

        if not player.is_alive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.restart()
                    food.spawn()


    next_frame()
    draw_all()
    
    DELTA = CLOCK.tick(60) / 300
    pygame.display.flip()

pygame.quit()