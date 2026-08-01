import unittest

from device_selection import select_device_id


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


if __name__ == "__main__":
    unittest.main()
