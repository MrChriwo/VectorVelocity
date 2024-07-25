import os
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from gymnasium import make
from gym_vectorvelocity import VectorVelocityEnv


def load_and_evaluate(model_path, num_episodes=10):
    """
    Load a pre-trained PPO model and evaluate it for a specified number of episodes.

    Args:
    - model_path (str): Path to the directory containing the saved model.
    - num_episodes (int): Number of episodes to run the evaluation.
    """
    # Load the model
    # path = current directory + model_path
    model_path = os.path.join(os.getcwd(), model_path)

    model = PPO.load(model_path)

    env = make("VectorVelocity-v0", mode="human")

    # Evaluate the model
    episode_rewards = []
    for ep in range(num_episodes):
        obs = env.reset()[0]
        done = False
        total_rewards = 0
        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, rewards, done, truncuated,  info = env.step(action)
            total_rewards += rewards
            env.render()
        episode_rewards.append(total_rewards)
        print(f"Episode {ep + 1}: Total Reward = {total_rewards}")

    # Close the environment
    env.close()

    # Print out results
    print(
        f"Average reward over {num_episodes} episodes: {sum(episode_rewards) / len(episode_rewards)}")


if __name__ == "__main__":
    # Path to the directory where the model is saved
    model_dir = "./notebooks/PPO/baseline_ppo"

    # Number of episodes to evaluate
    num_episodes = 10

    # Call the function
    load_and_evaluate(model_dir, num_episodes)
