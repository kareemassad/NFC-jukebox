from collections.abc import Mapping


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
