# Contribution Guidelines for VectorVelocity

We welcome everyone to join and contribute to VectorVelocity. Your input and creativity are invaluable to us! Here’s how you can get started and contribute effectively:

## Getting Started 🚀

1. **Share Your Idea:** Before you start working, share your idea in the Discussions section to ensure it aligns with the project's goals and to avoid development that might not be merged.
2. **Fork the Repo:** After we have discussed and approved your idea, you can start by forking the repository.
3. **Make Your Changes:** Implement the changes or additions you think are necessary.
4. **Submit a Pull Request:** Once you're done, submit a pull request (PR) for review.


## Pull Request Guidelines ⚙️

For pull requests, we appreciate following the common conventional commit naming conventions. You can find the cheat sheet [here](https://kapeli.com/cheat_sheets/Conventional_Commits.docset/Contents/Resources/Documents/index).

## Repository Structure 🔍

Understanding the repo structure is key to contributing effectively. Here’s an overview:

- **gym_vectorvelocity:** This directory contains the actual source of the Python package.
  - **env.py:** Contains the `VectorVelocityEnv` class, the OpenAI Gym Wrapper for Pygame.

- **gamefolder:** Contains the game itself with the following scripts:
  - **game.py:** The central script where everything comes together (main game loop, etc.).
  - **asset_manager.py:** Manages loading and handling of assets.
  - **player.py:** Controller for the player character.
  - **obstacle.py:** Defines obstacle objects.
  - **coin.py:** Defines coin objects.
  - **ui.py:** Manages the user interface.
  - **spawn_manager.py:** Handles logic for spawning and managing object instances.
  - **level_area.py:** Defines the main level area of the game 

- **game/assets:** Contains assets like images and sounds.
- **game/config:** Contains the settings for the game.

## Contribution Process 🔄

1. **Familiarize Yourself with the Code:** Before making contributions, please take some time to understand the existing codebase and check out the documentation.
2. **Documentation:** Any new functionality added must be reflected in the documentation. 
3. **Testing:** Opening a merge request into the `dev` branch triggers automated testing for Python versions 3.9 up to 3.12 and documentation testing for any changes.
4. **Encapsulation and Maintenance:** Ensure your code is encapsulated well for easier maintenance. Clean code is always appreciated.
5. **Unit Tests:** If your changes impact functionality, ensure that new or changed functionality is reflected in the tests/ folder so that unit tests can properly test the functionality.
6. **Review Process:** Be open to feedback during the PR review process. It's a collaborative effort to maintain and improve the project.

## Additional Points ➕

- **Consistency:** Maintain coding style and conventions used in the existing codebase.
- **Unit Tests:** Adding unit tests for new features or bug fixes is highly recommended.
- **Review Process:** Be open to feedback during the PR review process. It's a collaborative effort to maintain and improve the project.

We highly value your contributions and are excited to see what you will bring to the VectorVelocity project. Thank you for being a part of our journey! ❤️
