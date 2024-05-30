import gymnasium as gym
from gym import spaces
import numpy as np
from settings import FRAME_RATE, SCREEN_HEIGHT, SCREEN_WIDTH
from player import move_left, move_right
from game import Game

class VVEnv(gym.Env):
    metadata = {'render.modes': ['human'], 'render_fps': FRAME_RATE}

    def __init__(self):
        super(VVEnv, self).__init__()

        # Initialize the game
        self.game = Game()
        
        self.clock = self.game.clock
        self.screen = self.game.screen

        # Define the action and observation space
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.screen_height, self.screen_width, 3), dtype=np.uint8)
        self.action_space = spaces.Discrete(3) # Three actions: Do nothing, move left, move right



    def reset(self):
        # Reset the environment and return the initial observation
        pass

    def step(self, action):
        # Perform the given action in the environment and return the next observation, reward, done, and info
        if action == 0: # Do nothing
            pass
        elif action == 1: # Move left
            self.player_pos = move_left(self.player_pos)
        elif action == 2: # Move right
            self.player_pos = move_right(self.player_pos)

    def render(self, mode='human'):
        # Render the environment
        pass