import pygame
import sys
from buttons import *
from buffs import *
from sprites import *
from asset_loader import *
from PIL import Image

pygame.init()


# Главное меню
def main_menu():
    ind = 0
    anim_time = 5
    now_time = 0
    pygame.mixer.music.load("assets\\main.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1)
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
    s = pygame.Surface((WIDTH, HEIGHT))
    s.fill((0, 0, 0))
    for opacity in range(0, 255, 20):
        s.set_alpha(opacity)
        SCREEN.blit(s, (0, 0))
        pygame.display.flip()
        pygame.time.delay(100)
    user_progress = 1
    progress_bar_sur = pygame.Surface(SCREEN.get_size())
    lvl_file = Image.open(f'mazes\\maze{user_progress}.png')
    lvl_crop = lvl_file.crop((0, 0, 100, 100))
    x, y = lvl_crop.size
    lvl = lvl_crop.load()
    cnt = 0
    for row in range(y):
        for col in range(x):
            if lvl[row, col] == (0, 0, 0):
                Wall(row, col, SPRITES_WIDTH, SPRITES_HEIGHT, player.x, player.y)
            elif lvl[row, col] == (255, 255, 255):
                Road(row, col, SPRITES_WIDTH, SPRITES_HEIGHT, player.x, player.y)
            elif lvl[row, col] == (255, 0, 0):
                BootsBuff(row, col, SPRITES_WIDTH, SPRITES_HEIGHT, player, "boots")
            elif lvl[row, col] == (0, 255, 0):
                LanternBuff(row, col, SPRITES_WIDTH, SPRITES_HEIGHT, player, "lantern")
            cnt += 1
            # pygame.draw.rect(progress_bar_sur, (255, 255, 255), pygame.Rect(500, 500, 500 * (cnt // 10000), 250))
            pygame.draw.rect(progress_bar_sur, (128, 128, 128), pygame.Rect(500, 500, 500, 250), 1)
            pygame.draw.rect(progress_bar_sur, (0, 255, 0), pygame.Rect(500, 500, int((10000 / 10000) * cnt), 250))
            SCREEN.blit(progress_bar_sur, (0, 0))
            pygame.display.flip()
    SCREEN.fill((0, 0, 0))
    pygame.mixer.music.load("assets\\level.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1)
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                user.empty()
                walls.empty()
                buffs.empty()
                SCREEN.set_clip((0, 0, WIDTH, HEIGHT))
                pygame.mixer.music.load("assets\\main.mp3")
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(loops=-1)
                return
        last_pos = (player.rect.x, player.rect.y)
        user.update(pygame.key.get_pressed())
        buffs.update()
        for i in walls:
            i.rect.topleft = (i.rect.left + (last_pos[0] - player.rect.x), i.rect.top + (last_pos[1] - player.rect.y))
        for i in roads:
            i.rect.topleft = (i.rect.left + (last_pos[0] - player.rect.x), i.rect.top + (last_pos[1] - player.rect.y))
        for i in buffs:
            i.rect.topleft = (i.rect.left + (last_pos[0] - player.rect.x), i.rect.top + (last_pos[1] - player.rect.y))
        player.rect.topleft = (WIDTH // 2 - player.rect.width // 2, HEIGHT // 2 - player.rect.height // 2)
        pygame.event.pump()
        SCREEN.set_clip((player.rect.left - player.vision_x, player.rect.top - player.vision_y,
                         player.rect.width + player.vision_x * 2,
                         player.rect.height + player.vision_y * 2))
        SCREEN.fill((0, 0, 0))
        buffs.draw(SCREEN)
        user.draw(SCREEN)
        walls.draw(SCREEN)
        pygame.display.flip()


if __name__ == '__main__':
    main_menu()

# TODO Overall: Few Levels, CSV, Scoreboard, Hard Mode
