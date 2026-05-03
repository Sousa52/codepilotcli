from setuptools import setup, find_packages

setup(
    name="ai-assistant",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ai=ai_assistant.cli:main",
        ],
    },
)