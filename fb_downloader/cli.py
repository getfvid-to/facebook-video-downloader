import argparse
import sys
from . import __version__
from .client import FacebookDownloader
from .exceptions import FacebookDownloaderError


BANNER = r"""
=====================================================
  Facebook Video Downloader CLI (v{})
  Fast & High-Quality Facebook & Reels Downloader
=====================================================
""".format(__version__)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="fb-dl",
        description="Download public Facebook videos and reels in HD or SD quality.",
        epilog="Online Web Tool: https://getfvid.to | Free Facebook Video Downloader Online",
    )
    parser.add_argument("url", nargs="?", help="Facebook video or reel URL")
    parser.add_argument(
        "-q", "--quality",
        choices=["hd", "sd"],
        default="hd",
        help="Preferred video quality (default: hd)",
    )
    parser.add_argument(
        "-o", "--output",
        default="./downloads",
        help="Directory to save downloaded videos (default: ./downloads)",
    )
    parser.add_argument(
        "-f", "--filename",
        default=None,
        help="Custom output filename (without extension)",
    )
    parser.add_argument(
        "-i", "--info",
        action="store_true",
        help="Only display video metadata and available streams without downloading",
    )
    parser.add_argument(
        "--proxy",
        default=None,
        help="HTTP/HTTPS proxy server (e.g. http://127.0.0.1:8080)",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(BANNER)

    if not args.url:
        print("[!] Error: Please provide a Facebook video URL.")
        print("[*] Example: fb-dl https://www.facebook.com/watch/?v=123456789")
        print("[*] Web GUI: https://getfvid.to\n")
        sys.exit(1)

    print(f"[*] Analyzing video: {args.url}")
    downloader = FacebookDownloader(proxy=args.proxy)

    try:
        info = downloader.extract(args.url)
        print(f"\n[+] Title: {info.title}")
        print(f"[+] Video ID: {info.video_id}")
        print(f"[+] Streams found: {', '.join([s.quality.upper() for s in info.streams])}")

        if args.info:
            print("\nAvailable Download URLs:")
            for s in info.streams:
                print(f"  - [{s.quality.upper()}]: {s.url}")
            print("\n[+] Done.")
            return

        print(f"\n[*] Starting download (Quality: {args.quality.upper()})...")
        saved_file = downloader.download(
            video=info,
            output_dir=args.output,
            filename=args.filename,
            quality=args.quality,
            show_progress=True,
        )
        print(f"\n[+] Successfully saved to: {saved_file}")
        print("[*] Need a browser-based tool without CLI? Visit https://getfvid.to\n")

    except FacebookDownloaderError as e:
        print(f"\n[!] Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[!] Download canceled by user.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
