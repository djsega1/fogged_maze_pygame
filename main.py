import pygame
import csv

COEF_X, COEF_Y = 0.05, 0.08
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
    wall = Walls()
    all_sprites.add(player, wall)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            player.rect.top -= 10
        if key[pygame.K_DOWN]:
            player.rect.top += 10
        if key[pygame.K_LEFT]:
            player.rect.left -= 10
        if key[pygame.K_RIGHT]:
            player.rect.left += 10
        pygame.event.pump()
        SCREEN.fill((0, 0, 0))
        all_sprites.draw(SCREEN)
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
