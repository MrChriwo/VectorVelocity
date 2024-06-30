import pygame
from obstacle import Obstacle
from settings import LANE_POSITIONS


class Coin: 
    def __init__(self, gameScreen, speed, y,  lane_x, id: int):
        self.x = lane_x
        self.lane = LANE_POSITIONS.index(lane_x)
        self.y = y
        self.speed = speed
        self.gameScreen = gameScreen
        self.id = id


    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 10, 10)
    
    def update(self):
        self.y += self.speed
    
    def is_off_screen(self):
        return self.y > self.gameScreen.get_height()
        
    def draw(self, gameScreen):
        pygame.draw.circle(gameScreen, (235, 175, 4), (self.x, self.y), 8) 


