import time


def play_with_retry(
    play,
    context_uri,
    find_device,
    retry_seconds=5,
    sleep=time.sleep,
    log=print,
):
    while True:
        device_id = find_device()
        try:
            play(context_uri, device_id)
            return device_id
        except Exception as error:
            log("Spotify playback failed: " + str(error))
            sleep(retry_seconds)
