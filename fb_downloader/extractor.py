import re
from typing import List, Optional
from urllib.parse import urlparse, parse_qs

from .exceptions import InvalidURLError, VideoNotFoundError, PrivateVideoError
from .models import VideoInfo, VideoStream


class FacebookExtractor:
    """Extracts video stream metadata and direct media URLs from Facebook HTML payloads."""

    FB_PATTERNS = [
        r"(?:https?:\/\/)?(?:www\.|m\.|web\.)?facebook\.com\/(?:watch\/?\?v=|v\/|video\.php\?v=|reel\/|reel\?v=|share\/v\/|share\/r\/|.*?\/videos\/)(\d+)",
        r"(?:https?:\/\/)?(?:www\.|m\.|web\.)?facebook\.com\/(?:[a-zA-Z0-9.\-_]+)\/videos\/(\d+)",
        r"(?:https?:\/\/)?fb\.watch\/([a-zA-Z0-9_\-]+)",
    ]

    @classmethod
    def validate_and_extract_id(cls, url: str) -> str:
        """Validate Facebook video URL and attempt to extract video ID or unique slug."""
        if not url:
            raise InvalidURLError("The URL cannot be empty.")

        url = url.strip()
        parsed = urlparse(url)
        if not parsed.netloc:
            raise InvalidURLError(f"Invalid URL structure: {url}")

        for pattern in cls.FB_PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        # Handle general facebook.com URLs with ?v= query param
        if "facebook.com" in parsed.netloc or "fb.watch" in parsed.netloc:
            qs = parse_qs(parsed.query)
            if "v" in qs and qs["v"]:
                return qs["v"][0]
            # Fallback slug
            path_parts = [p for p in parsed.path.split("/") if p]
            if path_parts:
                return path_parts[-1]

        raise InvalidURLError(f"URL is not a recognized Facebook video link: {url}")

    @classmethod
    def clean_json_url(cls, raw_url: str) -> str:
        """Decode common JSON and HTML escaped characters in extracted URLs."""
        if not raw_url:
            return ""
        cleaned = raw_url.replace(r"\/", "/").replace("\\u0026", "&").replace("&amp;", "&")
        # Remove any surrounding quotes or backslashes
        cleaned = cleaned.strip("\"'\\")
        return cleaned

    @classmethod
    def parse_html(cls, html_content: str, source_url: str, video_id: str) -> VideoInfo:
        """Parse raw HTML content from Facebook and return a VideoInfo instance."""
        if not html_content:
            raise VideoNotFoundError("Received empty HTML payload from Facebook.")

        # Check for typical private/login required markers
        if "login_form" in html_content and "browser_native_sd_url" not in html_content and "playable_url" not in html_content:
            if "Log in to Facebook" in html_content or "You must log in to continue" in html_content:
                raise PrivateVideoError(
                    "This video appears to be private, restricted, or requires an active Facebook login."
                )

        streams: List[VideoStream] = []

        # 1. Search for HD Stream
        hd_url = cls._extract_pattern(html_content, [
            r'"browser_native_hd_url"\s*:\s*"([^"]+)"',
            r'"playable_url_quality_hd"\s*:\s*"([^"]+)"',
            r'hd_src\s*:\s*"([^"]+)"',
            r'"hd_src_no_ratelimit"\s*:\s*"([^"]+)"',
            r'hd_src_no_ratelimit:"([^"]+)"',
        ])
        if hd_url:
            cleaned_hd = cls.clean_json_url(hd_url)
            streams.append(VideoStream(quality="hd", url=cleaned_hd, resolution="720p/1080p"))

        # 2. Search for SD Stream
        sd_url = cls._extract_pattern(html_content, [
            r'"browser_native_sd_url"\s*:\s*"([^"]+)"',
            r'"playable_url"\s*:\s*"([^"]+)"',
            r'sd_src\s*:\s*"([^"]+)"',
            r'"sd_src_no_ratelimit"\s*:\s*"([^"]+)"',
            r'sd_src_no_ratelimit:"([^"]+)"',
        ])
        if sd_url:
            cleaned_sd = cls.clean_json_url(sd_url)
            # Avoid duplicate if HD and SD matched the exact same link
            if not any(s.url == cleaned_sd for s in streams):
                streams.append(VideoStream(quality="sd", url=cleaned_sd, resolution="360p/480p"))

        # 3. Fallback: OpenGraph meta tags
        if not streams:
            og_video = cls._extract_pattern(html_content, [
                r'<meta\s+property="og:video"\s+content="([^"]+)"',
                r'<meta\s+property="og:video:url"\s+content="([^"]+)"',
                r'<meta\s+property="og:video:secure_url"\s+content="([^"]+)"',
            ])
            if og_video:
                cleaned_og = cls.clean_json_url(og_video)
                streams.append(VideoStream(quality="sd", url=cleaned_og, resolution="standard"))

        if not streams:
            raise VideoNotFoundError(
                f"Could not locate playable video streams for video ID {video_id}. "
                "The video might be removed, geo-restricted, or set to private."
            )

        # Extract title / description
        title = cls._extract_pattern(html_content, [
            r'<meta\s+property="og:title"\s+content="([^"]+)"',
            r'<title>([^<]+)<\/title>',
        ])
        if title:
            title = cls.clean_json_url(title).replace(" | Facebook", "").strip()
        else:
            title = f"Facebook_Video_{video_id}"

        # Extract thumbnail
        thumbnail = cls._extract_pattern(html_content, [
            r'<meta\s+property="og:image"\s+content="([^"]+)"',
            r'"preferred_thumbnail"\s*:\s*\{"image"\s*:\s*\{"uri"\s*:\s*"([^"]+)"',
        ])
        if thumbnail:
            thumbnail = cls.clean_json_url(thumbnail)

        return VideoInfo(
            video_id=video_id,
            source_url=source_url,
            title=title or f"FB_Video_{video_id}",
            thumbnail_url=thumbnail,
            streams=streams,
        )

    @staticmethod
    def _extract_pattern(content: str, patterns: List[str]) -> Optional[str]:
        """Try multiple regex patterns in order and return the first matching group."""
        for pattern in patterns:
            match = re.search(pattern, content)
            if match and match.group(1):
                return match.group(1)
        return None
