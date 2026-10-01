# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-09-15

### Added
- Improved support for modern Facebook Reels (`facebook.com/reel/...`) and share links (`facebook.com/share/v/...`).
- Added live CLI progress bar with download speed and percentage indicator.
- Streamlined `FacebookDownloader` Python SDK with custom headers and proxy support.

### Changed
- Refactored regex extraction engine for higher reliability against obfuscated script tags.
- Optimized stream chunk buffer size to 1MB for smoother download throughput.

## [1.1.0] - 2026-06-20

### Added
- Added fallback parser for OpenGraph meta tags when JSON streams are inaccessible.
- Added `--info` CLI flag to inspect video streams without initiating download.

## [1.0.0] - 2026-03-10

### Initial Release
- Core video extraction engine supporting SD and HD qualities.
- Command-line tool `fb-dl`.
- Clean unit test suite with mock fixtures.
