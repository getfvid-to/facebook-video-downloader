import re
import unicodedata
from typing import Dict


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)

DEFAULT_HEADERS: Dict[str, str] = {
    "User-Agent": DEFAULT_USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}


def sanitize_filename(filename: str, max_length: int = 120) -> str:
    """
    Sanitize string to be safe for filenames on Windows, macOS, and Linux.
    """
    filename = unicodedata.normalize("NFKD", filename)
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = re.sub(r"\s+", " ", filename).strip()
    if not filename:
        filename = "facebook_video"
    if len(filename) > max_length:
        filename = filename[:max_length].rstrip()
    return filename


def format_bytes(size: int) -> str:
    """Format bytes into human-readable representation."""
    if size <= 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_idx = 0
    size_f = float(size)
    while size_f >= 1024.0 and unit_idx < len(units) - 1:
        size_f /= 1024.0
        unit_idx += 1
    return f"{size_f:.2f} {units[unit_idx]}"


def print_progress_bar(iteration: int, total: int, prefix: str = "", suffix: str = "", length: int = 40) -> None:
    """Terminal progress bar display."""
    if total <= 0:
        percent = 0.0
        filled_len = 0
    else:
        percent = min(100.0, (iteration / float(total)) * 100.0)
        filled_len = int(length * iteration // total)

    bar = "=" * filled_len + "-" * (length - filled_len)
    print(f"\r{prefix} [{bar}] {percent:.1f}% {suffix}", end="\r", flush=True)
    if total > 0 and iteration >= total:
        print()
