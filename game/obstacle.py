import pygame
import settings
import os
import random
class Obstacle:
    def __init__(self, gameScreen, speed, lane, y, x_offset):
        self.gameScreen = gameScreen
        self.width, self.height = 90, 90
        self.speed = speed
        self.y = y
        self.x = lane + x_offset
        self.image = self.load_random_image()

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    # loading random image from the obstacle asset path
    def load_random_image(self):
        images = [file for file in os.listdir(settings.OBSTACLE_ASSET_PATH)]
        random_image_file = random.choice(images)
        image = pygame.image.load(os.path.join(settings.OBSTACLE_ASSET_PATH, random_image_file))
        image = pygame.transform.scale(image, (int(self.width), int(self.height)))
        return image
    
    def update(self):
        self.y += self.speed

    def draw(self, screen):
        # Drawing the image instead of a rectangle
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.y > self.gameScreen.get_height()