import sys
import os
# path of current working directory
cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cwd)

import gymnasium as gym
from env import VVEnv 

def test_environment(env: VVEnv, episodes=5, mode='human', verbose=False):
    for episode in range(episodes):
        observation = env.reset()
        is_done = False
        total_reward = 0

        while not is_done:
            env.render()
            action = env.action_space.sample()  # Randomly sample an action
            observation, reward, done, info = env.step(action)
            total_reward += reward
            # Print observation and reward to see what's happening
            if verbose:
                print(f"Observation: {observation}")
                print(f"Reward: {reward}, Total Reward: {total_reward}")

            if done:
                print(f"Episode {episode+1} finished with total reward: {total_reward}")
                is_done = True
        
                
if __name__ == "__main__":
    env = VVEnv("human")
    test_environment(env, episodes=150, mode="human")
