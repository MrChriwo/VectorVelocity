from setuptools import setup, find_packages
import os

CI_VERSION = os.getenv('CI_VERSION')
CI_DESCRIPTION = os.getenv('CI_DESCRIPTION')
CI_LICENCE = os.getenv('CI_license')

setup(
    name='vector-velocity-gym',
    version=CI_VERSION,
    description=CI_DESCRIPTION,
    maintainer="MrChriwo",
    url="https://github.com/MrChriwo/VectorVelocity",
    author='MrChriwo & Stevenschneider',
    packages=find_packages(),
    license=CI_LICENCE,
    install_requires=[
        'gym',
        'pygame',
        'numpy',
    ],
    include_package_data=True
)


