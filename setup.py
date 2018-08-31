from distutils.core import setup

setup(
    name="Zookeeper",
    version="0.1",
    author="Dr. Dos",
    author_email="doctordos@gmail.com",
    url="https://github.com/DrDos0016/zookeeper",
    license="GPL 3",
    description="A Python library for parsing, analyzing, and modifying ZZT worlds.",
    long_description=open('README', 'r').read(),
    packages=["zookeeper",],
    package_data={
        "zookeeper": ["charsets/*.png", "palettes/*.dat"],
    },
)
