import pygame, sys, os
import random


def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class WinScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.message = "YOU WIN!"
        self.color = (243, 133, 24)
        self.particles = []
        self.music_played = False
        self.show_score = False

    def play_music(self):
        if not self.music_played:
            pygame.mixer.music.load(resource_path('assets/audios/win_music.mp3'))
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(2)
            self.music_played = True

    def add_particles(self):
        for _ in range(10):
            x = random.randint(0, self.screen.get_width())
            y = random.randint(0, self.screen.get_height())
            self.particles.append([x, y, random.randint(2, 6)])

    def update_particles(self):
        for particle in self.particles:
            particle[1] -= random.randint(1, 3)  # move upward
            particle[2] -= 0.1  # shrink size
            pygame.draw.circle(self.screen, (0, 246, 246), (particle[0], particle[1]), int(particle[2]))

        self.particles = [p for p in self.particles if p[2] > 0]

    def display_message(self):
        text = self.font.render(self.message, True, self.color)
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - 150))

    def display_score(self, score):
        score_text = f"Your Score: {score}"
        text = self.font.render(score_text, True, (35, 255, 155))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - 30))

    def draw(self, score):
        # Play music and show particles
        self.play_music()
        self.add_particles()
        self.update_particles()

        # Display "YOU WIN" message
        self.display_message()

        # Show score
        self.display_score(score)
