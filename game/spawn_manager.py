import pygame
from obstacle import Obstacle
from coin import Coin
import random
from player import Player
from level_area import LevelArea
import settings

class SpawnManager: 
    def __init__(self, player: Player, gameScreen, quitGame, lane_positions: list):
        self.gameScreen = gameScreen
        self.player = player
        self.lane_positions = lane_positions
        self.obstacles = []
        self.used_lanes = []
        self.coins = []
        self.collected_coins = 0  
        self.spawn_timer = 0
        self.spawn_rate = 5
        self.speed = 2
        self.coin_speed = 2
        self.coin_spawn_timer = 0
        self.coin_spawn_rate = 7
        self.level = LevelArea(gameScreen)
        self.quitGame = quitGame

    def spawn_level(self):
        self.level.draw()

    def check_collisions(self, source, objects):
        for object in objects:
            if source.rect.colliderect(object.rect):
                if isinstance(object, Coin):
                    self.coins.remove(object)
                    self.collected_coins += 1
                elif isinstance(object, Obstacle):
                    if pygame.rect.Rect.contains(object.rect, source.rect):
                        self.coins.remove(source)   
                        continue
                    if isinstance(source, Player):                      
                        print(f"collision detected, game over. Collected coins: {self.collected_coins}")
                        self.quitGame()

    def spawn_obstacles(self):
        count = random.randint(1, 2)
        height = random.randint(120, settings.LEVEL_HEIGHT * 0.38)

        for _ in range(count):
            lane = random.choice(self.lane_positions)
            unique_lanes = set(self.used_lanes)
            if len(unique_lanes) == 3:
                return
            while lane in unique_lanes:
                lane = random.choice(self.lane_positions)

            self.used_lanes.append(lane)
            self.obstacles.append(Obstacle(height, self.gameScreen, self.speed, lane))

    def spawn_coins(self):
        spawn_count = random.randint(5, 10)
        lane_count = random.randint(1, 2)
        current_lane_player = self.player.current_lane
        roi = self.lane_positions.copy()
        roi.pop(current_lane_player)        
        y = -150

        for _ in range(lane_count):
            for i in range(spawn_count):
                coin = Coin(self.gameScreen, self.coin_speed, y, roi[_])
                self.coins.append(coin)
                y -= 30
        
    def remove_objects(self, objects):
        for object in objects:
            object.update()
            if object.is_off_screen():
                objects.remove(object)
                if isinstance(object, Obstacle):
                    self.used_lanes.remove(object.x)

    def update(self, dt):
        self.level.update(dt)
        self.check_collisions(self.player, self.obstacles)
        self.check_collisions(self.player, self.coins)
        for coin in self.coins:
            if len(self.obstacles) == 0:
                break
            self.check_collisions(coin, self.obstacles)

        self.spawn_timer += dt
        self.coin_spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer = 0
            self.spawn_obstacles()
            
        if self.coin_spawn_timer >= self.coin_spawn_rate:
            self.coin_spawn_timer = 0
            self.spawn_coins()

        self.remove_objects(self.obstacles)
        self.remove_objects(self.coins)

    
    def draw(self):
        self.spawn_level()
        self.player.draw(self.gameScreen)
        for obstacle in self.obstacles:
            obstacle.draw(self.gameScreen)
        
        for coin in self.coins:
            coin.draw(self.gameScreen)
        

