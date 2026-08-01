def get_http_status(error):
    status = getattr(error, "http_status", None)
    if status is None:
        response = getattr(error, "response", None)
        status = getattr(response, "status_code", None)
    return status


def is_retryable_exception(error):
    status = get_http_status(error)
    if status is None:
        return True
    if not isinstance(status, int):
        return False

    return status in (408, 429) or 500 <= status < 600


def is_retryable_playback_exception(error):
    return get_http_status(error) == 404 or is_retryable_exception(error)
