import pygame
import sys
import os
import random
import json

# Platform independent paths
main_dir = os.path.split(os.path.abspath(__file__))[0]
img_dir = os.path.join(main_dir, 'images')
sound_dir = os.path.join(main_dir, 'audio')
font_dir = os.path.join(main_dir, 'font')
data_dir = os.path.join(main_dir, 'data')

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

def load_sound(sound_filename: str):
    """Loads a sound file and returns a corresponding Sound object. If pygame.mixer is not available an instance of a dummy class containing a play method is returned instead."""
    class NoSound:
        """Dummy class used in the event pygame.mixer is not available."""
        def play(self):
            None
    if not pygame.mixer:
        return NoSound()
    sound_location = os.path.join(sound_dir, sound_filename)
    try:
        sound = pygame.mixer.Sound(sound_location)
    except pygame.error as msg:
        print('Failed to load:', sound_filename)
        raise SystemExit(msg)
    return sound

def load_font(font_filename: str, font_size: int) -> pygame.font.Font:
    """Loads a font file and returns a Font object with the specified font and size on success. Returns the default pygame font with user specified size otherwise."""
    font_location = os.path.join(font_dir, font_filename)
    try:
        font = pygame.font.Font(font_location, font_size)
    except:
        font = pygame.font.Font(None, font_size)
    return font

def load_data(data_filename: str, permissions: str):
    """Loads a JSON file and returns a dictionary representation of the JSON file."""
    # Attempt to load the user specified file
    data_location = os.path.join(data_dir, data_filename)
    try:
        with open(data_location, permissions) as file:
            return json.load(file)
    except pygame.error as msg:
        print('Failed to load:', data_filename)
        raise SystemExit(msg)

