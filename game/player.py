import pygame
import time

class Player:
    def __init__(self, x, y, width, height, lp, lane_positions):
        self.width = width
        self.height = height
        self.lp = lp
        self.lane_positions = lane_positions
        self.current_lane = 1 # Start in the middle lane
        self.x = self.lane_positions[self.current_lane]
        self.y = y

    def move_to_lane(self, target_lane):
        target_x = self.lane_positions[target_lane]
        while abs(self.x - target_x) > 1:
            self.x += (target_x - self.x) * 0.01 # smooth movement
            time.sleep(0.15) # delay to make movement visible
            self.x = max(min(self.x, target_x), target_x) # Ensure x doesnt overshoot

        self.x = target_x # snap to target lane position
        self.current_lane = target_lane

    def move_left(self):
        if self.current_lane > 0:
            self.move_to_lane(self.current_lane - 1)


    def move_right(self):
        if self.current_lane < len(self.lane_positions) - 1:
            self.move_to_lane(self.current_lane + 1)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))

    def get_position(self):
        return self.x, self.y
    
    def get_size(self):
        return self.width, self.height
    
    def get_lp(self):
        return self.lp
    
    def set_lp(self, lp):
        self.lp = lp