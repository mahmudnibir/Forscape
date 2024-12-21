import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 1000
screen_height = 700

# Create the screen object
screen = pygame.display.set_mode((screen_width, screen_height))

# Define Player class
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
        jump_force = -16
        second_jump_force = -15
        max_fall_speed = 10
        max_jumps = 2

        if game_over == 0:
            key = pygame.key.get_pressed()

            # Jump logic
            if key[pygame.K_SPACE] and self.jumps_left > 0 and not self.jumped:
                if self.jumps_left == 2:
                    self.vel_y = jump_force
                elif self.jumps_left == 1:
                    self.vel_y = second_jump_force
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
                self.counter = 0
                self.index = 0
                self.image = self.idle_right[self.index] if self.direction == 1 else self.idle_left[self.index]

            # Handle run animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.run_right):
                    self.index = 0
                self.image = self.run_right[self.index] if self.direction == 1 else self.run_left[self.index]

            # Add gravity and limit fall speed
            self.vel_y += gravity
            if self.vel_y > max_fall_speed:
                self.vel_y = max_fall_speed
            dy += self.vel_y

            # Check for collision with tiles
            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
                        self.jumps_left = max_jumps

            # Prevent falling through screen bottom
            if self.rect.bottom + dy >= screen_height:
                self.rect.bottom = screen_height
                self.vel_y = 0
                self.in_air = False
                self.jumps_left = max_jumps

            # Update player position
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)
        return game_over

    def reset(self, x, y):
        self.run_right = []
        self.run_left = []
        self.idle_right = []
        self.idle_left = []
        self.jump_right = []
        self.jump_left = []
        self.index = 0
        self.counter = 0

        # Load the sprite sheets for run, idle, and jump animations
        run_sprite_sheet = pygame.image.load('_run.png')
        idle_sprite_sheet = pygame.image.load('_idle.png')
        jump_sprite_sheet = pygame.image.load('_jump.png')

        # Assuming each frame is 32x32 in the sprite sheet
        frame_width = 120
        frame_height = 40
        scale_width = 40
        scale_height = 60

        # Load run animation frames
        for num in range(10):  # 10 frames for run animation
            img_right = run_sprite_sheet.subsurface((num * frame_width, 0, frame_width, frame_height))
            img_right = pygame.transform.scale(img_right, (scale_width, scale_height))
            img_left = pygame.transform.flip(img_right, True, False)
            self.run_right.append(img_right)
            self.run_left.append(img_left)

        # Load idle animation frames
        for num in range(10):  # 10 frames for idle animation
            img_right = idle_sprite_sheet.subsurface((num * frame_width, 0, frame_width, frame_height))
            img_right = pygame.transform.scale(img_right, (scale_width, scale_height))
            img_left = pygame.transform.flip(img_right, True, False)
            self.idle_right.append(img_right)
            self.idle_left.append(img_left)

        # Load jump animation frames
        for num in range(10):  # 10 frames for jump animation
            img_right = jump_sprite_sheet.subsurface((num * frame_width, 0, frame_width, frame_height))
            img_right = pygame.transform.scale(img_right, (scale_width, scale_height))
            img_left = pygame.transform.flip(img_right, True, False)
            self.jump_right.append(img_right)
            self.jump_left.append(img_left)

        self.dead_image = pygame.image.load('assets/img/lost_img.png')
        self.image = self.run_right[self.index]
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
