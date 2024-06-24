import pygame
import random
from asset_manager import AssetManager
from settings import LANE_POSITIONS
class Obstacle:
    def __init__(self, gameScreen, speed, lane_x, y, x_offset, assetMgr: AssetManager, id: int):
        self.assetMgr = assetMgr
        self.gameScreen = gameScreen
        self.width, self.height = 90, 90
        self.speed = speed
        self.y = y
        self.x = lane_x + x_offset
        self.lane = LANE_POSITIONS.index(lane_x)
        self.image = self.load_random_image()
        self.id = id

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    # loading random image from the asset manager
    def load_random_image(self):
        images = self.assetMgr.get_asset("obstacles")
        image = random.choice(images)
        image = pygame.transform.scale(image, (int(self.width), int(self.height)))
        return image
    
    def update(self):
        self.y += self.speed

    def draw(self, screen):
        # Drawing the image instead of a rectangle
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.y > self.gameScreen.get_height()