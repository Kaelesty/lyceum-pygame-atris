import pygame

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
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
