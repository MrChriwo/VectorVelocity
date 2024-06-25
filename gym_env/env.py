import sys
import os
cwd = os.getcwd()
sys.path.append(cwd)

from game.settings import FRAME_RATE, SCREEN_HEIGHT, LANE_POSITIONS, MAXIMUM_SPEED, PLAYER_Y, LEVEL_WIDTH
from game.game import Game
import gymnasium as gym
from gymnasium import spaces
import numpy as np


class VVEnv(gym.Env):
    metadata = {'render.modes': ['human'], 'render_fps': FRAME_RATE}

    def __init__(self, mode='human'):
        super(VVEnv, self).__init__()
        self.mode = mode
        self.game = Game(self.mode)
        self.num_obstacles = 9
        self.num_coins = 20
        self.num_lanes = len(LANE_POSITIONS)

        self.OBSTACLE_Y_CONDITION = -89
        self.COIN_Y_CONDITION = -19
        self.OBSTACLE_MIN_X = LANE_POSITIONS[0] - 82
        self.OBSTACLE_MAX_X = LANE_POSITIONS[-1] + 83
        
        self.observation_space = spaces.Dict({
            "obstacles": spaces.Box(low=-1, high=1, shape=(self.num_obstacles*2,), dtype=np.float32),
            "coins": spaces.Box(low=-1, high=1, shape=(self.num_coins*2,), dtype=np.float32),
            "obstacles_y_dist": spaces.Box(low=-1, high=1, shape=(self.num_obstacles,), dtype=np.float32),
            "obstacles_x_dist": spaces.Box(low=-1, high=1, shape=(self.num_obstacles,), dtype=np.float32),
            "coin_y_dist": spaces.Box(low=-1, high=1, shape=(self.num_coins,), dtype=np.float32),
            "coin_x_dist": spaces.Box(low=-1, high=1, shape=(self.num_coins,), dtype=np.float32),
            "lane_obstacles": spaces.MultiDiscrete([self.num_lanes]*self.num_obstacles ,dtype=np.int32),
            "lane_coins": spaces.MultiDiscrete([self.num_lanes]*self.num_coins, dtype=np.int32),
            "score": spaces.Discrete(120000 +1),
            "collected_coins": spaces.Discrete(20000 +1),
            "speed": spaces.Discrete(MAXIMUM_SPEED +1),
            "player_pos": spaces.MultiDiscrete([1], dtype=np.float32)
        })
        self.action_space = spaces.Discrete(3)
        self.latest_speed = self.game.speed
        self.current_reward = 0
        self.dodged_obstacles = []
        self.missed_coins = []

    def normalize_coordinate(self, object_type: str, value: tuple):
        if object_type not in ["obstacle", "coin", "player"]:
            raise ValueError("Invalid object type. Must be either 'obstacle' or 'coin'")
        
        if object_type == "obstacle":
            norm_x = (value[0] - self.OBSTACLE_MIN_X) / (self.OBSTACLE_MAX_X - self.OBSTACLE_MIN_X)
            norm_y = (value[1] + abs(self.OBSTACLE_Y_CONDITION)) / (SCREEN_HEIGHT + abs(self.OBSTACLE_Y_CONDITION))
            return norm_x, norm_y
        elif object_type == "coin":
            norm_x = (value[0] - LANE_POSITIONS[0]) / (LANE_POSITIONS[-1] - LANE_POSITIONS[0])
            norm_y = (value[1] + abs(self.COIN_Y_CONDITION)) / (SCREEN_HEIGHT + abs(self.COIN_Y_CONDITION))
            return norm_x, norm_y
        elif object_type == "player":
            norm_x = (value[0] - LANE_POSITIONS[0]) / (LANE_POSITIONS[-1] - LANE_POSITIONS[0])
            norm_y = PLAYER_Y / SCREEN_HEIGHT
            return norm_x, norm_y
        
    def normalize_distance(self, x, y):
        max_y_distance = np.sqrt(LEVEL_WIDTH**2 + SCREEN_HEIGHT**2)

        norm_x = x / LEVEL_WIDTH
        norm_y = y / max_y_distance

        return norm_x, norm_y
        
    def calculate_normalized_distance(self, player_pos, object_pos):
        player_x, player_y = player_pos
        object_x, object_y = object_pos

        x_dist = player_x - object_x
        y_dist = player_y - object_y

        x_dist, y_dist = self.normalize_distance(x_dist, y_dist)

        return x_dist, y_dist
         
    def reset(self, seed=None):
        super().reset(seed=seed) 
        self.game.restart()
        self.current_reward = 0
        self.dodged_obstacles = []
        self.missed_coins = []
        self.latest_speed = self.game.speed
        return self._get_observation(), {}

    def step(self, action):
        if action == 0: # Do nothing
            self.game.player.x = self.game.player.get_current_positon()
        elif action == 1:  # Move right
            self.game.player.move_right()
        elif action == 2: # move left
            self.game.player.move_left()



        self.game.update(self.game.clock.tick(FRAME_RATE) / 1000.0)
        observation = self._get_observation()
        reward = self._get_reward()
        done = self.game.is_game_over()

        truncated = False

        return observation, reward, done, truncated, {}

    def _get_observation(self):
        player_pos = (self.game.player.get_current_positon(), PLAYER_Y)
        player_x = self.normalize_coordinate("player", player_pos)[0]
        player_x = np.array([player_x], dtype=np.float32)

        score = int(self.game.score)
        speed = int(self.game.speed)
        collected_coins = self.game.collected_coins

        obstacles = np.full((self.num_obstacles*2, ), -1, dtype=np.float32)
        coins = np.full((self.num_coins*2, ), -1, dtype=np.float32)
        obstacles_lane = np.full((self.num_obstacles, ), 0, dtype=np.int32)
        coins_lane = np.full((self.num_coins, ), 0, dtype=np.int32)

        obstacles_y_dist = np.full((self.num_obstacles, ), -1, dtype=np.float32)
        obstacles_x_dist = np.full((self.num_obstacles, ), -1, dtype=np.float32)
        coin_y_dist = np.full((self.num_coins, ), -1, dtype=np.float32)
        coin_x_dist = np.full((self.num_coins, ), -1, dtype=np.float32)

        for index, obstacle in enumerate(self.game.spawnMgr.obstacles):
            if index >= self.num_obstacles:
                break
            if obstacle.y < self.OBSTACLE_Y_CONDITION:
                continue
            norm_x, norm_y = self.normalize_coordinate("obstacle", (obstacle.x, obstacle.y))
            obstacles[index] = norm_x
            obstacles[index +1] = norm_y

            init_spawn_point = obstacle.x - obstacle.x_offset
            lane = LANE_POSITIONS.index(init_spawn_point) +1
            obstacles_lane[index] = lane

            x_dist, y_dist = self.calculate_normalized_distance(player_pos, (obstacle.x, obstacle.y))
            obstacles_x_dist[index] = x_dist
            obstacles_y_dist[index] = y_dist

        for index, coin in enumerate(self.game.spawnMgr.coins):
            if index >= self.num_coins:
                break
            if coin.y < self.COIN_Y_CONDITION:
                continue
            norm_x, norm_y = self.normalize_coordinate("coin", (coin.x, coin.y))
            coins[index] = norm_x
            coins[index +1] = norm_y

            lane = LANE_POSITIONS.index(coin.x) +1
            coins_lane[index] = lane

            x_dist, y_dist = self.calculate_normalized_distance(player_pos, (coin.x, coin.y))
            coin_x_dist[index] = x_dist
            coin_y_dist[index] = y_dist

        observation = {
            "obstacles": obstacles,
            "coins": coins,
            "obstacles_y_dist": obstacles_y_dist,
            "obstacles_x_dist": obstacles_x_dist,
            "coin_y_dist": coin_y_dist,
            "coin_x_dist": coin_x_dist,
            "lane_obstacles": obstacles_lane,
            "lane_coins": coins_lane,
            "score": score,
            "collected_coins": collected_coins,
            "speed": speed,
            "player_pos": player_x
        }

        # print(20 * "=")
        # print("OBSERVATION")
        # print(observation)
        # print(20 * "=" + "\n\n")

        return observation
    

    def _get_reward(self):
        reward = self.current_reward
        speed_factor = self.game.speed / 4 
        coin_reward = 10
        # score_reward = 20
        game_over_penalty = 75
        dodged_obstacle_reward = 5
        coin_missed_penalty = 4

        # Reward for dodging obstacles
        for obstacle in self.game.spawnMgr.obstacles:
            if obstacle.id in self.dodged_obstacles:
                continue
            if obstacle.y >= self.game.player.y +100 and not self.game.is_game_over():
                self.dodged_obstacles.append(obstacle.id)
                reward += dodged_obstacle_reward * speed_factor
                # print("Dodged obstacle")
            
            for id in self.dodged_obstacles:
                if id not in [obstacle.id for obstacle in self.game.spawnMgr.obstacles]:
                    self.dodged_obstacles.remove(id)
                    # print("Removed obstacle id", id)


        # Reward for collecting coins
        if self.game.collected_coins > self.game.last_updated_coins:
            reward += coin_reward * speed_factor
            self.game.last_updated_coins = self.game.collected_coins
            # print("Collected coin")

        # missed coins penalty
        for coin in self.game.spawnMgr.coins:
            if coin.id in self.missed_coins:
                continue
            if coin.y >= self.game.player.y + 20:
                self.missed_coins.append(coin.id)
                reward -= coin_missed_penalty * speed_factor
                # print("Missed coin")
            
            for id in self.missed_coins:
                if id not in [coin.id for coin in self.game.spawnMgr.coins]:
                    self.missed_coins.remove(id)
                             

        # Penalty for game over
        if self.game.is_game_over():
            reward -= game_over_penalty * speed_factor

        self.current_reward = reward
        return int(reward)
    
    def render(self):
        self.game.render()


if __name__ == "__main__":
    env = VVEnv()
    env.reset()
    for _ in range(10):
        done = False
        env.reset()
        steps = 0
        while not done:
            env.render()
            action = 0
            observation, reward, done, truncated, info = env.step(2)
            steps += 1
            if done:
                print(f"{20* '='}\nEPOCH {_ +1} DONE\nREWARD: {reward}\nSTEPS: {steps}\n{20* '='}")
                steps = 0
