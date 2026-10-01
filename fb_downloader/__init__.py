"""
Facebook Video Downloader
~~~~~~~~~~~~~~~~~~~~~~~~~

A lightweight, fast, and dependency-efficient Python library and CLI tool 
to extract and download public Facebook videos and reels in SD and HD qualities.

:copyright: (c) 2026 by Open Source Contributors.
:license: MIT, see LICENSE for more details.
"""

__title__ = "fb-video-downloader"
__description__ = "Fast and reliable Python CLI & library to download public Facebook videos and reels."
__version__ = "1.2.0"
__author__ = "Community Contributors"
__license__ = "MIT"

from .client import FacebookDownloader
from .exceptions import (
    FacebookDownloaderError,
    VideoNotFoundError,
    PrivateVideoError,
    InvalidURLError,
    DownloadError,
)
from .models import VideoInfo, VideoStream

__all__ = [
    "FacebookDownloader",
    "VideoInfo",
    "VideoStream",
    "FacebookDownloaderError",
    "VideoNotFoundError",
    "PrivateVideoError",
    "InvalidURLError",
    "DownloadError",
]
