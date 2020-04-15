from setuptools import setup


with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name="PyTwitch",
    version="1.0.0",
    license="MIT",
    description="A twitch bot I am making on my stream",
    author="vivax",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vivax3794/python_twitch_bot",
    python_requires=">=3.7",
    packages=['PyTwitch']
)
