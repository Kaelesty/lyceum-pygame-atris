import pygame
from menu_painter import MenuPainter

# game stats:
# omm - on main menu
# wfa - wait for activity
# gmc - game mode choosing

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


if __name__ == '__main__':
    fps = 30
    clock = pygame.time.Clock()
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    running = True
    pygame.display.set_caption('Atris - Main')
    main_status = 'wfa'
    mp = MenuPainter(screen)
    while running:
        screen.fill((0, 0, 0))
        if main_status == 'omm':
            mp.draw_main_menu()
        if main_status == "wfa":
            mp.draw_waiting()
        if main_status == 'gmc':
            mp.draw_selector()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_status == "wfa":
                    if check_click(event.pos[0], event.pos[1], 480, 620, 320, 64):
                        main_status = "omm"
                        mp.init_main_menu()
                        screen.fill((100, 0, 100))
                elif main_status == "omm":
                    group = list(mp.buttons)
                    for i in range(len(list(mp.buttons))):
                        if group[i].rect.collidepoint(event.pos):
                            group[i].change_stat('ps')
                    sprites = pygame.sprite.Group()
                    for elem in group:
                        sprites.add(elem)
                    mp.buttons = sprites
            elif event.type == pygame.MOUSEBUTTONUP:
                group = list(mp.buttons)
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
                if mp.buttons != False and main_status == "omm":
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
                    mp.buttons.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
