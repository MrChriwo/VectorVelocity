import gym
from gym import spaces
import numpy as np
import pygame
from game import Game
import settings

class VectorVelocityEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        super(VectorVelocityEnv, self).__init__()
        
        # Initialize the game
        self.game = Game()
        
        # Define the action and observation space
        # Actions: 0 = do nothing, 1 = move left, 2 = move right
        self.action_space = spaces.Discrete(3)
        
        # Observations: player position (x, y), obstacles (x, y) and coins (x, y)
        # Flatten the observations for simplicity
        self.max_obstacles = 3
        self.max_coins = 20
        self.observation_space = spaces.Box(
            low=0,
            high=max(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
            shape=(1 + self.max_obstacles + self.max_coins, 2),
            dtype=np.float32
        )
        
        # Initialize reward
        self.reward = 0
        self.done = False
        
    def reset(self):
        # Reset the game
        self.game = Game()
        self.reward = 0
        self.done = False
        return self._get_observation()
    
    def step(self, action):
        # Execute action
        if action == 1:
            self.game.player.move_left()
        elif action == 2:
            self.game.player.move_right()
        
        # Update the game state
        dt = self.game.clock.tick(settings.FRAME_RATE) / 1000.0
        self.game.update(dt)
        
        # Calculate reward
        coins_collected = self.game.spawnMgr.collected_coins
        self.reward += coins_collected
        
        # Update the 'done' flag based on whether the game is running or not
        self.done = not self.game.running
        
        # Get the current observation
        observation = self._get_observation()
        
        return observation, self.reward, self.done, {}
    
    def render(self, mode='human', close=False):
        if close:
            pygame.quit()
        else:
            self.game.draw()
    
    def _get_observation(self):
        player_pos = (self.game.player.x, self.game.player.y)
        obstacles_pos = [(obstacle.x, obstacle.y) for obstacle in self.game.spawnMgr.obstacles]
        coins_pos = [(coin.x, coin.y) for coin in self.game.spawnMgr.coins]
        
        # Ensure consistent observation shape
        obstacles_pos += [(0, 0)] * (self.max_obstacles - len(obstacles_pos))
        coins_pos += [(0, 0)] * (self.max_coins - len(coins_pos))
        
        all_pos = [player_pos] + obstacles_pos[:self.max_obstacles] + coins_pos[:self.max_coins]
        return np.array(all_pos, dtype=np.float32)
    
    def seed(self, seed=None):
        np.random.seed(seed)
        if seed is not None:
            pygame.init()
            pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"code": "reset"}))

# Example usage
if __name__ == "__main__":
    env = VectorVelocityEnv()
    obs = env.reset()
    
    for _ in range(1000):
        action = env.action_space.sample()  # Random action
        obs, reward, done, info = env.step(action)
        env.render()
        
        if done:
            break
    
    env.close()