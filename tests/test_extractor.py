import unittest
from fb_downloader.extractor import FacebookExtractor
from fb_downloader.exceptions import InvalidURLError, VideoNotFoundError, PrivateVideoError


class TestExtractor(unittest.TestCase):
    def test_url_validation(self):
        # Valid formats
        self.assertEqual(
            FacebookExtractor.validate_and_extract_id("https://www.facebook.com/watch/?v=10158498871234567"),
            "10158498871234567"
        )
        self.assertEqual(
            FacebookExtractor.validate_and_extract_id("https://facebook.com/reel/9876543210"),
            "9876543210"
        )
        self.assertEqual(
            FacebookExtractor.validate_and_extract_id("https://fb.watch/abcd1234/"),
            "abcd1234"
        )
        self.assertEqual(
            FacebookExtractor.validate_and_extract_id("https://www.facebook.com/username/videos/112233445566/"),
            "112233445566"
        )

        # Invalid formats
        with self.assertRaises(InvalidURLError):
            FacebookExtractor.validate_and_extract_id("https://youtube.com/watch?v=123")

        with self.assertRaises(InvalidURLError):
            FacebookExtractor.validate_and_extract_id("")

    def test_parse_html_with_hd_and_sd(self):
        mock_html = r"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta property="og:title" content="Awesome Funny Cat Reel" />
            <meta property="og:image" content="https://scontent.cdn.fb.com/thumb.jpg" />
        </head>
        <body>
            <script>
                var data = {
                    "browser_native_hd_url": "https:\/\/video.xx.fbcdn.net\/v\/hd_video.mp4?oh=123\u0026oe=456",
                    "browser_native_sd_url": "https:\/\/video.xx.fbcdn.net\/v\/sd_video.mp4?oh=123\u0026oe=456"
                };
            </script>
        </body>
        </html>
        """
        info = FacebookExtractor.parse_html(mock_html, "https://facebook.com/reel/123", "123")
        self.assertEqual(info.video_id, "123")
        self.assertIn("Cat Reel", info.title)
        self.assertTrue(info.has_hd)
        self.assertTrue(info.has_sd)

        hd_stream = info.get_stream("hd")
        self.assertIsNotNone(hd_stream)
        self.assertIn("hd_video.mp4", hd_stream.url)
        self.assertIn("&oe=456", hd_stream.url)

    def test_parse_html_private_video(self):
        mock_private_html = """
        <html>
            <body>
                <form id="login_form">
                    <input name="email" />
                    <div>Log in to Facebook to see this video</div>
                </form>
            </body>
        </html>
        """
        with self.assertRaises(PrivateVideoError):
            FacebookExtractor.parse_html(mock_private_html, "https://facebook.com/reel/999", "999")

    def test_parse_html_not_found(self):
        mock_empty_html = "<html><head><title>Page Not Found</title></head><body>Nothing here</body></html>"
        with self.assertRaises(VideoNotFoundError):
            FacebookExtractor.parse_html(mock_empty_html, "https://facebook.com/reel/888", "888")


if __name__ == "__main__":
    unittest.main()
