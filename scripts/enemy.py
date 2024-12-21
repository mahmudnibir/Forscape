import pygame, sys, os


def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type='blob'):
        pygame.sprite.Sprite.__init__(self)
        
        # Load different images based on enemy type
        if enemy_type == 'bat':
            self.image = pygame.image.load(resource_path('assets/img/tiles/3.png'))
        elif enemy_type == 'bee':
            self.image = pygame.image.load(resource_path('assets/img/tiles/4.png'))
        else:
            self.image = pygame.image.load(resource_path('assets/img/blob.png'))  # Default is the blob)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
