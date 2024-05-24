import pygame 
import settings


class LevelArea: 
    def __init__(self, screen):
        self.screen = screen
        self.rect = pygame.Rect(settings.LEVEL_X, settings.LEVEL_Y, settings.LEVEL_WIDTH, settings.LEVEL_HEIGHT)
        self.lane_positions = settings.LANE_POSITIONS
        # invisible rectangle to draw the level area on the screen
        self.checkpoint = pygame.Rect(settings.LEVEL_X / 2, settings.LEVEL_Y / 2, 1, 1)
    
    def draw(self):
        pygame.draw.rect(self.screen, (213, 23, 255), self.rect)

    def get_lane_position(self, lane):
        return self.lane_positions[lane]
    
    def update(self, dt):
        # draw level area, and move it down
        self.rect.y += 100 * dt
        self.checkpoint.y += 100 * dt

        # if the the mid of the level area is at the mid of the screen, reset the y position
        if self.checkpoint.y > settings.SCREEN_HEIGHT / 2:
            self.rect.y = settings.LEVEL_Y
            self.checkpoint.y = settings.LEVEL_Y / 2
        
