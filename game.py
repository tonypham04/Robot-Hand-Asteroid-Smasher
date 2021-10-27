import pygame
import sys

def main():
    """The main method runs when the script is run and houses the game loop and variables for the game."""
    pygame.init()
    screen = pygame.display.set_mode((480, 320))
    gameview = pygame.Surface((int(screen.get_width() / 2), int(screen.get_height() / 2)))
    pygame.display.set_caption('Robot Hand Asteroid Smasher')
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        gameview.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        scaled_gameview = pygame.transform.scale(gameview, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_gameview, (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    main()