import pygame
from obstacle import Obstacle


class Coin: 
    def __init__(self, gameScreen, speed, y,  lane):
        # self.image = pygame.image.load("assets/coin.png")
        # self.image = pygame.transform.scale(self.image, (50, 50))
        self.x = lane
        self.y = y
        self.speed = speed
        self.gameScreen = gameScreen
        # self.rect = self.image.get_rect()
        # self.rect.topleft = (self.x, self.y)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 10, 10)
    
    def update(self):
        self.y += self.speed
    
    def is_off_screen(self):
        return self.y > self.gameScreen.get_height()
        
    def draw(self, gameScreen):
            pygame.draw.rect(gameScreen, (0, 255, 0), self.rect)


