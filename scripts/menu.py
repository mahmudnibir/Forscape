import pygame, sys, os


def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# level feature is available. you can uncomment it here and in main code to activate it


class Menu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont(None, 55)
        self.small_font = pygame.font.SysFont(None, 35)
        self.button_size = (200, 50)
        self.button_color = (22, 31, 48)
        self.hover_color = (87, 143, 170)
        self.text_color = (247, 163, 90)

        # Load background image
        self.bg_image = pygame.image.load(resource_path('assets/img/bg_img/LandscapeOculus.png'))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))

        # Button positions for the main menu
        self.main_buttons = {
            'Play': (self.screen_width // 2, self.screen_height // 2 ),
            'Help': (self.screen_width // 2, self.screen_height // 2 + 100),
            'Quit': (self.screen_width // 2, self.screen_height // 2 + 200)
        }

        # # Button positions for the level menu
        # self.level_buttons = {
        #     'Level 1': (self.screen_width // 2, self.screen_height // 2 - 50),
        #     'Level ': (self.screen_width // 2, self.screen_height // 2 + 50),
        #     'Back': (50, 50)
        # }

        # Button positions for the help menu
        self.help_buttons = {
            'Back': (50, 50)
        }

        self.current_menu = 'main'  # Start with the main menu

    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        self.screen.blit(text_obj, text_rect)

    def draw_button(self, label, x, y, color, hover_color):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x - self.button_size[0] // 2, y - self.button_size[1] // 2, *self.button_size)

        if rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, hover_color, rect, border_radius=15)
            if click[0] == 1:  # Detect mouse click
                return label
        else:
            pygame.draw.rect(self.screen, color, rect, border_radius=15)

        self.draw_text(label, self.font, self.text_color, x, y)
        return None

    def display_help(self):
        while True:
            self.screen.blit(self.bg_image, (0, 0))  # Blit the background image

            # Help text content
            help_lines = [
                "Game Controls:",
                "- Move Left/Right: Use the left and right arrow keys.",
                "- Jump: Press the spacebar to jump; press again for a double jump.",
                "",
                "Game Features:",
                "- Collect Gems: Gather gems for points!",
                "- Enemies: Avoid or defeat enemies to progress.",
                "",
                "For more help or for any issues, contact the developer."
            ]

            # Draw help text
            y_offset = self.screen_height // 4  # Start drawing text lower on the screen
            for line in help_lines:
                self.draw_text(line, self.small_font, (230,230,230), self.screen_width // 2, y_offset)
                y_offset += 30  # Space between lines

            # Draw the back button
            back_button = self.draw_button('Back', self.help_buttons['Back'][0], self.help_buttons['Back'][1], self.button_color, self.hover_color)

            if back_button == 'Back':
                self.current_menu = 'main'
                return None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            pygame.display.update()

    # def level_menu(self):
    #     while True:
    #         self.screen.blit(self.bg_image, (0, 0))  # Blit the background image
    #         self.draw_text('Select Level', self.font, (124, 175, 203), self.screen_width // 2, self.screen_height // 4)

    #         for label, (x, y) in self.level_buttons.items():
    #             selected_button = self.draw_button(label, x, y, self.button_color, self.hover_color)
    #             if selected_button:
    #                 if selected_button == 'Back':
    #                     self.current_menu = 'main'
    #                     return None
    #                 elif selected_button == 'Level 1':
    #                     return selected_button
    #                 elif selected_button == 'Level 2':
    #                     return selected_button
    #                   # Return 'Level 1' or 'Level 2'

    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 return

    #         pygame.display.update()

    def run(self):
        while True:
            self.screen.blit(self.bg_image, (0, 0))  # Blit the background image

            if self.current_menu == 'main':
                for label, (x, y) in self.main_buttons.items():
                    selected_button = self.draw_button(label, x, y, self.button_color, self.hover_color)

                    if selected_button == 'Play':
                        return 'start_game'  # Directly return a signal to start the game
                    elif selected_button == 'Help':
                        self.display_help()
                    elif selected_button == 'Quit':
                        pygame.quit()  # Exit directly without confirmation
                        return  # End the program

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            pygame.display.update()

