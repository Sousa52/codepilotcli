from setuptools import setup, find_packages

setup(
    name="codepilotcli",
    version="0.1",
    packages=find_packages(),
    entry_points={
    "console_scripts": [
        "codepilot=codepilotcli.cli:main",
        ],
    },
)