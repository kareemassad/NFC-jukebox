import time

from collections.abc import Mapping
from spotify_retry import RetryPolicy, is_retryable_exception


PHONE_DEVICE_TYPES = frozenset(("phone", "smartphone"))


def select_device_id(devices, preferred_device_id=None):
    eligible_device_ids = []

    for device in devices or ():
        if not isinstance(device, Mapping):
            continue

        device_id = device.get("id")
        device_type = device.get("type")

        if not isinstance(device_id, str) or not device_id.strip():
            continue
        if not isinstance(device_type, str) or not device_type.strip():
            continue
        if device_type.strip().lower() in PHONE_DEVICE_TYPES:
            continue

        eligible_device_ids.append(device_id)

    if preferred_device_id in eligible_device_ids:
        return preferred_device_id
    if eligible_device_ids:
        return eligible_device_ids[0]
    return None


def wait_for_device(
    fetch_devices,
    preferred_device_id=None,
    retry_seconds=5,
    retryable_exceptions=(),
    retryable_no_status_exceptions=(),
    max_attempts=12,
    sleep=time.sleep,
    log=print,
):
    policy = RetryPolicy(max_attempts, retry_seconds, sleep, log)
    while policy.start_attempt():
        try:
            devices = fetch_devices()
        except retryable_exceptions as error:
            if not is_retryable_exception(error, retryable_no_status_exceptions):
                raise
            if not policy.wait(
                error,
                retry_message="Spotify device lookup failed: " + str(error),
                exhausted_message="Spotify device lookup failed after maximum attempts.",
            ):
                return None
            continue

        device_id = select_device_id(devices, preferred_device_id)
        if device_id is not None:
            return device_id

        if not policy.wait(
            retry_message="No non-phone Spotify device available. Retrying in 5 seconds.",
            exhausted_message="No non-phone Spotify device available after maximum attempts.",
        ):
            return None

    return None
