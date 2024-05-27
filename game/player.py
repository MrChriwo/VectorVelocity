import pygame
import settings

class Player:
    def __init__(self, x, lane_positions):
        self.image = pygame.image.load(settings.PLAYER_ASSET_PATH)
        self.lane_positions = lane_positions
        self.target_lane = 1
        self.current_lane = 1
        self.x = x
        self.y = 500
        self.speed = 1350

    @property
    def rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))

    def update(self, dt):
        target_x = self.lane_positions[self.target_lane]
        if self.x != target_x:
            step = self.speed * dt
            distance = target_x - self.x

            if abs(distance) > step:
                self.x += step * (distance / abs(distance))
            else:
                self.x = target_x
                self.current_lane = self.target_lane

    def move_left(self):
        if self.current_lane > 0:
            self.target_lane = self.current_lane - 1

    def move_right(self):
        if self.current_lane < len(self.lane_positions) - 1:
            self.target_lane = self.current_lane + 1

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def get_current_positon(self):
        return self.current_lane
