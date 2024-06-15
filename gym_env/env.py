import sys
import os
cwd = os.getcwd()
sys.path.append(cwd)

from game.settings import FRAME_RATE, SCREEN_HEIGHT, LANE_POSITIONS, MAXIMUM_SPEED
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
        
        # Define the action and observation space
        self.observation_space = spaces.Dict({
            "player_pos": spaces.Discrete(LANE_POSITIONS[-1]),
            "obstacles": spaces.Box(
                low=np.zeros((9, 2), dtype=np.int32),
                high=np.array([[SCREEN_HEIGHT, LANE_POSITIONS[-1]]]*9, dtype=np.int32),
                dtype=np.int32),
            "coins": spaces.Box(
                low=np.zeros((20, 2), dtype=np.int32),
                high=np.array([[SCREEN_HEIGHT, LANE_POSITIONS[-1]]]*20, dtype=np.int32),
                dtype=np.int32),
            "score": spaces.Discrete(np.iinfo(np.int32).max),
            "collected_coins": spaces.Discrete(np.iinfo(np.int32).max),
            "speed": spaces.Box(low=4.0, high=MAXIMUM_SPEED, shape=(1,), dtype=np.float32)

        })
        self.action_space = spaces.Discrete(3)
        self.latest_speed = self.game.speed

    def reset(self, seed=None):
        super().reset(seed=seed) 
        self.game.restart()
        return self._get_observation(), {}

    def step(self, action):

        if action == 1:  # Move left
            self.game.player.move_left()
        elif action == 2:  # Move right
            self.game.player.move_right()
        elif action == 0: # Do nothing
            pass

        self.game.update(self.game.clock.tick(FRAME_RATE) / 1000.0)
        observation = self._get_observation()
        reward = self._get_reward()
        done = self.game.is_game_over()
        truncated = False

        return observation, reward, done, truncated, {}

    def _get_observation(self):
        obstacles = np.array([[obstacle.y, obstacle.x] for obstacle in self.game.spawnMgr.obstacles])
        coins = np.array([[coin.y, coin.x] for coin in self.game.spawnMgr.coins])

        if len(obstacles) == 0:
            obstacles = np.zeros((9, 2), dtype=np.int32)
        if len(coins) == 0:
            coins = np.zeros((20, 2), dtype=np.int32)

        observation = {
            "player_pos": self.game.player.get_current_positon(),
            "obstacles": obstacles,
            "coins": coins,
            "score": int(self.game.score),
            "collected_coins": self.game.collected_coins,
            "speed": np.array([self.game.speed], dtype=np.float32)
        }
        return observation

    def _get_reward(self):
        reward = 0
        speed_factor = self.game.speed / 4 
        coin_reward = 10
        score_reward = 20
        game_over_penalty = 75
        dodged_obstacle_reward = 5

        # Reward for dodging obstacles
        for obstacle in self.game.spawnMgr.obstacles:
            if obstacle.y > self.game.player.y:
                reward += dodged_obstacle_reward * speed_factor

        # Reward for collecting coins
        if self.game.collected_coins > self.game.last_updated_coins:
            reward += coin_reward * speed_factor
            self.game.last_updated_coins = self.game.collected_coins

        # Reward for reaching score milestones
        if int(self.game.score) % 500 == 0 and self.game.score != 0:
            reward += score_reward * speed_factor

        # Penalty for game over
        if self.game.is_game_over():
            reward -= game_over_penalty * speed_factor
        return reward
    
    def render(self):
        self.game.render(self.mode)

