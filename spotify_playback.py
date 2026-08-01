import time

from spotify_retry import RetryPolicy, is_retryable_playback_exception


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
    policy = RetryPolicy(max_attempts, retry_seconds, sleep, log)
    while policy.start_attempt():
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
            if not policy.wait(
                error,
                retry_message="Spotify playback failed: " + str(error),
                exhausted_message="Spotify playback failed after maximum attempts.",
            ):
                return None

    return None
