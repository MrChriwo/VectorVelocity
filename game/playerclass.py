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

    def move_left(self):
        if self.current_lane > 0:
            target_x = self.lane_positions[self.current_lane - 1]
            while self.x > target_x:
                self.x -= 4 # step size
                time.sleep(0.01) # delay
                self.x = max(self.x, target_x) # Ensure x doesn't go below target_x

            self.current_lane -= 1


    def move_right(self):
        if self.current_lane < len(self.lane_positions) - 1:
            target_x = self.lane_positions[self.current_lane + 1]
            while self.x < target_x:
                self.x += 4 # step size
                time.sleep(0.01) # delay
                self.x = min(self.x, target_x) # Ensure x doesn't go above target_x

            self.current_lane += 1

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