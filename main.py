import pygame
import paint_main_menu

# game stats:
# omm - on main menu

if __name__ == '__main__':
    fps = 30
    clock = pygame.time.Clock()
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    running = True
    pygame.display.set_caption('Atris - Main')
    main_status = 'omm'
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if main_status == 'omm':
            paint_main_menu()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
