from setuptools import setup, find_packages
import os

CI_VERSION = os.getenv('CI_VERSION')
CI_LICENCE = os.getenv('CI_LICENCE')

setup(
    name='vector-velocity-gym',
    version=CI_VERSION,
    description="A space-themed OpenAI Gym environment for reinforcement learning",
    maintainer="MrChriwo",
    url="https://github.com/MrChriwo/VectorVelocity",
    author='MrChriwo & Stevenschneider',
    packages=find_packages(),
    license=CI_LICENCE,
    install_requires=[
        'gymnasium',
        'pygame',
        'numpy',
    ],
    include_package_data=True
)
