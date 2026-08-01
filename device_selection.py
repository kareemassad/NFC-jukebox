import time

from collections.abc import Mapping


PHONE_DEVICE_TYPES = frozenset(("phone", "smartphone"))


def is_retryable_exception(error, retryable_exceptions):
    if not isinstance(error, retryable_exceptions):
        return False

    status = getattr(error, "http_status", None)
    if status is None:
        response = getattr(error, "response", None)
        status = getattr(response, "status_code", None)
    if status is None:
        return True
    if not isinstance(status, int):
        return False

    return status == 429 or 500 <= status < 600


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
    sleep=time.sleep,
    log=print,
):
    while True:
        try:
            devices = fetch_devices()
        except retryable_exceptions as error:
            if not is_retryable_exception(error, retryable_exceptions):
                raise
            log("Spotify device lookup failed: " + str(error))
            sleep(retry_seconds)
            continue

        device_id = select_device_id(devices, preferred_device_id)
        if device_id is not None:
            return device_id

        log("No non-phone Spotify device available. Retrying in 5 seconds.")
        sleep(retry_seconds)
