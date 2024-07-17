HOW TO
======

This section guides you on how to use the module effectively.

Installation
------------

To install, simply run:

.. code-block:: bash

   pip install vector-velocity-gym

Requirements:
  The module is tested for compatibility with Python versions 3.9 up to 3.12.

Testing Installation
--------------------

To test if the installation was successful:

.. code-block:: python

   from gym_vectorvelocity.utils import test_with_random_moves

   test_with_random_moves()

This function will start the game as an environment, render it, and make random moves inside it.
By default the testing runs for 5 episodes. You can change the number of episodes by passing the `episodes` parameter to the function.

.. code-block:: python

   from gym_vectorvelocity.utils import test_with_random_moves

   test_with_random_moves(episodes=10)


**Note:** This function runs until all episodes are completed. It is recommended to run this function with a small number of episodes.
Execute run in debug mode to manually stop the execution via debugger if needed

Using the Environment
---------------------

To use the environment for your reinforcement training:

.. code-block:: python

   from gym_vectorvelocity import VectorVelocityEnv
   from gymnasium import make

   env = make('VectorVelocity-v0')

This will create a gym environment, simple as that! 😁

Playing as Human
----------------

There is another function in `utils.py` within the `gym_vectorvelocity` module called `play_as_human()`. This function renders the game and makes it interactive for players. The `play_as_human` function accepts two optional parameters:

- `sound_volume`: A float where the user can set up the background sound volume. The default is 0.
- `save_volume`: A boolean that makes the volume setting persistent for restarts.

To play the game as a human:

.. code-block:: python

   from gym_vectorvelocity.utils import play_as_human

   play_as_human(sound_volume=0.5, save_volume=True)