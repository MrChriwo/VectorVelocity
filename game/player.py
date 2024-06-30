import pygame
import settings
from asset_manager import AssetManager

class Player:
    def __init__(self, x, lane_positions, assetMgr: AssetManager):
        self.image = assetMgr.get_asset("player")
        self.lane_positions = lane_positions
        self.target_lane = 1
        self.current_lane = 1
        self.x = x
        self.y = settings.PLAYER_Y
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

    def stay_in_lane(self):
        self.target_lane = self.current_lane

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def get_current_positon(self):
        return settings.LANE_POSITIONS[self.current_lane]
    
    def update_speed(self, speed):
        self.speed += speed