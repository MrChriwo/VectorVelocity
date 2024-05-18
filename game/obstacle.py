import pygame
class Obstacle:
    def __init__(self, height, gameScreen, speed, lane):
        self.gameScreen = gameScreen
        self.width, self.height = 150, height
        self.speed = speed
        self.y = -height + 20  # Start position just above the screen
        self.x = lane

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (123, 255, 255), self.rect)

    def is_off_screen(self):
        return self.y > self.gameScreen.get_height()