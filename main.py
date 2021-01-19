import pygame
from menu_painter import MenuPainter


# game stats:
# omm - on main menu
# wfa - wait for activity
# gmc - game mode choosing
# ig-cl - in game classic
# ig-bt - in game btris
# ig-wt - in game welltris

def check_click(x_pos, y_pos, x_left, y_top, width, height):
    if x_left <= x_pos <= x_left + width:
        if y_top <= y_pos <= y_top + height:
            return True
    return False


def button_reaction(name):
    global main_status, mp
    if name == 'play':
        main_status = 'gmc'
        mp.init_selector()
    elif name == 'classic':
        main_status = 'ig-cl'
        mp.init_classic(name)
    elif name == "normal":
        main_status = 'ig-cl'
        mp.init_classic(name)
    elif name == "hard":
        main_status = 'ig-cl'
        mp.init_classic(name)
    elif name == "btris_20":
        main_status = 'ig-bt'
        mp.init_btris(20)
    elif name == "btris_10":
        main_status = 'ig-bt'
        mp.init_btris(10)
    elif name == "btris_5":
        main_status = 'ig-bt'
        mp.init_btris(5)
    elif name == "_easy":
        main_status = "ig-wt"
        mp.init_welltris("easy")


if __name__ == '__main__':
    fps = 30
    clock = pygame.time.Clock()
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    running = True
    pygame.display.set_caption('Atris')
    main_status = 'wfa'
    mp = MenuPainter(screen)
    following_bt = False
    while running:
        screen.fill((0, 0, 0))
        if main_status == 'omm':
            mp.draw_main_menu()
        elif main_status == "wfa":
            mp.draw_waiting()
        elif main_status == 'gmc':
            mp.draw_selector()
        elif main_status == 'ig-cl':
            mp.draw_and_step()
            fps = 5
        elif main_status == "ig-bt":
            mp.btris.draw_self()
            if following_bt:
                mp.btris.update(pygame.mouse.get_pos())
        elif main_status == "ig-wt":
            mp.draw_and_step_w()
            fps = 5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_status == "wfa":
                    if check_click(event.pos[0], event.pos[1], 480, 620, 320, 64):
                        main_status = "omm"
                        mp.init_main_menu()
                        screen.fill((100, 0, 100))
                elif main_status in ["omm", "gmc"]:
                    group = list(mp.buttons)
                    for i in range(len(list(mp.buttons))):
                        if group[i].rect.collidepoint(event.pos):
                            group[i].change_stat('ps')
                    sprites = pygame.sprite.Group()
                    for elem in group:
                        sprites.add(elem)
                    mp.buttons = sprites
                elif main_status == "ig-bt":
                    if mp.btris.catch_mbd(event.pos):
                        following_bt = True
            elif event.type == pygame.KEYDOWN:
                if main_status == "ig-cl":
                    if event.key != 120:
                        mp.tetris.catch(event)
                    else:
                        if mp.tetris.game == 0:
                            mp.tetris.terminate()
                            main_status = "gmc"
                            mp.tetris = 0
                            mp.init_selector()
                            fps = 30
                elif main_status == "ig-bt":
                    if event.key != 120:
                        mp.btris.catch(event)
                    else:
                        mp.btris.terminate()
                        main_status = "gmc"
                        mp.btris = 0
                        mp.init_selector()
                        fps = 30
                elif main_status == "ig-wt":
                    mp.welltris.catch(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if main_status == "ig-bt":
                    if following_bt:
                        mp.btris.catch_mbu(event.pos)
                        following_bt = False
                else:
                    try:
                        group = list(mp.buttons)
                    except TypeError:
                        break
                    for i in range(len(list(mp.buttons))):
                        if group[i].stat == 'ps':
                            if group[i].rect.collidepoint(event.pos):
                                group[i].change_stat('st')
                                button_reaction(group[i].name)
                            else:
                                group[i].change_stat('st')
                                sprites = pygame.sprite.Group()
                                for elem in group:
                                    sprites.add(elem)
                                mp.buttons = sprites
            else:
                if mp.buttons != False and main_status in ['omm', 'gmc']:
                    group = list(mp.buttons)
                    for i in range(len(group)):
                        if group[i].rect.collidepoint(pygame.mouse.get_pos()):
                            group[i].change_stat("uw")
                        else:
                            group[i].change_stat("st")
                    btns = pygame.sprite.Group()
                    for elem in group:
                        btns.add(elem)
                    mp.upload_buttons(btns)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
