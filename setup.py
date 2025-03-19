from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "Anime Recommender System",
    description = "Anime recommender system",
    version="0.0.1",
    author="Owais Bin Mushtaq",
    packages=find_packages(),
    install_requires = requirements,
)