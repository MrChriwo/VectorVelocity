import sys
import os
cwd = os.getcwd()
sys.path.append(cwd)

from game.settings import FRAME_RATE, SCREEN_HEIGHT, SCREEN_WIDTH, LANE_POSITIONS
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
            "player_pos": spaces.Discrete(len(LANE_POSITIONS)),
            "obstacles": spaces.Box(
                low=np.zeros((9, 2), dtype=np.int32),
                high=np.array([[SCREEN_HEIGHT, LANE_POSITIONS[-1]]]*9, dtype=np.int32),  # Replicate the high value
                dtype=np.int32),
            "coins": spaces.Box(
                low=np.zeros((20, 2), dtype=np.int32),
                high=np.array([[SCREEN_HEIGHT, LANE_POSITIONS[-1]]]*20, dtype=np.int32),  # Replicate the high value
                dtype=np.int32),
            "score": spaces.Discrete(np.iinfo(np.int32).max),
            "collected_coins": spaces.Discrete(np.iinfo(np.int32).max)
        })
        self.action_space = spaces.Discrete(3)

    def reset(self):
        self.game.restart()
        return self._get_observation()

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
        return observation, reward, done, {}

    def _get_observation(self):
        obstacles = np.array([[obstacle.y, obstacle.x] for obstacle in self.game.spawnMgr.obstacles])
        coins = np.array([[coin.y, coin.x] for coin in self.game.spawnMgr.coins])
        return {
            "player_pos": self.game.player.get_current_positon(),
            "obstacles": obstacles,
            "coins": coins,
            "score": self.game.score,
            "collected_coins": self.game.collected_coins
        }

    def _get_reward(self):
        reward = 0
        if self.game.collected_coins > self.game.last_updated_coins:
            reward += self.game.collected_coins
            self.game.last_updated_coins = self.game.collected_coins
        if self.game.score % 500 == 0 and self.game.score != 0:
            reward += 500
        if self.game.is_game_over():
            reward -= 1000
        return reward
    
    def render(self):
        self.game.render(self.mode)

