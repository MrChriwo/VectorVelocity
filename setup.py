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
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=('tests', 'tests.*')),
    license=CI_LICENCE,
    install_requires=[
        'gymnasium',
        'pygame',
        'numpy',
    ],
    include_package_data=True
)
