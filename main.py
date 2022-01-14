import pygame
import csv

COEF_X, COEF_Y = 0.05, 0.08
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = SCREEN.get_size()


# Класс Монтгомери
class Monty(pygame.sprite.Sprite):
    image = pygame.image.load("data\\BryceRight1.png")
    image = pygame.transform.scale(image, (WIDTH * COEF_X, HEIGHT * COEF_Y))
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
        pygame.event.pump()
        SCREEN.fill((0, 0, 0))
        all_sprites.draw(SCREEN)
        clock.tick(30)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
