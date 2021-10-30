import pygame
import sys
import os
import random

# Platform independent paths
main_dir = os.path.split(os.path.abspath(__file__))[0]
img_dir = os.path.join(main_dir, 'images')

def load_image(img_filename: str, colorkey=None) -> pygame.Surface:
    """Loads an image from an image file and applies transparent color if applicable. A Surface representation of the image is returned."""
    # Attempt to load the user specified image
    img_location = os.path.join(img_dir, img_filename)
    try:
        img = pygame.image.load(img_location).convert()
    except pygame.error as msg:
        print('Failed to load:', img_filename)
        raise SystemExit(msg)
    # Apply color transparency if applicable
    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        # The pygame.RLEACCEL flag provides better performance on non accelerated displays
        img.set_colorkey(colorkey, pygame.RLEACCEL)
    return img

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """Initialize an instance of the Player class."""
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('player.png', (255, 255, 255))
        self.rect = self.image.get_rect()

    def update(self):
        """Updates the player position based on where the mouse cursor is."""
        pos = pygame.mouse.get_pos()
        # The actual gameview is 1/2 the screen size so divide the mouse coordinates by 2 to account for the 2x scaling
        self.rect.center = (pos[0] / 2, pos[1] / 2)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        """Initialize an instance of the Asteroid class."""
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('asteroid.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.velocity = [random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])]

    def update(self):
        """Moves the asteroid within the game boundaries."""
        # Random movement
        self.rect.move_ip(self.velocity)
        # Check for bounds
        screen_size = pygame.display.get_window_size()
        # Divide x and y of screen size by 2 to get the boundaries prior to scaling up 2x
        x_boundaries = (0, screen_size[0] / 2)
        y_boundaries = (0, screen_size[1] / 2)
        if self.rect.center[0] < x_boundaries[0] or self.rect.center[0] > x_boundaries[1]:
            # Flip the x velocity then move back into the gameview
            self.velocity[0] = -self.velocity[0]
            self.rect.move_ip(self.velocity)
        if self.rect.center[1] < y_boundaries[0] or self.rect.center[1] > y_boundaries[1]:
            self.velocity[1] = -self.velocity[1]
            self.rect.move_ip(self.velocity)

def main():
    """The main method runs when the script is run and houses the game loop and variables for the game."""
    # Initialize game components
    pygame.init()
    screen = pygame.display.set_mode((480, 320))
    gameview = pygame.Surface((int(screen.get_width() / 2), int(screen.get_height() / 2)))
    pygame.display.set_caption('Robot Hand Asteroid Smasher')
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    # Prepare game objects
    player = Player()
    asteroids = []
    asteroids.extend([Asteroid(), Asteroid(), Asteroid()])
    sprites_group = pygame.sprite.RenderPlain((asteroids, player))
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        sprites_group.update()
        gameview.fill((0, 0, 0))
        sprites_group.draw(gameview)
        scaled_gameview = pygame.transform.scale(gameview, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_gameview, (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    main()
# References
# Line by Line Chimp (pygame docs, https://www.pygame.org/docs/tut/ChimpLineByLine.html)
# pygame.Surface.set_colorkey (pygame docs, https://www.pygame.org/docs/ref/surface.html#pygame.Surface.set_colorkey)