import os
import time
from typing import Callable, Optional, Union
import requests

from .exceptions import DownloadError, NetworkError
from .extractor import FacebookExtractor
from .models import VideoInfo, VideoStream
from .utils import DEFAULT_HEADERS, format_bytes, print_progress_bar, sanitize_filename


class FacebookDownloader:
    """
    Main client class for fetching Facebook video metadata and downloading media streams.

    Usage:
        downloader = FacebookDownloader()
        info = downloader.extract("https://www.facebook.com/watch/?v=123456789")
        downloader.download(info, quality="hd", output_dir="./downloads")
    """

    def __init__(
        self,
        timeout: int = 15,
        proxy: Optional[str] = None,
        headers: Optional[dict] = None,
    ):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(headers or DEFAULT_HEADERS)
        if proxy:
            self.session.proxies.update({"http": proxy, "https": proxy})

    def extract(self, url: str) -> VideoInfo:
        """
        Extract video information, metadata, and download links from a Facebook URL.

        :param url: URL to the Facebook video/reel/post
        :return: VideoInfo instance containing video metadata and streams
        """
        video_id = FacebookExtractor.validate_and_extract_id(url)

        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Failed to fetch video page: {e}") from e

        return FacebookExtractor.parse_html(response.text, source_url=url, video_id=video_id)

    def download(
        self,
        video: Union[VideoInfo, str],
        output_dir: str = ".",
        filename: Optional[str] = None,
        quality: str = "hd",
        show_progress: bool = True,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> str:
        """
        Download a video stream to local storage.

        :param video: VideoInfo instance or string URL
        :param output_dir: Destination directory
        :param filename: Custom filename (without extension)
        :param quality: Preferred quality ('hd' or 'sd')
        :param show_progress: Display standard CLI progress bar if True
        :param progress_callback: Optional callback(downloaded_bytes, total_bytes)
        :return: Absolute path to the saved file
        """
        if isinstance(video, str):
            video = self.extract(video)

        stream = video.get_stream(quality=quality)
        if not stream:
            raise DownloadError(f"No stream found for quality '{quality}'.")

        # Prepare output directory & filepath
        os.makedirs(output_dir, exist_ok=True)
        base_name = filename if filename else video.title
        safe_name = sanitize_filename(base_name)
        target_path = os.path.join(output_dir, f"{safe_name}_{stream.quality.lower()}.mp4")

        try:
            with self.session.get(stream.url, stream=True, timeout=self.timeout) as resp:
                resp.raise_for_status()
                total_size = int(resp.headers.get("content-length", 0))

                downloaded = 0
                chunk_size = 1024 * 1024  # 1 MB
                start_time = time.time()

                with open(target_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=chunk_size):
                        if not chunk:
                            continue
                        f.write(chunk)
                        downloaded += len(chunk)

                        if progress_callback:
                            progress_callback(downloaded, total_size)

                        if show_progress:
                            elapsed = time.time() - start_time
                            speed = downloaded / elapsed if elapsed > 0 else 0
                            suffix = f"{format_bytes(downloaded)} / {format_bytes(total_size)} ({format_bytes(int(speed))}/s)"
                            print_progress_bar(downloaded, total_size, prefix=f"Downloading [{stream.quality.upper()}]", suffix=suffix)

            return os.path.abspath(target_path)

        except requests.exceptions.RequestException as e:
            if os.path.exists(target_path):
                try:
                    os.remove(target_path)
                except OSError:
                    pass
            raise DownloadError(f"Network error while downloading stream: {e}") from e
        except IOError as e:
            raise DownloadError(f"Disk write error: {e}") from e
