# Contributing to Facebook Video Downloader

Thank you for your interest in contributing to **Facebook Video Downloader**! We welcome bug reports, feature suggestions, documentation improvements, and pull requests.

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/getfvid/facebook-video-downloader.git
   cd facebook-video-downloader
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

Run the test suite with `pytest`:
```bash
pytest tests/ -v
```

Run code formatting and linter:
```bash
flake8 fb_downloader tests
black --check fb_downloader tests
```

## Submitting Pull Requests

1. Create a descriptive feature branch (`git checkout -b feature/support-new-reels-url`).
2. Commit your changes with clear, concise commit messages.
3. Push to your branch and open a Pull Request against `main`.
4. Ensure all CI tests pass.

## Community & Resources

- Online web alternative: [Getfvid.to](https://getfvid.to)
- Issue Tracker: [GitHub Issues](https://github.com/getfvid/facebook-video-downloader/issues)
