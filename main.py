import pygame
import csv
from math import ceil


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


COEF_X, COEF_Y = 0.05, 0.08
SCREEN = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
WIDTH, HEIGHT = SCREEN.get_size()
SPRITES_WIDTH, SPRITES_HEIGHT = WIDTH * COEF_X, HEIGHT * COEF_Y
user, walls = SpriteGroup(), SpriteGroup()


class Monty(Sprite):

    def __init__(self, x, y):
        super().__init__(user)
        self.image = pygame.transform.scale(pygame.image.load("data\\BryceRight1.png"),
                                            (SPRITES_WIDTH, SPRITES_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.last = self.rect.copy()

    def update(self, key):
        self.last = self.rect.copy()
        if key[pygame.K_w]:
            self.rect.top -= 10
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.top += 10
        if key[pygame.K_s]:
            self.rect.top += 10
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.top -= 10
        if key[pygame.K_a]:
            self.rect.left -= 10
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.left += 10
        if key[pygame.K_d]:
            self.rect.left += 10
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.left -= 10


class Walls(Sprite):

    def __init__(self, x, y):
        super().__init__(walls)
        self.image = pygame.transform.scale(pygame.image.load("data\\Wall.png"),
                                            (SPRITES_WIDTH, SPRITES_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self):
        pass


# Запуск игры
def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    Monty(500, 500)
    Walls(200, 200)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        user.update(pygame.key.get_pressed())
        pygame.event.pump()
        SCREEN.fill((0, 0, 0))
        user.draw(SCREEN)
        walls.draw(SCREEN)
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
