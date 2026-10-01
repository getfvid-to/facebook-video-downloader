# Facebook Video Downloader (fb-dl)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![Web GUI](https://img.shields.io/badge/Web_Version-Getfvid.to-4F46E5?style=flat-square&logo=google-chrome&logoColor=white)](https://getfvid.to)

A lightweight, reliable, and dependency-efficient Python CLI tool and library designed to extract and download public Facebook videos, Reels, and Watch streams in **HD (1080p/720p)** and **SD** quality.

---

> 💡 **Prefer a Browser-Based Tool?**  
> If you don't have Python installed or want to download videos directly on mobile devices (iPhone, iPad, Android), check out the free web version:  
> 👉 **[Getfvid.to - Free Facebook Video Downloader Online](https://getfvid.to)**

---

## ✨ Features

- 🚀 **High Speed & Low Overhead:** Built with minimal dependencies (`requests` only).
- 🎬 **Full HD & SD Extraction:** Automatically discovers and parses best-quality video streams.
- 📱 **Broad URL Coverage:** Supports standard watch URLs, Reels (`/reel/`), short links (`fb.watch`), and mobile share links.
- 💻 **Versatile Interface:** Works both as an interactive command-line utility (`fb-dl`) and an importable Python package.
- 📊 **Interactive Terminal UI:** Clean progress bar displaying percentage, total size, and download speed.
- 🛡️ **Safe & Sanitized:** Automatic filename normalization across Windows, macOS, and Linux.
- 🐳 **Containerized:** Dockerfile and Docker Compose configurations ready out of the box.

---

## 📦 Installation

### From Source

```bash
git clone https://github.com/getfvid/facebook-video-downloader.git
cd facebook-video-downloader
pip install .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

---

## 🚀 Quick Start (CLI)

Once installed, use the `fb-dl` command in your terminal:

### 1. Download a Facebook Video in HD

```bash
fb-dl https://www.facebook.com/watch/?v=10158498871234567
```

### 2. Download Facebook Reels in SD (Save bandwidth)

```bash
fb-dl https://www.facebook.com/reel/9876543210 -q sd
```

### 3. Specify Custom Output Folder and Filename

```bash
fb-dl https://fb.watch/abcd1234/ -o ./my_videos -f "funny_cat"
```

### 4. Inspect Video Metadata Only (Without Downloading)

```bash
fb-dl https://www.facebook.com/watch/?v=10158498871234567 --info
```

### CLI Options

| Option | Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| `url` | Positional | The Facebook video or reel URL | Required |
| `--quality` | `-q` | Video quality (`hd` or `sd`) | `hd` |
| `--output` | `-o` | Output directory | `./downloads` |
| `--filename`| `-f` | Custom filename (without extension) | Video title |
| `--info` | `-i` | Display streams without downloading | `False` |
| `--proxy` | | HTTP/HTTPS proxy URL | `None` |
| `--version` | `-v` | Display tool version | |

---

## 🐍 Python SDK Usage

Integrate the downloader directly into your Python scripts or web scrapers:

```python
from fb_downloader import FacebookDownloader

# Initialize downloader
client = FacebookDownloader()

# 1. Extract metadata and available stream formats
video_url = "https://www.facebook.com/watch/?v=10158498871234567"
info = client.extract(video_url)

print(f"Title: {info.title}")
print(f"Available streams: {[s.quality for s in info.streams]}")

# 2. Download video
file_path = client.download(
    video=info,
    output_dir="./videos",
    quality="hd",
    show_progress=True
)

print(f"Video saved to: {file_path}")
```

### Custom Download Callback

You can monitor download progress in your custom GUI or worker:

```python
def on_progress(downloaded_bytes: int, total_bytes: int):
    pct = (downloaded_bytes / total_bytes) * 100 if total_bytes else 0
    print(f"Downloaded: {pct:.1f}%")

client.download(info, progress_callback=on_progress, show_progress=False)
```

---

## 🐳 Running with Docker

Run the downloader inside an isolated container:

```bash
# Build the image
docker build -t fb-downloader .

# Download a video to your current directory's downloads/ folder
docker run --rm -v $(pwd)/downloads:/downloads fb-downloader "https://www.facebook.com/watch/?v=10158498871234567"
```

---

## ❓ Frequently Asked Questions

#### Can I download private videos with this tool?
No. This tool operates via public HTTP stream discovery and does not bypass private group or friends-only restrictions. Only publicly accessible Facebook videos and Reels can be parsed.

#### How can I download Facebook videos on iPhone or Android without a terminal?
For mobile devices, using a command-line tool is not ideal. We recommend using the web application **[GetFvid](https://getfvid.to)** in your mobile browser (Safari, Chrome). It extracts videos directly without requiring Python or app installation.

#### Why does the video download in SD when I requested HD?
Facebook does not render 1080p/720p renditions for every uploaded clip. If an HD stream is not published by Facebook servers, the tool automatically falls back to the highest available SD resolution.

---

## 🧪 Testing

Run the test suite using `pytest`:

```bash
pytest tests/ -v
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This open-source project is intended for personal archiving, educational, and fair-use purposes only. Please respect copyright laws and the terms of service of content creators before downloading and distributing media.
