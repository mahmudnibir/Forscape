import pygame
from pygame.locals import *
from pygame import mixer
import csv
import sys
import os

# Import your other classes
from button import Button
from menu import Menu
from coin import Coin
from timer import Timer
from player import Player
from world import World
from win_msg import WinScreen

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()


# frame rate control here
clock = pygame.time.Clock()
fps = 60

# constants
screen_width = 1000
screen_height = 700
ROWS = 14
COLS = 20
TILE_TYPES = 16
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# Define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

# Define game variables
tile_size = 50
game_over = 0
main_menu = True
level = 1
max_levels = 3
score = 0


def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Define colours
white = (255, 255, 255)
blue = (0, 0, 255)

# Load images
bg_img = pygame.image.load(resource_path('assets/img/bg_img/bg1.png'))
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
restart_img = pygame.image.load(resource_path('assets/img/button_img/restart_btn.png'))

# Load sounds
pygame.mixer.music.load(resource_path('assets/audios/music.mp3'))
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound(resource_path('assets/audios/coin.wav'))
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound(resource_path('assets/audios/jump.wav'))
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound(resource_path('assets/audios/game_over.wav'))
game_over_fx.set_volume(0.5)

img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(resource_path(f'assets/img/tiles/{x}.png'))
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function to reset level
def reset_level(level):
    global world_data  # Make sure to reference the global variable
    player.reset(100, screen_height - 130)
    blob_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()

    # Load in level data and create world
    world_data = []
    try:
        with open(resource_path(f'data/level{level}_data.csv'), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                if x >= ROWS:
                    break  # Prevent index out of range
                world_data.append([int(tile) for tile in row[:COLS]])  # Ensure we only take up to COLS tiles
    except Exception as e:
        print(f"Error loading level {level}: {e}")

    world = World(world_data, tile_size, blob_group, platform_group, lava_group, coin_group, exit_group, enemy_group)
    return world

player = Player(100, screen_height - 330)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# Create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

# Load the initial level
world_data = []
for _ in range(ROWS):
    world_data.append([-1] * COLS)
world = reset_level(level)

# Create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 50, restart_img)

menu = Menu(screen, screen_width, screen_height)
win_screen = WinScreen(screen, font)
timer = Timer()

run = True
while run:

	clock.tick(fps)

	screen.blit(bg_img, (0, 0))

	if main_menu == True:
		choice = menu.run()
		if choice == 'Quit':
			run = False
		elif choice == 'start_game':
			# level = 1
			main_menu = False
			timer.start()
	else:
		world.draw(screen)

		if game_over == 0:
			elapsed_time = timer.get_formatted_time()
			draw_text(f'Time: {elapsed_time}', font_score, (243, 133, 24), tile_size - 35, 50)
			blob_group.update()
			platform_group.update()
			#update score
			#check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
				coin_fx.play()
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
		
		blob_group.draw(screen)
		platform_group.draw(screen)
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)
		enemy_group.draw(screen)

		game_over = player.update(game_over, world, blob_group, lava_group, exit_group, platform_group, game_over_fx, font, screen_width, screen_height)

		#if player has died
		if game_over == -1:
			# timer.reset()
			if restart_button.draw():
				world_data = []
				world = reset_level(level)
				game_over = 0
				score = 0
				# timer.start()

		#if player has completed the level
		if game_over == 1:
			#reset game and go to next level
			# timer.stop()
			level += 1
			if level <= max_levels:
				#reset level
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				win_screen.draw(score)
				if restart_button.draw():
					level = 1
					timer.reset()
					timer.start()
					#reset level
					world_data = []
					world = reset_level(level)
					game_over = 0
					score = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
