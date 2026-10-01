from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class VideoStream:
    """Represents an extracted video stream (HD or SD)."""
    quality: str  # 'hd' or 'sd'
    url: str
    resolution: Optional[str] = None
    filesize_approx: Optional[int] = None

    def __repr__(self) -> str:
        return f"<VideoStream quality={self.quality.upper()} url={self.url[:30]}...>"


@dataclass
class VideoInfo:
    """Detailed metadata for a Facebook video."""
    video_id: str
    source_url: str
    title: str = "Facebook Video"
    description: Optional[str] = None
    duration_seconds: Optional[int] = None
    thumbnail_url: Optional[str] = None
    streams: List[VideoStream] = field(default_factory=list)

    @property
    def has_hd(self) -> bool:
        return any(s.quality.lower() == "hd" for s in self.streams)

    @property
    def has_sd(self) -> bool:
        return any(s.quality.lower() == "sd" for s in self.streams)

    def get_stream(self, quality: str = "hd") -> Optional[VideoStream]:
        """
        Get the preferred stream by quality ('hd' or 'sd').
        Falls back to available stream if requested quality is not found.
        """
        quality = quality.lower()
        # Direct match
        for s in self.streams:
            if s.quality.lower() == quality:
                return s
        # Fallback
        if self.streams:
            return self.streams[0]
        return None
