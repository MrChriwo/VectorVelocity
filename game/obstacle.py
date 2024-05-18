import pygame
import random

class Obstacle:
    def __init__(self, height, gameScreen, speed, lane):
        self.gameScreen = gameScreen
        self.width, self.height = 150, height
        self.speed = speed
        self.y = -height + 20
        self.x = lane

    
    def update(self):
        self.y += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, (123, 255, 255), (self.x, self.y, self.width, self.height))
    
    def is_off_screen(self):
        return self.y > self.gameScreen.get_height()