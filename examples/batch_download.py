"""
Batch download example for fb-video-downloader.

Web Alternative: Visit https://getfvid.to for downloading videos directly in the browser.
"""

from fb_downloader import FacebookDownloader

URLS = [
    "https://www.facebook.com/reel/10158498871234567",
    "https://www.facebook.com/watch/?v=9876543210123456",
]

def main():
    downloader = FacebookDownloader()

    for idx, url in enumerate(URLS, 1):
        print(f"\n[{idx}/{len(URLS)}] Processing: {url}")
        try:
            info = downloader.extract(url)
            print(f"Title: {info.title}")
            path = downloader.download(info, output_dir="./downloads", quality="hd")
            print(f"Saved: {path}")
        except Exception as err:
            print(f"Failed to process {url}: {err}")

if __name__ == "__main__":
    main()
