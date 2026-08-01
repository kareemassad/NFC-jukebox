import time

from spotify_retry import is_retryable_playback_exception


def play_with_retry(
    play,
    context_uri,
    find_device,
    retry_seconds=5,
    retryable_exceptions=(),
    sleep=time.sleep,
    log=print,
):
    while True:
        device_id = find_device()
        try:
            play(context_uri, device_id)
            return device_id
        except retryable_exceptions as error:
            if not is_retryable_playback_exception(error):
                raise
            log("Spotify playback failed: " + str(error))
            sleep(retry_seconds)
