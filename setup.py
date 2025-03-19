from setuptools import setup, find_packages
import os

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "Anime Recommender System",
    description = "Anime recommender system",
    author="Owais Bin Mushtaq",
    packages=find_packages(),
    install_requires = requirements,
)