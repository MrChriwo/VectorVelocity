import unittest
import numpy as np
from env import VVEnv 
import time 


## DEPCRECATED 
## CAN NOT BE USED BECAUSE ENVIORNMENT HAS BEEN CHANGED
# TO DO: UPDATE TESTS TO REFLECT NEW ENVIRONMENT

class TestVVEnv(unittest.TestCase):

    def setUp(self):
        self.env = VVEnv(mode='agent')
        self.env.reset()

    def test_initialization(self):
        self.assertIsInstance(self.env, VVEnv)
        self.assertEqual(self.env.current_step, 0)
        self.assertIsNotNone(self.env.game)

    def test_reset(self):
        observation, _ = self.env.reset()
        self.assertIsInstance(observation, dict)
        self.check_observation(observation)

    def test_step(self):
        for _ in range(50000):
            print("starting epoch", _ +1)
            done = False
            self.env.reset()
            steps = 0
            start = time.time()

            while not done:
                self.env.render()
                action = self.env.action_space.sample()
                observation, reward, done, truncated, info = self.env.step(action)
                steps += 1
                self.check_observation(observation)
                self.assertIsInstance(reward, int)
                self.assertIsInstance(done, bool)
                self.assertIsInstance(truncated, bool)
                self.assertIsInstance(info, dict)

                # print(f"Action: {action}, Reward: {reward}, Done: {done}, Truncated: {truncated}")
                # print(f"Observation: {observation}")

                if done:
                    print(f"{20* '='}\nEPOCH {_ +1} DONE\nREWARD: {reward}\nSTEPS: {steps}\nTIME: {time.time() - start} seconds\n{20* '='}")
                    steps = 0

    def check_observation(self, observation):
        # Check player position
        try:
            self.assertTrue(observation['player_pos'] <= self.env.observation_space['player_pos'].n)
            
            # Check obstacles
            self.assertTrue(np.all(observation['obstacles'] >= self.env.observation_space['obstacles'].low))
            self.assertTrue(np.all(observation['obstacles'] <= self.env.observation_space['obstacles'].high))

            # Check coins
            self.assertTrue(np.all(observation['coins'] >= self.env.observation_space['coins'].low))
            self.assertTrue(np.all(observation['coins'] <= self.env.observation_space['coins'].high))

            # Check other discrete spaces
            self.assertTrue(0 <= observation['score'] < self.env.observation_space['score'].n)
            self.assertTrue(0 <= observation['collected_coins'] < self.env.observation_space['collected_coins'].n)
            self.assertTrue(0 <= observation['speed'] < self.env.observation_space['speed'].n)
        except AssertionError:
            print("Observation: ", observation)
            # print which observation is failing
            raise
            

    def test_boundaries(self):
        lowest_action = 0
        highest_action = self.env.action_space.n - 1
        _, _, _, _, _ = self.env.step(lowest_action)
        _, _, _, _, _ = self.env.step(highest_action)
        self.assertIn(lowest_action, range(self.env.action_space.n))
        self.assertIn(highest_action, range(self.env.action_space.n))


if __name__ == '__main__':
    unittest.main()
