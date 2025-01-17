from setuptools import setup, find_packages

setup(
    name="anki-today",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    python_requires=">=3.6",
) 