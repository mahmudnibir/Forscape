import pygame

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = pygame.time.get_ticks()
            self.running = True

    def stop(self):
        if self.running:
            self.elapsed_time += pygame.time.get_ticks() - self.start_time
            self.running = False

    def reset(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False

    def get_time(self):
        if self.running:
            return self.elapsed_time + (pygame.time.get_ticks() - self.start_time)
        return self.elapsed_time

    def get_formatted_time(self):
        total_seconds = self.get_time() // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02}:{seconds:02}"
