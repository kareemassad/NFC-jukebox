import unittest

from catalog import find_album


class FindAlbumTests(unittest.TestCase):
    def test_returns_album_for_matching_tag_id(self):
        rows = [
            {
                "ID": "42",
                "URI": "spotify:album:42",
                "Artist": "Example Artist",
                "Album": "Example Album",
            }
        ]

        self.assertEqual(
            find_album(rows, 42),
            (
                "spotify:album:42",
                "Example Artist",
                "Example Album",
            ),
        )

    def test_returns_none_for_unknown_tag_id(self):
        rows = [
            {
                "ID": "42",
                "URI": "spotify:album:42",
                "Artist": "Example Artist",
                "Album": "Example Album",
            }
        ]

        self.assertIsNone(find_album(rows, 99))


if __name__ == "__main__":
    unittest.main()
