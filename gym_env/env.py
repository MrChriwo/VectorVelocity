import sys
import os
cwd = os.getcwd()
sys.path.append(cwd)

from game.settings import FRAME_RATE, SCREEN_HEIGHT, LANE_POSITIONS, MAXIMUM_SPEED, PLAYER_Y, LEVEL_WIDTH
from game.game import Game
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import time 


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

        self.MAX_Y_DISTANCE = np.sqrt(LEVEL_WIDTH**2 + SCREEN_HEIGHT**2)

        self.observation_space = spaces.Dict({
            "obstacles": spaces.Box(low=-1, high=1, shape=(self.num_obstacles*2,), dtype=np.float32),
            "coins": spaces.Box(low=-1, high=1, shape=(self.num_coins*2,), dtype=np.float32),
            "obstacle_dists": spaces.Box(low=-1, high=1, shape=(self.num_obstacles*2,), dtype=np.float32),
            "coin_dists": spaces.Box(low=-1, high=1, shape=(self.num_coins*2,), dtype=np.float32),
            "lane_obstacles": spaces.MultiDiscrete([self.num_lanes +1]*self.num_obstacles ,dtype=np.int32),
            "lane_coins": spaces.MultiDiscrete([self.num_lanes +1]*self.num_coins, dtype=np.int32),
            "score": spaces.Discrete(120000 +1),
            "collected_coins": spaces.Discrete(20000 +1),
            "speed": spaces.Discrete(MAXIMUM_SPEED +1),
            "player_pos": spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)
        })
        self.action_space = spaces.Discrete(3)
        self.latest_speed = self.game.speed

        self.dodged_obstacles = []
        self.missed_coins = []
        self.start_time = time.time()

        # rewards and penaltys
        self.current_reward = 0

        self.game_over_penalty = 75
        self.coin_missed_penalty = 3

        self.dodged_obstacle_reward = 2
        self.coin_reward = 1

    def normalize_obstacle_coordinate(self, value: tuple):
        norm_x = (value[0] - self.OBSTACLE_MIN_X) / (self.OBSTACLE_MAX_X - self.OBSTACLE_MIN_X)
        norm_y = (value[1] + abs(self.OBSTACLE_Y_CONDITION)) / (SCREEN_HEIGHT + abs(self.OBSTACLE_Y_CONDITION))
        return norm_x, norm_y
    
    def normalize_coin_coordinate(self, value: tuple):
        norm_x = (value[0] - LANE_POSITIONS[0]) / (LANE_POSITIONS[-1] - LANE_POSITIONS[0])
        norm_y = (value[1] + abs(self.COIN_Y_CONDITION)) / (SCREEN_HEIGHT + abs(self.COIN_Y_CONDITION))
        return norm_x, norm_y
    
    def normalize_player_coordinate(self, value: tuple):
        norm_x = (value[0] - LANE_POSITIONS[0]) / (LANE_POSITIONS[-1] - LANE_POSITIONS[0])
        norm_y = PLAYER_Y / SCREEN_HEIGHT
        return norm_x, norm_y

        
    def normalize_distance(self, x, y):
        norm_x = x / LEVEL_WIDTH
        norm_y = y / self.MAX_Y_DISTANCE

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
        self.current_reward = 0
        self.dodged_obstacles = []
        self.missed_coins = []
        self.latest_speed = self.game.speed
        self.start_time = time.time()

        self.game.restart()

        return self._get_observation()

    def step(self, action):
        if action == 0: # Do nothing
            self.game.player.stay_in_lane()
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
        player_x = self.normalize_player_coordinate(player_pos)[0]
        player_x = np.array([player_x], dtype=np.float32)

        score = int(self.game.score)
        speed = int(self.game.speed)
        collected_coins = self.game.collected_coins

        obstacles = np.full((self.num_obstacles*2, ), -1, dtype=np.float32)
        coins = np.full((self.num_coins*2, ), -1, dtype=np.float32)
        obstacles_lane = np.full((self.num_obstacles, ), 0, dtype=np.int32)
        coins_lane = np.full((self.num_coins, ), 0, dtype=np.int32)

        obstacles_dists = np.full((self.num_obstacles*2, ), -1, dtype=np.float32)
        coin_dists = np.full((self.num_coins*2, ), -1, dtype=np.float32)

        for index, obstacle in enumerate(self.game.spawnMgr.obstacles):
            if index >= self.num_obstacles:
                break
            if obstacle.y < self.OBSTACLE_Y_CONDITION:
                continue
            norm_x, norm_y = self.normalize_obstacle_coordinate((obstacle.x, obstacle.y))
            obstacles[index] = norm_x
            obstacles[index +1] = norm_y

            init_spawn_point = obstacle.x - obstacle.x_offset
            lane = LANE_POSITIONS.index(init_spawn_point) +1
            obstacles_lane[index] = lane

            x_dist, y_dist = self.calculate_normalized_distance(player_pos, (obstacle.x, obstacle.y))
            obstacles_dists[index] = x_dist
            obstacles_dists[index +1] = y_dist

        for index, coin in enumerate(self.game.spawnMgr.coins):
            if index >= self.num_coins:
                break
            if coin.y < self.COIN_Y_CONDITION:
                continue
            norm_x, norm_y = self.normalize_coin_coordinate((coin.x, coin.y))
            coins[index] = norm_x
            coins[index +1] = norm_y

            lane = LANE_POSITIONS.index(coin.x) +1
            coins_lane[index] = lane

            x_dist, y_dist = self.calculate_normalized_distance(player_pos, (coin.x, coin.y))
            coin_dists[index] = x_dist
            coin_dists[index +1] = y_dist

        observation = {
            "obstacles": obstacles,
            "coins": coins,
            "obstacle_dists": obstacles_dists,
            "coin_dists": coin_dists,
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
    

    def normalize_reward(self, reward):
        return reward / 10

    def _get_reward(self):
        current_time = time.time()
        time_elapsed = current_time - self.start_time
        time_reward = time_elapsed * 0.1
        reward = self.current_reward
        speed_factor = self.game.speed / 4 

        if self.game.is_game_over():
            reward -= self.game_over_penalty * speed_factor
            self.current_reward = reward
            return reward
        
        reward += time_reward

        # Reward for dodging obstacles
        for obstacle in self.game.spawnMgr.obstacles:
            if obstacle.id in self.dodged_obstacles:
                continue
            if obstacle.y >= self.game.player.y +100:
                self.dodged_obstacles.append(obstacle.id)
                reward += self.dodged_obstacle_reward * speed_factor
                # print("Dodged obstacle")
            
        # clean up dodged obstacles
        self.dodged_obstacles = [id for id in self.dodged_obstacles if id in [obstacle.id for obstacle in self.game.spawnMgr.obstacles]]


        # Reward for collecting coins
        if self.game.collected_coins > self.game.last_updated_coins:
            reward += self.coin_reward * speed_factor
            self.game.last_updated_coins = self.game.collected_coins
            # print("Collected coin")

        # missed coins penalty
        for coin in self.game.spawnMgr.coins:
            if coin.id in self.missed_coins:
                continue
            if coin.y >= self.game.player.y + 20:
                self.missed_coins.append(coin.id)
                reward -= self.coin_missed_penalty * speed_factor
                # print("Missed coin")
            
        # clean up missed coins
        self.missed_coins = [id for id in self.missed_coins if id in [coin.id for coin in self.game.spawnMgr.coins]]

        reward = self.normalize_reward(reward)
                             
        self.current_reward = reward
        return reward
    
    def render(self):
        self.game.render()


if __name__ == "__main__":
    env = VVEnv()
    env.reset()

    for _ in range(1000):
        obs = env.reset()
        done = False

        while not done:
            action = env.action_space.sample()
            obs, rewards, done, _, info = env.step(action)
            env.render()

            if done:
                print("Episode finished with reward: ", rewards)
                print("score", obs["score"])
                break