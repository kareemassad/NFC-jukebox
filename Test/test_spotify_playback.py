import unittest

from Test.helpers import HttpError
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
                retryable_exceptions=(RuntimeError,),
                retryable_no_status_exceptions=(RuntimeError,),
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

    def test_retries_when_playback_device_is_missing(self):
        devices = iter(["speaker-1", "computer-1"])
        attempts = []
        sleeps = []

        def find_device():
            return next(devices)

        def play(context_uri, device_id):
            attempts.append((context_uri, device_id))
            if len(attempts) == 1:
                raise HttpError(404, "Device not found")

        self.assertEqual(
            play_with_retry(
                play,
                "spotify:album:42",
                find_device,
                retryable_exceptions=(HttpError,),
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

    def test_propagates_missing_context_404(self):
        def play(context_uri, device_id):
            raise HttpError(404, "Context not found")

        with self.assertRaises(HttpError):
            play_with_retry(
                play,
                "spotify:album:42",
                lambda: "speaker-1",
                retryable_exceptions=(HttpError,),
                sleep=lambda seconds: self.fail(
                    "missing context errors must not be retried"
                ),
                log=lambda message: None,
            )

    def test_honors_retry_after_header(self):
        attempts = []
        sleeps = []

        def play(context_uri, device_id):
            attempts.append(device_id)
            if len(attempts) == 1:
                raise HttpError(429, headers={"Retry-After": "17"})

        self.assertEqual(
            play_with_retry(
                play,
                "spotify:album:42",
                lambda: "speaker-1",
                retryable_exceptions=(HttpError,),
                sleep=sleeps.append,
                log=lambda message: None,
            ),
            "speaker-1",
        )
        self.assertEqual(attempts, ["speaker-1", "speaker-1"])
        self.assertEqual(sleeps, [17.0])

    def test_returns_none_after_max_attempts(self):
        attempts = []
        sleeps = []

        def play(context_uri, device_id):
            attempts.append(device_id)
            raise HttpError(503)

        self.assertIsNone(
            play_with_retry(
                play,
                "spotify:album:42",
                lambda: "speaker-1",
                retryable_exceptions=(HttpError,),
                max_attempts=2,
                sleep=sleeps.append,
                log=lambda message: None,
            )
        )
        self.assertEqual(attempts, ["speaker-1", "speaker-1"])
        self.assertEqual(sleeps, [5])

    def test_propagates_permanent_playback_error(self):
        def play(context_uri, device_id):
            raise HttpError(401)

        with self.assertRaises(HttpError):
            play_with_retry(
                play,
                "spotify:album:42",
                lambda: "speaker-1",
                retryable_exceptions=(HttpError,),
                sleep=lambda seconds: self.fail(
                    "permanent errors must not be retried"
                ),
                log=lambda message: None,
            )


if __name__ == "__main__":
    unittest.main()
