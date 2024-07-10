import pygame 
from . import settings 
import os

class AssetManager: 
    def __init__(self): 
        self.is_audio_available = pygame.mixer.get_init()
        self.assets = {}

        if self.is_audio_available: 
            pygame.mixer.init()

        self.load_assets()

    def load_assets(self): 
        self.assets['background'] = pygame.image.load(settings.BACKGROUND_ASSET_PATH)
        self.assets['background'] = pygame.transform.scale(self.assets['background'], (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.assets["player"] = pygame.image.load(settings.PLAYER_ASSET_PATH)
        self.assets["obstacles"] = []

        if self.is_audio_available:
            self.assets['bgmusic'] = pygame.mixer.Sound(settings.SOUNDS_ASSET_PATH + "bgmusic.wav")
            self.assets['bgmusic'].set_volume(settings.MUSIC_VOLUME)

        obstacles = os.listdir(settings.OBSTACLE_ASSET_PATH)
        for obstacle in obstacles: 
            self.assets["obstacles"].append(pygame.image.load(settings.OBSTACLE_ASSET_PATH + obstacle)) 


    def get_asset(self, key): 
        return self.assets[key]