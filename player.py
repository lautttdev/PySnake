import pygame
from screen import SCALED_TILE_SIZE
from spritesheet import Spritesheet
from matrix import MAP


def check_is_alive(func):
    def wrapper(self, *args, **kwargs):
        if self.is_alive:
            return func(self, *args, **kwargs)
    
    return wrapper


class Player(pygame.sprite.Sprite):
    max_length = 483

    initial_pos = [
            (11, 11),
            (10, 11),
            (9, 11)
        ]
    
    initial_length = 3


    def __init__(self, player_group: pygame.sprite.Group, walls_group, food_group, skin, screen: pygame.Surface):
        self.player_group = player_group
        self.walls_group = walls_group
        self.food_group = food_group
        self.screen = screen

        self.spritesheet = Spritesheet()
        self.delta = 0

        self.skin = skin
        self.skin_fix = 0

        match self.skin:
            case 1: self.skin_fix = 0
            case 2: self.skin_fix = 3
            case 3: self.skin_fix = 4

        self.head_sprites = {
            "up": self.spritesheet.get_sprite(1, self.skin_fix),
            "left": self.spritesheet.get_sprite(2, self.skin_fix),
            "down": self.spritesheet.get_sprite(3, self.skin_fix),
            "right": self.spritesheet.get_sprite(4, self.skin_fix)
        }

        self.body_sprite = self.spritesheet.get_sprite(5, self.skin_fix)

        self.direction = "right"
        self.direction_x, self.direction_y = 0, 0
        self.last_direction = self.direction

        self.new_pos = None

        self.length = self.initial_length

        self.body = []
        self.build_body()

        self.is_alive = True

        self.body_pos = self.initial_pos.copy()


    def build_body(self):
        for part in range(self.length):
            self.body.append(self.head_sprites.get(self.direction) if part == 0 else self.body_sprite)


    @check_is_alive
    def check_collisions(self):
        if self.new_pos is None:
            return

        for food in self.food_group:
            if self.length >= self.max_length:
                return self.win()

            if self.new_pos == food.current_pos:
                self.body_pos.insert(0, self.new_pos)
                self.body.append(self.body_sprite)
                self.length += 1
                food.spawn()
                return


        if MAP[self.new_pos[1]][self.new_pos[0]] in ("W", "U", "L", "R", "D") or self.new_pos in self.body_pos:
            return self.lose()


        self.body_pos.insert(0, self.new_pos)
        self.body_pos.pop()
    

    @check_is_alive
    def move(self):
        self.direction = self.last_direction

        match self.direction:
            case "up": self.direction_x, self.direction_y = 0, -1
            case "down": self.direction_x, self.direction_y = 0, 1
            case "left": self.direction_x, self.direction_y = -1, 0
            case "right": self.direction_x, self.direction_y = 1, 0

        head_x, head_y = self.body_pos[0]
        self.new_pos = (
            head_x + self.direction_x,
            head_y + self.direction_y
        )
    

    def restart(self):
        self.is_alive = True
        self.length = self.initial_length
        self.body_pos = self.initial_pos.copy()

        self.direction = "right"
        self.last_direction = "right"

        self.new_pos = None

        self.body.clear()
        self.build_body()

        for i, part in enumerate(reversed(self.body)):
            part.set_alpha(255)
            self.screen.blit(part, (self.body_pos[i][0] * SCALED_TILE_SIZE, self.body_pos[i][1] * SCALED_TILE_SIZE))


    def win(self):
        print("UR THE BIGGEST AND FATTEST SNAKE IN THE ENTIRE WORLD!!!")
        print("Press SPACE to Restart")
        self.is_alive = False


    def lose(self):
        self.is_alive = False
        print("-" * 20, "\n", "Press SPACE to Restart.")

        for part in range(self.length):
            body_part = (self.head_sprites.get(self.direction) if part == 0 else self.body[part])
            self.screen.blit(body_part, (self.body_pos[part][0] * SCALED_TILE_SIZE, self.body_pos[part][1] * SCALED_TILE_SIZE))
        
        for i, part in enumerate(reversed(self.body)):
            part.set_alpha(0)
            self.screen.blit(part, (self.body_pos[i][0] * SCALED_TILE_SIZE, self.body_pos[i][1] * SCALED_TILE_SIZE))

    
    #@check_is_alive
    def draw_parts(self):
        for part in range(self.length):
            body_part = (self.head_sprites.get(self.direction) if part == 0 else self.body[part])
            self.screen.blit(body_part, (self.body_pos[part][0] * SCALED_TILE_SIZE, self.body_pos[part][1] * SCALED_TILE_SIZE))
    

    @check_is_alive
    def get_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP) and self.direction != "down":
                self.last_direction = "up"

            elif event.key in (pygame.K_s, pygame.K_DOWN) and self.direction != "up":
                self.last_direction = "down"

            elif event.key in (pygame.K_a, pygame.K_LEFT) and self.direction != "right":
                self.last_direction = "left"

            elif event.key in (pygame.K_d, pygame.K_RIGHT) and self.direction != "left":
                self.last_direction = "right"