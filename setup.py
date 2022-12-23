"""Run setuptools."""
from setuptools import find_packages, setup

setup(
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"invokator": ["py.typed"]},
    include_package_data=True,
)
