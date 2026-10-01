"""
Basic usage example for fb-video-downloader.

Web Alternative: If you need an instant web tool without code:
Visit https://getfvid.to - Free Online Facebook Downloader
"""

from fb_downloader import FacebookDownloader

def main():
    downloader = FacebookDownloader()

    # Target URL
    video_url = "https://www.facebook.com/watch/?v=10158498871234567"

    print(f"Extracting info for: {video_url}")
    try:
        info = downloader.extract(video_url)
        print(f"Found Video: {info.title}")
        print(f"Has HD Stream: {info.has_hd}")

        # Download HD version
        output_path = downloader.download(
            video=info,
            output_dir="./downloads",
            quality="hd",
        )
        print(f"Downloaded successfully to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
