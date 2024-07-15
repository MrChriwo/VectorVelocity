import unittest
from gym_vectorvelocity.env import VectorVelocityEnv
import numpy as np

class TestVectorVelocityEnv(unittest.TestCase):
    
    def setUp(self):
        self.env = VectorVelocityEnv(mode='agent')

    def test_env_initialization(self):
        """
        Test the environment initialization
        """
        self.assertIsNotNone(self.env)
        self.assertEqual(self.env.mode, 'agent')

    def test_reset(self):
        """
        Test the reset functionality
        """
        obs, info = self.env.reset()
        self.assertIsNotNone(obs)
        self.assertIsInstance(obs, dict)
        self.assertIn("obstacles", obs)
        self.assertIn("coins", obs)
        self.assertIn("score", obs)
        self.assertIn("player_pos", obs)

    def test_step(self):
        """
        Test stepping through the environment
        """
        self.env.reset()
        obs, reward, done, truncated, info = self.env.step(1)
        self.assertIsInstance(obs, dict)
        self.assertIn("obstacles", obs)
        self.assertIn("coins", obs)
        self.assertIn("score", obs)
        self.assertIn("player_pos", obs)
        self.assertIsInstance(reward, float)
        self.assertIsInstance(done, bool)
        self.assertIsInstance(truncated, bool)

        # Check observation space
        self.check_observation_space(obs)

    def test_action_space(self):
        """
        Test if the action space is correctly defined
        """
        self.assertEqual(self.env.action_space.n, 3)

    def test_observation_space(self):
        """
        Test if the observation space is correctly defined
        """
        obs_space = self.env.observation_space.spaces
        self.assertIn("obstacles", obs_space)
        self.assertIn("coins", obs_space)
        self.assertIn("score", obs_space)
        self.assertIn("player_pos", obs_space)

    def check_observation_space(self, obs):
        """
        Helper function to check if the observation is valid
        """
        self.assertIn("obstacles", obs)
        self.assertIn("coins", obs)
        self.assertIn("score", obs)
        self.assertIn("player_pos", obs)
        self.assertIsInstance(obs["obstacles"], np.ndarray)
        self.assertIsInstance(obs["coins"], np.ndarray)
        self.assertIsInstance(obs["score"], int)
        self.assertIsInstance(obs["player_pos"], np.ndarray)

    def test_random_moves(self):
        """
        Test the environment by running random moves for multiple episodes
        """
        episodes = 10
        for _ in range(episodes):
            obs, info = self.env.reset()
            done = False
            while not done:
                action = self.env.action_space.sample()
                obs, reward, done, truncated, info = self.env.step(action)
                self.assertIsInstance(obs, dict)
                self.assertIsInstance(reward, float)
                self.assertIsInstance(done, bool)
                self.assertIsInstance(truncated, bool)

                self.check_observation_space(obs)

if __name__ == '__main__':
    unittest.main()
