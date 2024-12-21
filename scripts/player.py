import pygame
import sys, os

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 1000
screen_height = 700

# Create the screen object
screen = pygame.display.set_mode((screen_width, screen_height))

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Define Player class
class Player:
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over, world, blob_group, lava_group, exit_group, platform_group, game_over_fx, font, screen_width, screen_height, col_thresh=20):
        dx = 0
        dy = 0
        walk_speed = 3
        walk_cooldown = 3
        gravity = 1.01
        jump_force = -17
        second_jump_force = -15
        max_fall_speed = 10
        max_jumps = 2

        if game_over == 0:
            key = pygame.key.get_pressed()

            # Jump logic
            if key[pygame.K_SPACE] and self.jumps_left > 0 and not self.jumped:
                if self.jumps_left == 2:  # First jump
                    self.vel_y = jump_force
                elif self.jumps_left == 1:  # Second jump (double jump)
                    self.vel_y = second_jump_force
                    self.double_jump_animating = True
                self.jumped = True
                self.jumps_left -= 1
            if not key[pygame.K_SPACE]:
                self.jumped = False

            # Horizontal movement
            if key[pygame.K_LEFT]:
                dx -= walk_speed
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += walk_speed
                self.counter += 1
                self.direction = 1
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                # If player is not moving, show idle animation
                self.counter = 0
                self.index = 0
                self.idle_counter += 1
                if self.idle_counter > walk_cooldown:
                    self.idle_counter = 0
                    self.idle_index += 1
                    if self.idle_index >= len(self.idle_images_right):
                        self.idle_index = 0
                    self.image = self.idle_images_right[self.idle_index] if self.direction == 1 else self.idle_images_left[self.idle_index]
            else:
                self.idle_index = 0
                self.idle_counter = 0

            # Handle running animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                self.image = self.images_right[self.index] if self.direction == 1 else self.images_left[self.index]

            # Add gravity and cap the falling speed
            self.vel_y += gravity
            if self.vel_y > max_fall_speed:
                self.vel_y = max_fall_speed
            dy += self.vel_y

            # Check for collision with tiles
            self.in_air = True
            for tile in world.tile_list:
                # x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
                        self.jumps_left = max_jumps
                        self.double_jump_animating = False  # Reset double jump animation

            # Collision with enemies, lava, etc.
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                game_over_fx.play()
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # Prevent falling off the screen
            if self.rect.bottom + dy >= screen_height:
                self.rect.bottom = screen_height
                self.vel_y = 0
                self.in_air = False
                self.jumps_left = max_jumps

            # Prevent going off-screen horizontally
            if self.rect.left + dx < 0:
                dx = -self.rect.left
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right

            # Handle double jump animation
            if self.double_jump_animating:
                self.double_jump_counter += 1
                if self.double_jump_counter > walk_cooldown:
                    self.double_jump_counter = 0
                    self.double_jump_index += 1
                    if self.double_jump_index >= len(self.double_jump_images_right):
                        self.double_jump_index = 0
                    self.image = self.double_jump_images_right[self.double_jump_index] if self.direction == 1 else self.double_jump_images_left[self.double_jump_index]

            # Update player position
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image

            # Move towards x = 500, y = 100
            target_x = 340
            target_y = 100
            speed = 5

            # Move in the x direction
            if self.rect.x < target_x:
                self.rect.x += min(speed, target_x - self.rect.x)
            elif self.rect.x > target_x:
                self.rect.x -= min(speed, self.rect.x - target_x)

            # Move in the y direction
            if self.rect.y > target_y:
                self.rect.y -= min(speed, self.rect.y - target_y)

        screen.blit(self.image, self.rect)
        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.idle_images_right = []
        self.idle_images_left = []
        self.double_jump_images_right = []
        self.double_jump_images_left = []
        self.index = 0
        self.idle_index = 0
        self.counter = 0
        self.idle_counter = 0
        self.double_jump_index = 0
        self.double_jump_counter = 0
        self.double_jump_animating = False

        # Load running sprite sheet (6 frames)
        run_sprite_sheet = pygame.image.load(resource_path('assets/img/character/run2.png'))
        frame_width = 32
        frame_height = 32
        scale_width = 49
        scale_height = 53

        # Load running animation frames
        for num in range(8):
            img_right = run_sprite_sheet.subsurface((num * frame_width, 0, frame_width, frame_height))
            img_right = pygame.transform.scale(img_right, (scale_width, scale_height))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        # Load idle sprite sheet (11 frames)
        idle_sprite_sheet = pygame.image.load(resource_path('assets/img/character/idle.png'))
        for num in range(11):
            img_idle_right = idle_sprite_sheet.subsurface((num * frame_width, 0, frame_width, frame_height))
            img_idle_right = pygame.transform.scale(img_idle_right, (scale_width, scale_height))
            img_idle_left = pygame.transform.flip(img_idle_right, True, False)
            self.idle_images_right.append(img_idle_right)
            self.idle_images_left.append(img_idle_left)

        # Load double jump sprite sheet (6 frames)
        double_jump_sprite_sheet = pygame.image.load(resource_path('assets/img/character/double_jump.png'))
        for num in range(6):
            img_double_jump_right = double_jump_sprite_sheet.subsurface((num * frame_width, 0, frame_width, frame_height))
            img_double_jump_right = pygame.transform.scale(img_double_jump_right, (scale_width, scale_height))
            img_double_jump_left = pygame.transform.flip(img_double_jump_right, True, False)
            self.double_jump_images_right.append(img_double_jump_right)
            self.double_jump_images_left.append(img_double_jump_left)

        self.dead_image = pygame.image.load(resource_path('assets/img/lost_img.png'))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
        self.jumps_left = 2
