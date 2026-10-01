from setuptools import setup, find_packages

setup(
    name="fb-video-downloader",
    version="1.2.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "fb-dl=fb_downloader.cli:main",
        ],
    },
)
