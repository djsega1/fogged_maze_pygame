import pygame
import sys
from buttons import *
from sprites import *
from asset_loader import *

pygame.init()


# Главное меню
def main_menu():
    ind = 0
    anim_time = 5
    now_time = 0
    while True:
        SCREEN.fill((0, 0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        if now_time > anim_time:
            now_time = 0
            ind = (ind + 1) % 3
        images = load_image("Idle", 300, 300)
        image = images[ind]
        MENU_TEXT = get_font(80).render("Fogged Maze", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(topleft=(50, 50))
        PLAY_BUTTON = Button(image=None, pos=(100, 300),
                             text_input="PLAY", font=get_font(60), base_color="#694916", hovering_color="#bd8428")
        # OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
        #                         text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(100, 450),
                             text_input="QUIT", font=get_font(60), base_color="#694916", hovering_color="#bd8428")
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(image, (WIDTH // 1.5, HEIGHT // 6.5))
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                # if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        now_time += 30 / 1000
        pygame.display.flip()


# Запуск уровня
def play():
    clock = pygame.time.Clock()
    player = Monty(SPRITES_WIDTH, SPRITES_HEIGHT)
    Walls(500, 500, SPRITES_WIDTH, SPRITES_HEIGHT)
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        last_pos = (player.rect.x, player.rect.y)
        user.update(pygame.key.get_pressed())
        for i in walls:
            i.rect.topleft = (i.rect.left + (last_pos[0] - player.rect.x), i.rect.top + (last_pos[1] - player.rect.y))
        player.rect.topleft = (WIDTH // 2 - player.rect.width // 2, HEIGHT // 2 - player.rect.height // 2)
        pygame.event.pump()
        SCREEN.fill((0, 0, 0))
        user.draw(SCREEN)
        walls.draw(SCREEN)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main_menu()
