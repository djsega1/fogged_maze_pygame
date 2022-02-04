import pygame
from asset_loader import load_image

COEF_X, COEF_Y = 0.05, 0.08
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = SCREEN.get_size()
SPRITES_WIDTH, SPRITES_HEIGHT = 80, 80


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)

    def get_event(self, event):
        pass


class Monty(Sprite):

    def __init__(self, x, y, SPRITES_WIDTH, SPRITES_HEIGHT):
        super().__init__(user)
        self.images = load_image("Right", SPRITES_WIDTH, SPRITES_HEIGHT)
        self.ind = 0
        self.SPRITES_WIDTH = SPRITES_WIDTH
        self.SPRITES_HEIGHT = SPRITES_HEIGHT
        self.escaped = False
        self.mp = 2
        self.boots_pickup = "NO"
        self.lantern_pickup = "NO"
        self.score = 900000
        self.vision_x = self.mp * SPRITES_WIDTH
        self.vision_y = self.mp * SPRITES_HEIGHT
        self.anim_time = 0.3
        self.speed = 10
        self.now_time = 0
        self.x = x * SPRITES_WIDTH
        self.y = y * SPRITES_HEIGHT
        self.dir = 'Right'
        self.image = self.images[self.ind]
        self.rect = self.images[0].get_rect()
        self.rect.topleft = (WIDTH // 2 - self.rect.width // 2, HEIGHT // 2 - self.rect.height // 2)
        self.last = self.rect.copy()

    def update(self, key):
        self.vision_x = self.mp * SPRITES_WIDTH
        self.vision_y = self.mp * SPRITES_HEIGHT
        if self.now_time > self.anim_time:
            self.now_time = 0
            self.ind = (self.ind + 1) % 3
        self.anim_time = 1
        self.images = load_image(f"Idle{self.dir}", self.SPRITES_WIDTH, self.SPRITES_HEIGHT)
        self.image = self.images[self.ind]
        self.last = self.rect.copy()
        if key[pygame.K_w]:
            self.images = load_image("Back", self.SPRITES_WIDTH, self.SPRITES_HEIGHT)
            self.image = self.images[self.ind]
            self.anim_time = 0.3
            self.dir = "Back"
            self.rect.top -= self.speed
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.top += self.speed
        if key[pygame.K_s]:
            self.images = load_image("Front", self.SPRITES_WIDTH, self.SPRITES_HEIGHT)
            self.image = self.images[self.ind]
            self.anim_time = 0.3
            self.dir = ""
            self.rect.top += self.speed
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.top -= self.speed
        if key[pygame.K_a]:
            self.images = load_image("Left", self.SPRITES_WIDTH, self.SPRITES_HEIGHT)
            self.image = self.images[self.ind]
            self.anim_time = 0.3
            self.dir = "Left"
            self.rect.left -= self.speed
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.left += self.speed
        if key[pygame.K_d]:
            self.images = load_image("Right", self.SPRITES_WIDTH, self.SPRITES_HEIGHT)
            self.image = self.images[self.ind]
            self.anim_time = 0.3
            self.dir = "Right"
            self.rect.left += self.speed
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.left -= self.speed
        SCREEN.scroll(10, 10)
        self.now_time += 30 / 1000


class Wall(Sprite):

    def __init__(self, x, y, SPRITES_WIDTH, SPRITES_HEIGHT, player_x, player_y):
        super().__init__(walls)
        self.image = pygame.transform.scale(pygame.image.load("assets\\Wall.png"),
                                            (SPRITES_WIDTH, SPRITES_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH // 2 - self.rect.width // 2 + (x * SPRITES_WIDTH - player_x),
                             HEIGHT // 2 - self.rect.height // 2 + (y * SPRITES_HEIGHT - player_y))

    def update(self):
        pass


class Road(Sprite):
    def __init__(self, x, y, SPRITES_WIDTH, SPRITES_HEIGHT, player_x, player_y):
        super().__init__(roads)
        self.image = pygame.transform.scale(pygame.image.load(f"assets\\Road1.png"),
                                            (SPRITES_WIDTH, SPRITES_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH // 2 - self.rect.width // 2 + (x * SPRITES_WIDTH - player_x),
                             HEIGHT // 2 - self.rect.height // 2 + (y * SPRITES_HEIGHT - player_y))

    def update(self):
        pass


user, walls, roads = SpriteGroup(), SpriteGroup(), SpriteGroup()
