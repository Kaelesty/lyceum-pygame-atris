import pygame
from menu_painter import MenuPainter

# game stats:
# omm - on main menu
# wfa - wait for activity

def check_click(x_pos, y_pos, x_left, y_top, width, height):
    if x_left <= x_pos <= x_left + width:
        if y_top <= y_pos <= y_top + height:
            return True
    return False

if __name__ == '__main__':
    fps = 30
    clock = pygame.time.Clock()
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    running = True
    pygame.display.set_caption('Atris - Main')
    main_status = 'wfa'
    mp = MenuPainter(screen)
    while running:
        if main_status == 'omm':
            mp.draw_main_menu()
        if main_status == "wfa":
            mp.draw_waiting()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_status == "wfa":
                    if check_click(event.pos[0], event.pos[1], 480, 620, 320, 64):
                        main_status = "omm"
                        mp.init_main_menu()
                        screen.fill((100, 0, 100))
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
