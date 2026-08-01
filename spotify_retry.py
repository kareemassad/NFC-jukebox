import math
import time


class RetryPolicy:
    def __init__(
        self,
        max_attempts=12,
        retry_seconds=5,
        sleep=time.sleep,
        log=print,
    ):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.max_attempts = max_attempts
        self.retry_seconds = retry_seconds
        self.sleep = sleep
        self.log = log
        self.attempts = 0

    def start_attempt(self):
        if self.attempts >= self.max_attempts:
            return False
        self.attempts += 1
        return True

    def wait(
        self,
        error=None,
        retry_message=None,
        exhausted_message=None,
    ):
        if self.attempts >= self.max_attempts:
            if exhausted_message:
                self.log(exhausted_message)
            return False
        if retry_message:
            self.log(retry_message)
        delay = self.retry_seconds
        if error is not None:
            delay = get_retry_after_seconds(error, self.retry_seconds)
        self.sleep(delay)
        return True


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
        delay = float(retry_after)
    except (TypeError, ValueError):
        return default_seconds
    if not math.isfinite(delay):
        return default_seconds
    return max(0, delay)


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
