import unittest
from unittest.mock import MagicMock, patch
from fb_downloader.client import FacebookDownloader


class TestClient(unittest.TestCase):
    @patch("requests.Session.get")
    def test_downloader_extract(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = r"""
        <html>
            <meta property="og:title" content="Viral Facebook Video" />
            <script>
                var x = {"browser_native_hd_url": "https:\/\/video.fbcdn.net\/test.mp4"};
            </script>
        </html>
        """
        mock_get.return_value = mock_response

        downloader = FacebookDownloader()
        info = downloader.extract("https://www.facebook.com/watch/?v=123456")

        self.assertEqual(info.video_id, "123456")
        self.assertEqual(info.title, "Viral Facebook Video")
        self.assertTrue(info.has_hd)
        self.assertEqual(info.get_stream("hd").url, "https://video.fbcdn.net/test.mp4")


if __name__ == "__main__":
    unittest.main()
