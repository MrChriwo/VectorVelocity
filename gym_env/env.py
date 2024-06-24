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
        
        self.observation_space = spaces.Dict({
            "player_pos": spaces.Discrete(LANE_POSITIONS[-1] +1 ),
            "obstacles": spaces.Box(
                low=np.full((9, 2), [-454, -1], dtype=np.int32),
                high=np.full((9, 2), [SCREEN_HEIGHT + 120, LANE_POSITIONS[-1] + 90], dtype=np.int32),
                dtype=np.int32),
            "coins": spaces.Box(
                low=np.full((40, 2), [-710, -1], dtype=np.int32),
                high=np.full((40, 2), [SCREEN_HEIGHT + 120, LANE_POSITIONS[-1] + 90], dtype=np.int32),
                dtype=np.int32),
            "score": spaces.Discrete(10000),
            "collected_coins": spaces.Discrete(20000),
            "speed": spaces.Discrete(MAXIMUM_SPEED+1)
        })
        self.action_space = spaces.Discrete(3)
        self.latest_speed = self.game.speed
        self.current_reward = 0
        self.dodged_obstacles = []
        self.missed_coins = []

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

        max_obstacles = 9
        max_coins = 40
        obstacles = np.full((max_obstacles, 2), -1, dtype=np.int32)
        coins = np.full((max_coins, 2), -1, dtype=np.int32)

        game_obstacles = np.array([[obstacle.y, obstacle.x] for obstacle in self.game.spawnMgr.obstacles])
        game_coins = np.array([[coin.y, coin.x] for coin in self.game.spawnMgr.coins])
        if game_obstacles.size > 0:
            obstacles[:len(game_obstacles)] = game_obstacles
        if game_coins.size > 0:
            coins[:len(game_coins)] = game_coins


        observation = {
            "player_pos": int(self.game.player.get_current_positon()),
            "obstacles": obstacles,
            "coins": coins,
            "score": int(self.game.score),
            "collected_coins": self.game.collected_coins,
            "speed": int(self.game.speed)
        }

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
