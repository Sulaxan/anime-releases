import os

from cffi.setuptools_ext import execfile
from setuptools import setup, find_packages


def get_version(version_file):
    glob = {}
    execfile(version_file, glob)
    return glob["__version__"]


def get_requirements():
    with open("requirements.txt") as file:
        requirements = file.readlines()
    return requirements


setup(
    name="anime-releases",
    version=get_version(os.path.join("webhook", "version.py")),
    url="https://github.com/Sulaxan/anime-releases",
    author="Sulaxan",
    license="MIT",
    description="Discord webhook for notifying new anime releases via livechart.me RSS feeds",
    python_requires=">=3.8",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=get_requirements(),
    scripts=["webhook/main.py"],
    setup_requires=[]
)
