import pygame
import sys
from buttons import *
from buffs import *
from sprites import *
from asset_loader import *
from PIL import Image
from csv import reader, writer
import os

pygame.init()
with open("data.csv", "r+") as csvfile:
    for i in reader(csvfile, delimiter=";"):
        HARD = int(i[1])
        HIGH = int(i[0])
        break


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
        if HARD:
            base_color, hovering_color = "Red", "White"
        else:
            base_color, hovering_color = "White", "Red"
        MODE_BUTTON = Button(image=None, pos=(int(WIDTH * 0.55), int(HEIGHT * 0.8)),
                             text_input="HARD MODE", font=get_font(int(0.06 * HEIGHT)),
                             base_color=base_color, hovering_color=hovering_color)
        QUIT_BUTTON = Button(image=None, pos=(int(WIDTH * 0.2), int(WIDTH * 0.35)),
                             text_input="QUIT", font=get_font(int(0.06 * HEIGHT)),
                             base_color="#694916", hovering_color="#bd8428")
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(image, (int(WIDTH * 0.65), MENU_RECT.top + MENU_RECT.h))
        for button in [PLAY_BUTTON, QUIT_BUTTON, MODE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if MODE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    hard()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    end()
        now_time += 30 / 1000
        pygame.display.flip()


def hard():
    global HARD
    if HARD:
        HARD = 0
    else:
        HARD = 1


def exit_to_main():
    user.empty()
    walls.empty()
    buffs.empty()
    SCREEN.set_clip((0, 0, WIDTH, HEIGHT))
    pygame.mixer.music.load("assets\\main.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1)


def black_screen():
    s = pygame.Surface((WIDTH, HEIGHT))
    s.fill((0, 0, 0))
    for opacity in range(0, 255, 20):
        s.set_alpha(opacity)
        SCREEN.blit(s, (0, 0))
        pygame.display.flip()
        pygame.time.delay(100)


# Запуск уровня
def play():
    clock = pygame.time.Clock()
    player = Monty(1, 1, SPRITES_WIDTH, SPRITES_HEIGHT)
    black_screen()
    user_progress = 2
    progress_bar_sur = pygame.Surface(SCREEN.get_size())
    lvl_file = Image.open(f'mazes\\maze{user_progress}.png')
    lvl_crop = lvl_file.crop((0, 0, 100, 100))
    x, y = lvl_crop.size
    lvl = lvl_crop.load()
    cnt = 0
    for row in range(y):
        for col in range(x):
            print(lvl[row, col])
            if lvl[row, col][:3] == (0, 0, 0):
                Wall(row, col, SPRITES_WIDTH, SPRITES_HEIGHT, player.x, player.y)
            elif lvl[row, col][:3] == (255, 255, 255):
                Road(row, col, SPRITES_WIDTH, SPRITES_HEIGHT, player.x, player.y)
            elif lvl[row, col][:3] == (255, 0, 0):
                BootsBuff(row, col, SPRITES_WIDTH, SPRITES_HEIGHT, player, "boots")
            elif lvl[row, col][:3] == (0, 255, 0):
                LanternBuff(row, col, SPRITES_WIDTH, SPRITES_HEIGHT, player, "lantern")
            elif lvl[row, col][:3] == (0, 0, 255):
                Exit(row, col, SPRITES_WIDTH, SPRITES_WIDTH, player, 'portal1')
            cnt += 1
            pygame.draw.rect(progress_bar_sur, (128, 128, 128),
                             pygame.Rect(HEIGHT - 250, WIDTH - 25, WIDTH - 200, 250), 1)
            pygame.draw.rect(progress_bar_sur, (0, 255, 0),
                             pygame.Rect(100, HEIGHT - 250, int(((WIDTH - 200) / 10000) * cnt), 100))
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
                end()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                black_screen()
                exit_to_main()
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
        if HARD:
            buffs.empty()
        SCREEN.fill((0, 0, 0))
        buffs.draw(SCREEN)
        user.draw(SCREEN)
        walls.draw(SCREEN)
        if player.escaped:
            black_screen()
            exit_to_main()
            return
        pygame.display.flip()


def end():
    os.remove("data.csv")
    with open("data.csv", "w") as csvfile:
        writer(csvfile, delimiter=";").writerow([HIGH, HARD])
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_menu()

# TODO Overall: Few Levels, CSV, Scoreboard, Hard Mode