def save_data(json_data_filename: str, data):
    """Saves the specified data inside the specified JSON file."""
    # Attempt to open the file and write data to it
    data_location = os.path.join(data_dir, json_data_filename)
    with open(data_location, 'w') as f:
        json.dump(data, f)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        """Initialize an instance of the Asteroid class."""
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('asteroid.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        # TODO: Change velocity to be a random float for move variation and decreased likely hood of overlap
        self.velocity = [random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])]
        self.explosion_sound = load_sound('explosion.wav')

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
        # TODO: Add logic to rotate the asteroids

    def explode(self):
        """Plays an explosion sound."""
        # TODO: Visual effect for exploding
        self.explosion_sound.play()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """Initialize an instance of the Player class."""
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('player.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.smashing = False

    def update(self):
        """Updates the player position based on where the mouse cursor is."""
        pos = pygame.mouse.get_pos()
        # The actual gameview is 1/2 the screen size so divide the mouse coordinates by 2 to account for the 2x scaling
        self.rect.center = (pos[0] / 2, pos[1] / 2)

    def smash(self):
        """Changes the player image to that of the robot hand in a clenched fist state."""
        # Change to image of robot hand clenched into a fist
        self.image = load_image('smash.png', (255, 255, 255))
        self.smashing = True

    def unsmash(self):
        """Changes the player image back to it's original state if the player was attempting a smash previously."""
        if self.smashing:
            self.image = load_image('player.png', (255, 255, 255))

def create_asteroids(nun_asteroids: int) -> list[Asteroid]:
    """Returns a list of asteroids containing the specified number of asteroids"""
    asteroids = []
    for i in range(nun_asteroids):
        asteroids.append(Asteroid())
    return asteroids

def has_asteroids(group: pygame.sprite.RenderPlain) -> bool:
    """Returns a bool of whether or not a RenderPlain group has any asteroids in it."""
    return len([obj for obj in group if type(obj) == Asteroid]) > 0

# TODO: Separate class for time conversions?

def minutesToMilliseconds(minutes: float) -> float:
    """Converts minutes into milliseconds."""
    seconds = minutesToSeconds(minutes)
    return secondsToMilliseconds(seconds)

def minutesToSeconds(minutes: float) -> float:
    """Converts minutes to seconds."""
    return minutes * 60

def secondsToMilliseconds(seconds: float) -> float:
    """Converts seconds to milliseconds."""
    return seconds * 1000

def secondsToMinutes(seconds: float) -> float:
    """Converts seconds to minutes."""
    return seconds * 1 / 60

def millisecondsToSeconds(milliseconds: float) -> float:
    """Converts millseconds to seconds."""
    return milliseconds * 1 / 1000

def millisecondsToMinutes(milliseconds: float) -> float:
    """Converts milliseconds to minutes."""
    seconds = millisecondsToSeconds(milliseconds)
    return secondsToMinutes(seconds)

def millisecondsToMinutesSecondsFormat(milliseconds: float) -> str:
    """Converts millseconds to a string with time formated as {minutes}:{seconds}."""
    # Convert milliseconds to minutes with remainder
    minutes = millisecondsToMinutes(milliseconds)
    # Convert remainder to seconds
    remainder = minutes - int(minutes)
    seconds = minutesToSeconds(remainder)
    formatted_time = f'{int(minutes)}:{int(seconds)}'
    # Add a leading zero to the seconds if the number of seconds is a single digit number
    if int(seconds) < 10:
        formatted_time = f'{int(minutes)}:0{int(seconds)}'
    return formatted_time

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
    num_asteroids = 3
    asteroids = create_asteroids(num_asteroids)
    sprites_group = pygame.sprite.RenderPlain((asteroids, player))
    score = 0
    high_score = load_data('high_score.json', 'r')['high_score']
    current_high_score_color = (255, 255, 255)
    time_limit = minutesToMilliseconds(2)
    game_active = True
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and game_active:
                player.smash()
                hit_list = pygame.sprite.spritecollide(player, sprites_group, False)
                hit_asteroids = [obj for obj in hit_list if type(obj) == Asteroid]
                if len(hit_asteroids) != 0:
                    hit_asteroids[0].explode()
                    # Update the score with 1 points awards for every asteroid destroyed
                    # Showing * 1 for clarity that each asteroid is worth 1 point
                    score += len(hit_asteroids) * 1
                    sprites_group.remove(hit_asteroids)
                # TODO: Clicking and missing an asteroid
                # Check if the group has any asteroids remaining
                if not has_asteroids(sprites_group):
                    # Refill the group with one more asteroid than before
                    num_asteroids += 1
                    asteroids = create_asteroids(num_asteroids)
                    sprites_group.add(asteroids)
            if event.type == pygame.MOUSEBUTTONUP and game_active:
                player.unsmash()
        # TODO: Refill the sprite group with asteroids with one more asteroid then before once all asteroids have been destroyed.
        sprites_group.update()
        gameview.fill((0, 0, 0))
        remaining_time = time_limit - pygame.time.get_ticks()
        if remaining_time <= 0:
            game_active = False
        if game_active:
            if pygame.font:
                font = load_font('Pixeltype.ttf', 16)
                # Score Text
                text = font.render(f'Score: {score}', False, (255, 255, 255))
                textpos = text.get_rect(topleft = (5, 5))
                # Remaining Time Text
                remaining_time_text_color = (255, 255, 255)
                if remaining_time < secondsToMilliseconds(10):
                    remaining_time_text_color = (255, 87, 51)
                remaining_time_text = font.render(f'Time: {millisecondsToMinutesSecondsFormat(remaining_time)}', False, remaining_time_text_color)
                remaining_time_text_pos = remaining_time_text.get_rect(topleft = (textpos.x, textpos.y + 10))
                gameview.blit(remaining_time_text, remaining_time_text_pos)
                gameview.blit(text, textpos)
                # High Score Text
                # Check if the user has achieved a new high score
                # Don't alter the original high score, use a local copy instead
                current_high_score = high_score
                if score > current_high_score:
                    current_high_score = score
                    current_high_score_color = (57, 255, 20)
                high_score_text = font.render(f'High Score: {current_high_score}', False, current_high_score_color)
                high_score_textpos = high_score_text.get_rect(topright = (gameview.get_width() - 5, 5))
                gameview.blit(high_score_text, high_score_textpos)
        else:
            if pygame.font:
                font = load_font('Pixeltype.tff', 24)
                end_game_text = font.render('Thanks for playing!', False, (255, 255, 255))
                end_game_text_pos = end_game_text.get_rect(center = (gameview.get_width() / 2, gameview.get_height() / 2))
                gameview.blit(end_game_text, end_game_text_pos)
                if score > high_score:
                    # Render the new high score
                    new_high_score_text = font.render(f'New High Score: {score}', False, (57, 255, 20))
                    new_high_score_pos = new_high_score_text.get_rect(center = (gameview.get_width() / 2, gameview.get_height()  * 3 / 4))
                    gameview.blit(new_high_score_text, new_high_score_pos)
                    # Save the new high score
                    save_data('high_score.json', {"high_score": score})
        sprites_group.draw(gameview)
        scaled_gameview = pygame.transform.scale(gameview, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_gameview, (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    main()
# References
# Line by Line Chimp (pygame docs, https://www.pygame.org/docs/tut/ChimpLineByLine.html)
# pygame.Surface.set_colorkey (pygame docs, https://www.pygame.org/docs/ref/surface.html#pygame.Surface.set_colorkey)
# Pixeltype.ttf font obtained from: https://github.com/clear-code-projects/UltimatePygameIntro/tree/main/font