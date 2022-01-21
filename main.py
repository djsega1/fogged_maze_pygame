import pygame
import csv


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


def load_image(image):
    images = list()
    for i in range(1, 5):
        images.append(pygame.transform.scale(pygame.image.load(f"data\\Bryce{image}{i}.png"),
                                             (SPRITES_WIDTH, SPRITES_HEIGHT)))
    return images


COEF_X, COEF_Y = 0.05, 0.08
SCREEN = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
WIDTH, HEIGHT = SCREEN.get_size()
SPRITES_WIDTH, SPRITES_HEIGHT = WIDTH * COEF_X, HEIGHT * COEF_Y
user, walls = SpriteGroup(), SpriteGroup()


class Monty(Sprite):

    def __init__(self, x, y):
        super().__init__(user)
        self.images = load_image("right")
        self.ind = 0
        self.image = self.images[self.ind]
        self.rect = self.images[0].get_rect()
        self.rect.left = x
        self.rect.top = y
        self.last = self.rect.copy()

    def update(self, key):
        self.last = self.rect.copy()
        if key[pygame.K_w]:
            self.images = load_image("Back")
            self.image = self.images[self.ind]
            self.ind = (self.ind + 1) % 3
            self.rect.top -= 10
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.top += 10
        if key[pygame.K_s]:
            self.images = load_image("Front")
            self.image = self.images[self.ind]
            self.ind = (self.ind + 1) % 3
            self.rect.top += 10
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.top -= 10
        if key[pygame.K_a]:
            self.images = load_image("Left")
            self.image = self.images[self.ind]
            self.ind = (self.ind + 1) % 3
            self.rect.left -= 10
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.left += 10
        if key[pygame.K_d]:
            self.images = load_image("Right")
            self.image = self.images[self.ind]
            self.ind = (self.ind + 1) % 3
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
