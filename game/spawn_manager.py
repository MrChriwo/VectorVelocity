import pygame
from obstacle import Obstacle
import random

class SpawnManager: 
    def __init__(self, gameScreen: pygame.Surface, lane_positions: list):
        self.gameScreen = gameScreen
        self.lane_positions = lane_positions
        self.obstacles = []
        self.used_lanes = []
        self.spawn_timer = 0
        self.spawn_rate = 2
        self.speed = 2

    def spawn_obstacles(self):
        count = random.randint(1, 2)
        height = random.randint(50, 150)

        for _ in range(count):
            lane = random.choice(self.lane_positions)
            # get unique values of used lanes, use a lane thats not in the unique values
            unique_lanes = set(self.used_lanes)
            if len(unique_lanes) == 3:
                return
            while lane in unique_lanes:
                lane = random.choice(self.lane_positions)

            self.used_lanes.append(lane)
            self.obstacles.append(Obstacle(height, self.gameScreen, self.speed, lane))

       

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer = 0
            self.spawn_obstacles()
        
        for obstacle in self.obstacles[:]:  
            obstacle.update()
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                self.used_lanes.remove(obstacle.x)

    
    def draw(self):
        for obstacle in self.obstacles:
            obstacle.draw(self.gameScreen)

