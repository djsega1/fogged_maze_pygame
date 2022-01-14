import pygame
import csv
from math import ceil

COEF_X, COEF_Y = 0.05, 0.08
SCREEN = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
WIDTH, HEIGHT = SCREEN.get_size()
SPRITES_WIDTH, SPRITES_HEIGHT = WIDTH * COEF_X, HEIGHT * COEF_Y


# Класс Монтгомери
class Monty(pygame.sprite.Sprite):
    image = pygame.image.load("data\\BryceRight1.png")
    image = pygame.transform.scale(image, (SPRITES_WIDTH, SPRITES_HEIGHT))
    rect = image.get_rect()

    def __init__(self, *group):
        super().__init__(*group)

    def update(self):
        pass


class Walls(pygame.sprite.Sprite):
    image = pygame.image.load("data\\Wall.png")
    image = pygame.transform.scale(image, (SPRITES_WIDTH, SPRITES_HEIGHT))
    rect = image.get_rect()

    def __init__(self, *group):
        super().__init__(*group)

    def update(self):
        pass


# Запуск игры
def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    all_sprites = pygame.sprite.Group()
    player = Monty()
    walls = list()
    # стены по периметру
    for i in range(ceil(WIDTH / SPRITES_WIDTH)):
        wall = Walls(all_sprites)
        wall.rect.left = i * SPRITES_WIDTH
        walls.append(wall)
        wall = Walls(all_sprites)
        wall.rect.left = i * SPRITES_WIDTH
        wall.rect.top = HEIGHT - SPRITES_HEIGHT
        walls.append(wall)
    for i in range(ceil(HEIGHT / SPRITES_HEIGHT)):
        wall = Walls(all_sprites)
        wall.rect.top = i * SPRITES_HEIGHT
        walls.append(wall)
        wall = Walls(all_sprites)
        wall.rect.left = WIDTH - SPRITES_WIDTH
        wall.rect.top = i * SPRITES_HEIGHT
        walls.append(wall)
    # --
    all_sprites.add(player)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            player.rect.top -= 10
        if key[pygame.K_s]:
            player.rect.top += 10
        if key[pygame.K_a]:
            player.rect.left -= 10
        if key[pygame.K_d]:
            player.rect.left += 10
        SCREEN.fill((0, 0, 0))
        all_sprites.draw(SCREEN)
        pygame.event.pump()
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
