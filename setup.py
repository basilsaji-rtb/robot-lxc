import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name = "RobotLxcLibrary",
        version = "0.0.1",
        author = "Basil Saji",
        author_email = "sajibasil@gmail.com",
        description = ("Robotframework library for creating and destroying LXC containers"),
        license = "BSD",
        keywords = "robotframework lxc container robot keyword library",
        url = "None",
        packages = ['RobotLxcLibrary'],
        long_description=read('README'),
)
