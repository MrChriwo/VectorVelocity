from stable_baselines3 import PPO
from gym_env.env import VVEnv  # Assuming your environment class is named 'VVEnv' and is in 'gym_env.env'

def main():
    # Load the environment
    env = VVEnv("human")

    # Load the pre-trained PPO model
    model = PPO.load("ppo1_vv")

    # Evaluate the agent
    reset = env.reset()
    obs = reset[0]
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, _, info = env.step(action)
        env.render()

        if done: 
            print(obs["score"])


if __name__ == "__main__":
    main()