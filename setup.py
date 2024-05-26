"""Setup for pyIndego."""
import os
from setuptools import find_packages, setup

current_dir = os.path.dirname(os.path.realpath(__file__))

# Little hack to load the version.py file without loading the __init__.py.
# As that would fail (when deps are not yet installed).
__version__ = None
with open(os.path.join(current_dir, "pyIndego", "version.py"), "r") as fh:
    exec(fh.read())

with open(os.path.join(current_dir, "README.md"), "r") as fh:
    long_description = fh.read()

setup(
    name="pyIndego",
    version=__version__,
    author="jm-73, sander1988",
    author_email="jens@myretyr.se",
    description="API for Bosch Indego mower",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jm-73/pyIndego",
    packages=find_packages("."),
    install_requires=["requests", "aiohttp", "pytz"],
    extras_require={"testing": ["pytest", "pytest-asyncio", "pytest-cov", "mock"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
