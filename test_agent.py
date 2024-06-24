from stable_baselines3 import PPO
from gym_env.env import VVEnv  # Assuming your environment class is named 'VVEnv' and is in 'gym_env.env'

def main():
    # Load the environment
    env = VVEnv()

    # Load the pre-trained PPO model
    model = PPO.load("ppo_vv")

    done = False

    for _ in range(1000):
        obs = env.reset()
        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, rewards, done, _, info = env.step(action)
            env.render()
        done = False

if __name__ == "__main__":
    main()
