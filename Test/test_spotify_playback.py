import unittest

from spotify_playback import play_with_retry


class PlayWithRetryTests(unittest.TestCase):
    def test_returns_device_after_successful_playback(self):
        attempts = []

        def play(context_uri, device_id):
            attempts.append((context_uri, device_id))

        self.assertEqual(
            play_with_retry(
                play,
                "spotify:album:42",
                lambda: "speaker-1",
                sleep=lambda seconds: None,
                log=lambda message: None,
            ),
            "speaker-1",
        )
        self.assertEqual(
            attempts,
            [("spotify:album:42", "speaker-1")],
        )

    def test_retries_with_a_fresh_device_after_playback_error(self):
        devices = iter(["speaker-1", "computer-1"])
        attempts = []
        sleeps = []

        def find_device():
            return next(devices)

        def play(context_uri, device_id):
            attempts.append((context_uri, device_id))
            if len(attempts) == 1:
                raise RuntimeError("Playback device disconnected")

        self.assertEqual(
            play_with_retry(
                play,
                "spotify:album:42",
                find_device,
                sleep=sleeps.append,
                log=lambda message: None,
            ),
            "computer-1",
        )
        self.assertEqual(
            attempts,
            [
                ("spotify:album:42", "speaker-1"),
                ("spotify:album:42", "computer-1"),
            ],
        )
        self.assertEqual(sleeps, [5])


if __name__ == "__main__":
    unittest.main()
