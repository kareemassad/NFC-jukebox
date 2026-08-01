import time

from spotify_retry import get_retry_after_seconds, is_retryable_playback_exception


def play_with_retry(
    play,
    context_uri,
    find_device,
    retry_seconds=5,
    retryable_exceptions=(),
    retryable_no_status_exceptions=(),
    max_attempts=12,
    sleep=time.sleep,
    log=print,
):
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    for attempt in range(max_attempts):
        device_id = find_device()
        if device_id is None:
            log("No playback device available after maximum attempts.")
            return None
        try:
            play(context_uri, device_id)
            return device_id
        except retryable_exceptions as error:
            if not is_retryable_playback_exception(
                error, retryable_no_status_exceptions
            ):
                raise
            if attempt + 1 == max_attempts:
                log("Spotify playback failed after maximum attempts.")
                return None
            log("Spotify playback failed: " + str(error))
            sleep(get_retry_after_seconds(error, retry_seconds))

    return None
