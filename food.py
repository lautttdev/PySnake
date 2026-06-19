import pygame
from spritesheet import Spritesheet
from random import choice
from matrix import MAP
from screen import SCALED_TILE_SIZE

zero_positions = []

for row, valuey in enumerate(MAP):
    for col, valuex in enumerate(valuey):
        if valuex == 0:
            zero_positions.append((col, row))


class Food(pygame.sprite.Sprite):
    spritesheet = Spritesheet()

    foods_sprites = [
        spritesheet.get_sprite(6, 0),
        spritesheet.get_sprite(6, 1),
        spritesheet.get_sprite(6, 3),
        spritesheet.get_sprite(7, 3),
        spritesheet.get_sprite(6, 4), 
    ]

    def __init__(self, food_group, player):
        pygame.sprite.Sprite.__init__(self)

        self.image = choice(self.foods_sprites)
        self.rect = self.image.get_rect()

        self.food_group = food_group
        self.food_group.add(self)
        self.player = player

        self.current_pos = None
    

    def spawn(self):
        spawn_pos = choice(zero_positions)

        if spawn_pos not in self.player.body_pos:
            self.current_pos = spawn_pos

            spawn_pos_x, spawn_pos_y = spawn_pos[0] * SCALED_TILE_SIZE, spawn_pos[1] * SCALED_TILE_SIZE

            self.rect.topleft = (spawn_pos_x, spawn_pos_y)
            self.image = choice(self.foods_sprites)
            return

        self.spawn()
