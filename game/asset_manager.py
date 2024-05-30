import pygame 
import settings 
import os

class AssetManager: 
    def __init__(self): 
        self.assets = {}
        self.load_assets()

    def load_assets(self): 
        self.assets['background'] = pygame.image.load(settings.BACKGROUND_ASSET_PATH)
        self.assets['background'] = pygame.transform.scale(self.assets['background'], (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.assets['bgmusic'] = pygame.mixer.Sound(settings.SOUNDS_ASSET_PATH + "bgmusic.wav")
        self.assets['bgmusic'].set_volume(settings.MUSIC_VOLUME)
        self.assets["player"] = pygame.image.load(settings.PLAYER_ASSET_PATH)
        self.assets["obstacles"] = []

        obstacles = os.listdir(settings.OBSTACLE_ASSET_PATH)
        for obstacle in obstacles: 
            self.assets["obstacles"].append(pygame.image.load(settings.OBSTACLE_ASSET_PATH + obstacle)) 


    def get_asset(self, key): 
        return self.assets[key]