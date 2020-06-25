import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyIndego",
    version="2.0.12",
    author="jm-73",
    author_email="jens@myretyr.se",
    description="API for Bosch Indego mower",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jm-73/pyIndego",
    packages=setuptools.find_packages(),
    install_requires=["requests", "aiohttp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
