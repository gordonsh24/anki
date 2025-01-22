from setuptools import setup, find_packages

setup(
    name="anki-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.31.0",
        "dependency-injector>=4.45.0",
        "typer[all]>=0.15.1",
    ],
    entry_points={
        "console_scripts": [
            "anki=src.cli:app",
        ],
    },
) 