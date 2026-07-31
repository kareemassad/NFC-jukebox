# NFC Jukebox: Non-Phone Spotify Device Selection

Date: 2026-07-31

Status: Approved design, pending written-spec review

## Context

The jukebox reads an NFC tag, looks up the matching Spotify album, and starts playback on an available Spotify device. `Read.py` currently prefers one hard-coded device ID and otherwise returns the first device. The current code assumes that the device list is not empty. It does not exclude phones. A missing device or a temporary Spotify error can stop the long-running reader loop.

The Spotify Web API exposes a device `type`, such as `smartphone`, `computer`, or `speaker`. The available-device response is documented at [Get a User's Available Devices](https://developer.spotify.com/documentation/web-api/reference/get-a-users-available-devices).

The project will continue to use Spotify Connect. This change will not add direct Bluetooth pairing or local audio-device management.

## Goals

- Keep the NFC-to-Spotify user flow unchanged.
- Keep the existing preferred device behavior when that device is available and is not a phone.
- Select the first available non-phone device when the preferred device is unavailable.
- Keep the reader process alive when no eligible device is available.
- Recover from temporary device-list and playback errors without terminating the reader loop.
- Make device selection independent from Raspberry Pi hardware so it can be tested.

## Non-goals

- Add artificial intelligence features.
- Pair or reconnect Bluetooth devices on the Raspberry Pi.
- Replace Spotify Connect with local audio playback.
- Change the NFC tag format or the CSV catalog.
- Add a web interface.
- Change Spotify authentication or notification behavior.

## Design

### Device selection

Add a pure device-selection function. The function will receive the Spotify device list and the existing preferred device ID. It will return a device ID or `None`.

The function will apply this policy:

1. Ignore entries that are not mappings or that do not have a non-empty string device ID and device type.
2. Exclude device types `smartphone` and `phone`, with case-insensitive comparison.
3. Return the existing preferred device ID when it is in the eligible list.
4. Otherwise return the first eligible device ID in the order returned by Spotify.
5. Return `None` when no eligible device exists.

The function will not guess a device type from the device name. This keeps the rule predictable.

### Runtime recovery

The Spotify device lookup will use the selector function. When the selector returns `None`, the runtime will log that no non-phone device is available, wait for a short fixed retry interval, and try again. It will not select a phone as a fallback.

The retry interval will be five seconds. When Spotify raises an API or network error while listing devices or starting playback, the runtime will catch the error, log the failure, wait five seconds, and keep the reader process alive. The next attempt will request a fresh device list.

The existing GPIO cleanup path will remain in a `finally` block so shutdown still releases the RC522 resources.

### Code boundaries

- `device_selection.py` will contain the pure selection rule.
- `Read.py` will keep the NFC loop and Spotify integration. It will call the selection rule and handle retry behavior.
- A standard-library test module will cover the selection rule without importing Raspberry Pi or Spotify libraries.

## Error handling

- Unknown NFC IDs will be logged and skipped without indexing into a missing album record.
- An empty Spotify device list will not cause an index error.
- Phone-only device lists will not cause playback on a phone.
- Temporary Spotify failures will not terminate the NFC reader process.
- PushBullet notifications will be sent only after playback starts successfully.

## Testing

The tests will cover:

- A preferred non-phone device.
- A preferred phone device with another eligible device available.
- Selection of the first eligible device.
- Case-insensitive phone filtering.
- Empty device lists.
- Phone-only device lists.
- Entries with missing IDs or types.
- Malformed device entries that do not stop selection.

The implementation will not require live Spotify credentials, an RC522 reader, a Raspberry Pi, or an active audio device for these tests.

## Operational impact

The NFC workflow and Spotify Connect output remain the same. The main behavior change is that the process waits for an eligible non-phone Spotify device instead of selecting a phone or crashing when the device list is empty. Direct Bluetooth behavior remains outside this change.
