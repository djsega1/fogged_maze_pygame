import pygame


def load_image(image, SPRITES_WIDTH, SPRITES_HEIGHT):
    images = list()
    for i in range(1, 5):
        images.append(pygame.transform.scale(pygame.image.load(f"data\\Bryce{image}{i}.png"),
                                             (SPRITES_WIDTH, SPRITES_HEIGHT)))
    return images


def get_font(size):
    return pygame.font.Font("data\\font.ttf", size)
