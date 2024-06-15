import pygame
from obstacle import Obstacle


class Coin: 
    def __init__(self, gameScreen, speed, y,  lane):
        self.x = lane
        self.y = y
        self.speed = speed
        self.gameScreen = gameScreen


    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 10, 10)
    
    def update(self):
        self.y += self.speed
    
    def is_off_screen(self):
        return self.y > self.gameScreen.get_height()
        
    def draw(self, gameScreen):
        pygame.draw.circle(gameScreen, (235, 175, 4), (self.x, self.y), 8) 


