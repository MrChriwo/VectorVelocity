import pygame
from obstacle import Obstacle
from coin import Coin
import random
from player import Player
from level_area import LevelArea
import settings

class SpawnManager: 

    def __init__(self, player: Player, gameScreen, quitGame, lane_positions: list, speed):
        self.gameScreen = gameScreen
        self.player = player
        self.lane_positions = lane_positions
        self.obstacles = []
        self.used_lanes = []
        self.coins = []
        self.obstacle_spawn_timer = 0
        self.coin_spawn_timer = 0
        self.obstacle_spawn_rate = 2.5
        self.speed = speed
        self.coin_spawn_rate = self.obstacle_spawn_rate +2
        self.level = LevelArea(gameScreen)
        self.quitGame = quitGame


    def spawn_level(self):
        self.level.draw()


    def update_spawn_rates(self):
        # print("spawn rate: ", self.obstacle_spawn_rate)
        if self.obstacle_spawn_rate >= settings.MAINIMUM_OBSTACLE_SPAWN_RATE:
            self.obstacle_spawn_rate -= settings.OBSTACLE_SPAWN_RATE_DECREASE
            self.coin_spawn_rate = (self.obstacle_spawn_rate + 2) * settings.COIN_SPAWN_RATE_MULTIPLIER
            # print("spawn rate updated: ", self.obstacle_spawn_rate)


    def get_available_lane(self):
        available_lanes = [lane for lane in self.lane_positions if lane not in self.used_lanes]
        if not available_lanes:
            return None
        return random.choice(available_lanes)


    def update_speed(self, speed):
        self.speed = speed
        for obstacle in self.obstacles:
            obstacle.speed = speed
        for coin in self.coins:
            coin.speed = speed


    def check_collisions(self, source, objects, updateCoins = False):
        for object in objects:
            if source.rect.colliderect(object.rect):
                if isinstance(object, Coin):
                    self.coins.remove(object)
                    if updateCoins: updateCoins(1)
                elif isinstance(object, Obstacle):
                    if pygame.rect.Rect.contains(object.rect, source.rect):
                        self.coins.remove(source)   
                        continue
                    if isinstance(source, Player):                      
                        self.quitGame()

            
    def spawn_obstacles(self):
        count = random.randint(1, settings.MAXIMUM_OBSTACLE_SPAWN_COUNT)
        spawned = []
        y_offset = -100
        lane = self.get_available_lane()

        for _ in range(count):    
            unique_lanes = set(self.used_lanes)
            if len(unique_lanes) == 3:
                return
            x_offset = random.randint(-82, 83)
            if lane is None:
                return
            obstacle = Obstacle(self.gameScreen, self.speed, lane, y_offset, x_offset)

            y_offset -= settings.OBSTACLE_Y_OFFSET_DECREASE
            spawned.append(obstacle)
            self.obstacles.append(obstacle)
            self.used_lanes.append(lane + x_offset)


    def spawn_coins(self):
        spawn_count = random.randint(5, 10)
        lane_count = random.randint(1, 2)
        current_lane_player = self.player.current_lane
        roi = self.lane_positions.copy()
        roi.pop(current_lane_player)        
        y = -110

        for _ in range(lane_count):
            for i in range(spawn_count):
                coin = Coin(self.gameScreen, self.speed, y, roi[_])
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
        for coin in self.coins:
            if len(self.obstacles) == 0:
                break
            self.check_collisions(coin, self.obstacles)

        self.obstacle_spawn_timer += dt
        self.coin_spawn_timer += dt

        if self.obstacle_spawn_timer >= self.obstacle_spawn_rate:
            self.obstacle_spawn_timer = 0
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
        
