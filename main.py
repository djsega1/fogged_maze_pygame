import pygame
import sys
from buttons import *
from sprites import *
from asset_loader import *
from maps import levels

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
        images = load_image("Idle", int(HEIGHT * 0.4), int(HEIGHT * 0.4))
        image = images[ind]
        MENU_TEXT = get_font(int(0.07 * HEIGHT)).render("Fogged Maze", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(topleft=(int(WIDTH * 0.1), int(WIDTH * 0.125)))
        PLAY_BUTTON = Button(image=None, pos=(int(WIDTH * 0.2), int(WIDTH * 0.25)),
                             text_input="PLAY", font=get_font(int(0.06 * HEIGHT)),
                             base_color="#694916", hovering_color="#bd8428")
        # OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
        #                         text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(int(WIDTH * 0.2), int(WIDTH * 0.35)),
                             text_input="QUIT", font=get_font(int(0.06 * HEIGHT)),
                             base_color="#694916", hovering_color="#bd8428")
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(image, (int(WIDTH * 0.65), MENU_RECT.top + MENU_RECT.h))
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
    player = Monty(1, 1, SPRITES_WIDTH, SPRITES_HEIGHT)
    lvl = levels[1]
    for row in range(len(lvl)):
        for col in range(len(lvl[row])):
            if lvl[row][col]:
                Wall(col, row, SPRITES_WIDTH, SPRITES_HEIGHT, player.x, player.y)
            # elif not lvl[row][col]:
            #     Road(col, row, SPRITES_WIDTH, SPRITES_HEIGHT, player.x, player.y)
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                user.empty()
                walls.empty()
                return
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


if __name__ == '__main__':
    main_menu()

# TODO Arseniy: CSV
# TODO Overall: Level Creator, Few Levels
