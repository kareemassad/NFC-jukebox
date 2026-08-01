import unittest

import device_selection
from device_selection import select_device_id


class HttpError(Exception):
    def __init__(self, http_status):
        super().__init__(f"HTTP {http_status}")
        self.http_status = http_status


class SelectDeviceIdTests(unittest.TestCase):
    def test_prefers_existing_non_phone_device(self):
        devices = [
            {"id": "speaker-1", "type": "speaker"},
            {"id": "computer-1", "type": "computer"},
        ]

        self.assertEqual(
            select_device_id(devices, preferred_device_id="computer-1"),
            "computer-1",
        )

    def test_does_not_select_preferred_phone(self):
        devices = [
            {"id": "phone-1", "type": "smartphone"},
            {"id": "speaker-1", "type": "speaker"},
        ]

        self.assertEqual(
            select_device_id(devices, preferred_device_id="phone-1"),
            "speaker-1",
        )

    def test_selects_first_non_phone_device(self):
        devices = [
            {"id": "phone-1", "type": "smartphone"},
            {"id": "computer-1", "type": "computer"},
            {"id": "speaker-1", "type": "speaker"},
        ]

        self.assertEqual(select_device_id(devices), "computer-1")

    def test_phone_filter_is_case_insensitive(self):
        devices = [
            {"id": "phone-1", "type": "SmartPhone"},
            {"id": "speaker-1", "type": "Speaker"},
        ]

        self.assertEqual(select_device_id(devices), "speaker-1")

    def test_returns_none_when_no_eligible_device_exists(self):
        self.assertIsNone(select_device_id([]))
        self.assertIsNone(
            select_device_id([
                {"id": "phone-1", "type": "smartphone"},
                {"id": "phone-2", "type": "phone"},
            ])
        )

    def test_skips_malformed_entries(self):
        devices = [
            None,
            {"id": "missing-type"},
            {"type": "speaker"},
            {"id": "", "type": "speaker"},
            {"id": "speaker-1", "type": "speaker"},
        ]

        self.assertEqual(select_device_id(devices), "speaker-1")

    def test_retries_after_device_lookup_error(self):
        responses = [
            RuntimeError("Spotify is offline"),
            [{"id": "speaker-1", "type": "speaker"}],
        ]
        sleeps = []

        def fetch_devices():
            response = responses.pop(0)
            if isinstance(response, Exception):
                raise response
            return response

        self.assertEqual(
            device_selection.wait_for_device(
                fetch_devices,
                retryable_exceptions=(RuntimeError,),
                sleep=sleeps.append,
                log=lambda message: None,
            ),
            "speaker-1",
        )
        self.assertEqual(sleeps, [5])

    def test_retries_transient_http_error(self):
        responses = [
            HttpError(503),
            [{"id": "speaker-1", "type": "speaker"}],
        ]
        sleeps = []

        def fetch_devices():
            response = responses.pop(0)
            if isinstance(response, Exception):
                raise response
            return response

        self.assertEqual(
            device_selection.wait_for_device(
                fetch_devices,
                retryable_exceptions=(HttpError,),
                sleep=sleeps.append,
                log=lambda message: None,
            ),
            "speaker-1",
        )
        self.assertEqual(sleeps, [5])

    def test_propagates_permanent_http_error(self):
        def fetch_devices():
            raise HttpError(401)

        with self.assertRaises(HttpError):
            device_selection.wait_for_device(
                fetch_devices,
                retryable_exceptions=(HttpError,),
                sleep=lambda seconds: self.fail(
                    "permanent errors must not be retried"
                ),
                log=lambda message: None,
            )

    def test_retries_when_only_phone_devices_are_available(self):
        responses = [
            [{"id": "phone-1", "type": "smartphone"}],
            [{"id": "computer-1", "type": "computer"}],
        ]
        sleeps = []

        def fetch_devices():
            return responses.pop(0)

        self.assertEqual(
            device_selection.wait_for_device(
                fetch_devices,
                sleep=sleeps.append,
                log=lambda message: None,
            ),
            "computer-1",
        )
        self.assertEqual(sleeps, [5])

    def test_propagates_unconfigured_device_lookup_error(self):
        def fetch_devices():
            raise ValueError("invalid device response")

        with self.assertRaises(ValueError):
            device_selection.wait_for_device(
                fetch_devices,
                sleep=lambda seconds: self.fail(
                    "unexpected errors must not be retried"
                ),
                log=lambda message: None,
            )


if __name__ == "__main__":
    unittest.main()
