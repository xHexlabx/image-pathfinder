# setup.py

from setuptools import setup, find_packages

setup(
    name='image-pathfinder',
    version='0.2.0',
    author='คู่หูเขียนโค้ด',
    description='A tool to find a path in a grid-based map from an image.',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'Pillow',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'findpath=scripts.main:run_pathfinder',
            'createmap=scripts.create_map:main',
        ],
    },
)