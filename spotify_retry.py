def get_http_status(error):
    status = getattr(error, "http_status", None)
    if status is None:
        response = getattr(error, "response", None)
        status = getattr(response, "status_code", None)
    return status


def get_retry_after_seconds(error, default_seconds):
    response = getattr(error, "response", None)
    headers = getattr(response, "headers", None)
    if headers is None:
        headers = getattr(error, "headers", None)
    if not headers:
        return default_seconds

    retry_after = headers.get("Retry-After")
    if retry_after is None:
        retry_after = headers.get("retry-after")
    try:
        return max(0, float(retry_after))
    except (TypeError, ValueError):
        return default_seconds


def is_retryable_exception(error, no_status_exceptions=()):
    status = get_http_status(error)
    if status is None:
        return isinstance(error, no_status_exceptions)
    if not isinstance(status, int):
        return False

    return status in (408, 429) or 500 <= status < 600


def is_retryable_playback_exception(error, no_status_exceptions=()):
    status = get_http_status(error)
    if is_retryable_exception(error, no_status_exceptions):
        return True
    if status != 404:
        return False

    message = " ".join(
        str(getattr(error, attribute, ""))
        for attribute in ("msg", "reason")
    ).lower().replace("_", " ")
    return "no active device" in message or (
        "device" in message
        and (
            "not found" in message
            or "not available" in message
            or "unavailable" in message
        )
    )
