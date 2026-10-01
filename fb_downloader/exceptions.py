"""Custom exceptions for the Facebook Video Downloader library."""


class FacebookDownloaderError(Exception):
    """Base exception for all errors raised by fb_downloader."""
    pass


class InvalidURLError(FacebookDownloaderError):
    """Raised when the provided URL is not a recognized Facebook video URL."""
    pass


class VideoNotFoundError(FacebookDownloaderError):
    """Raised when the video cannot be found (deleted or invalid ID)."""
    pass


class PrivateVideoError(FacebookDownloaderError):
    """Raised when the video is restricted, private, or requires authentication."""
    pass


class NetworkError(FacebookDownloaderError):
    """Raised when network requests fail or time out."""
    pass


class DownloadError(FacebookDownloaderError):
    """Raised when an error occurs during the video stream download."""
    pass
