import pygame
from asset_loader import load_image


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
        self.anim_time = 0.3
        self.now_time = 0
        self.dir = 'Right'
        self.image = self.images[self.ind]
        self.rect = self.images[0].get_rect()
        self.rect.left = x
        self.rect.top = y
        self.last = self.rect.copy()

    def update(self, key):
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
            self.rect.top -= 10
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.top += 10
        if key[pygame.K_s]:
            self.images = load_image("Front", self.SPRITES_WIDTH, self.SPRITES_HEIGHT)
            self.image = self.images[self.ind]
            self.anim_time = 0.3
            self.dir = ""
            self.rect.top += 10
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.top -= 10
        if key[pygame.K_a]:
            self.images = load_image("Left", self.SPRITES_WIDTH, self.SPRITES_HEIGHT)
            self.image = self.images[self.ind]
            self.anim_time = 0.3
            self.dir = "Left"
            self.rect.left -= 10
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.left += 10
        if key[pygame.K_d]:
            self.images = load_image("Right", self.SPRITES_WIDTH, self.SPRITES_HEIGHT)
            self.image = self.images[self.ind]
            self.anim_time = 0.3
            self.dir = "Right"
            self.rect.left += 10
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.left -= 10
        self.now_time += 30 / 1000


class Walls(Sprite):

    def __init__(self, x, y, SPRITES_WIDTH, SPRITES_HEIGHT):
        super().__init__(walls)
        self.image = pygame.transform.scale(pygame.image.load("assets\\Wall.png"),
                                            (SPRITES_WIDTH, SPRITES_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self):
        pass


user, walls = SpriteGroup(), SpriteGroup()
