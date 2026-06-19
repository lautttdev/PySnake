import pygame
from screen import *
from pathlib import Path

SPRITESHEET_PATH = Path("Resources") / "sprites" / "snake.png"

class Spritesheet:
    def __init__(self):
        self.sheet = pygame.image.load(SPRITESHEET_PATH).convert_alpha()
    
    def get_sprite(self, col, row):
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        sprite.set_colorkey("black")

        sprite.blit(
            self.sheet,
            (0, 0),
            (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )

        sprite = pygame.transform.scale(sprite, (SCALED_TILE_SIZE, SCALED_TILE_SIZE))
    
        return sprite

SPRITESHEET = Spritesheet()