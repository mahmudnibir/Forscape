import pygame
from enemy import Enemy  
from game_platform import Platform  
from lava import Lava  
from coin import Coin  
from exit import Exit 
import sys, os

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TileTypes:
    EMPTY = -1
    COIN = 0
    DIRT1 = 1
    DIRT2 = 2
    DIRT3 = 3
    DIRT4 = 4
    DIRT5 = 5
    DIRT6 = 6
    DIRT7 = 7
    ENEMY = 8
    BAT = 9
    BEE = 10
    LAVA = 11
    SPIKE = 12
    GRASS = 13
    ROCK = 14
    EXIT1 = 15
    EXIT2 = 17

class World:
    def __init__(self, data, tile_size, blob_group, platform_group, lava_group, coin_group, exit_group, enemy_group):
        self.tile_list = []
        self.tile_size = tile_size

        # Load tile images and scale them
        self.images = {
            'dirt1': pygame.transform.scale(pygame.image.load(resource_path('assets/img/tiles/1.png')), (tile_size, tile_size)),
            'dirt2': pygame.transform.scale(pygame.image.load(resource_path('assets/img/tiles/2.png')), (tile_size, tile_size)),
            'dirt3': pygame.transform.scale(pygame.image.load(resource_path('assets/img/tiles/3.png')), (tile_size, tile_size)),
            'dirt4': pygame.transform.scale(pygame.image.load(resource_path('assets/img/tiles/4.png')), (tile_size, tile_size)),
            'dirt5': pygame.transform.scale(pygame.image.load(resource_path('assets/img/tiles/5.png')), (tile_size, tile_size)),
            'dirt6': pygame.transform.scale(pygame.image.load(resource_path('assets/img/tiles/6.png')), (tile_size, tile_size)),
            'dirt7': pygame.transform.scale(pygame.image.load(resource_path('assets/img/tiles/7.png')), (tile_size, tile_size)),
            'grass': pygame.transform.scale(pygame.image.load(resource_path('assets/img/tiles/13.png')), (tile_size, tile_size))
        }

        self.load_world(data, blob_group, platform_group, lava_group, coin_group, exit_group, enemy_group)

    def load_world(self, data, blob_group, platform_group, lava_group, coin_group, exit_group, enemy_group):
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile in {TileTypes.DIRT1, TileTypes.DIRT2, TileTypes.DIRT3, TileTypes.DIRT4, TileTypes.DIRT5, TileTypes.DIRT6, TileTypes.DIRT7}:
                    img_name = {TileTypes.DIRT1: 'dirt1', TileTypes.DIRT2: 'dirt2', TileTypes.DIRT3: 'dirt3',
                                TileTypes.DIRT4: 'dirt4', TileTypes.DIRT5: 'dirt5', TileTypes.DIRT6: 'dirt6',
                                TileTypes.DIRT7: 'dirt7'}.get(tile)
                    img = self.images[img_name]
                    img_rect = img.get_rect(topleft=(col_count * self.tile_size, row_count * self.tile_size))
                    self.tile_list.append((img, img_rect))

                elif tile == TileTypes.GRASS:
                    img = self.images['grass']
                    img_rect = img.get_rect(topleft=(col_count * self.tile_size, row_count * self.tile_size))
                    self.tile_list.append((img, img_rect))

                elif tile == TileTypes.ENEMY:
                    blob = Enemy(col_count * self.tile_size, row_count * self.tile_size + 15)
                    blob_group.add(blob)

                elif tile == TileTypes.DIRT5:
                    platform = Platform(col_count * self.tile_size, row_count * self.tile_size, 2, 0)
                    platform_group.add(platform)

                elif tile == TileTypes.LAVA:
                    lava = Lava(col_count * self.tile_size, row_count * self.tile_size + (self.tile_size // 2))
                    lava_group.add(lava)

                elif tile == TileTypes.COIN:
                    coin = Coin(col_count * self.tile_size + (self.tile_size // 2), row_count * self.tile_size + (self.tile_size // 2))
                    coin_group.add(coin)

                elif tile in {TileTypes.EXIT1, TileTypes.EXIT2}:
                    exit_tile = Exit(col_count * self.tile_size, row_count * self.tile_size - (self.tile_size // 2))
                    exit_group.add(exit_tile)

                col_count += 1
            row_count += 1

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
