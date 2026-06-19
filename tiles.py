import pygame
from spritesheet import Spritesheet

SPRITESHEET = Spritesheet()

WALL_SPRITE = SPRITESHEET.get_sprite(12, 0)
DOWN_WALL_SPRITE = SPRITESHEET.get_sprite(7, 2)
RIGHT_WALL_SPRITE = SPRITESHEET.get_sprite(8, 2)
LEFT_WALL_SPRITE = SPRITESHEET.get_sprite(9, 2)
UP_WALL_SPRITE = SPRITESHEET.get_sprite(10, 2)

class Tile(pygame.sprite.Sprite):
    def __init__(self, sprite, pos, tile_pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.tile_pos = tile_pos

        