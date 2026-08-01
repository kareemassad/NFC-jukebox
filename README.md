# NFC-jukebox

Tap an NFC tag to play its album on Spotify. The project runs on a Raspberry Pi 3B+ with an RC522 reader.

## Required gear

1. Raspberry Pi 3B+
2. RC522 RFID reader
3. NFC/RFID cards or stickers
4. SD card
5. A Spotify Connect computer or speaker

## Hardware setup

Enable SPI on the Pi:

```bash
sudo raspi-config
```

Select **Interface Options**, then **SPI**, then **Enable**.

The included driver expects this wiring. Check your existing wiring before powering the reader.

| RC522 pin | Pi physical pin | Pi signal |
| --- | ---: | --- |
| 3.3V | 1 | 3V3 |
| RST | 22 | GPIO25 |
| GND | 6 | Ground |
| MISO | 21 | GPIO9 |
| MOSI | 19 | GPIO10 |
| SCK | 23 | GPIO11 |
| SDA/SS | 24 | GPIO8 / CE0 |

## Install

From the project directory, install the Pi packages and Python dependencies:

```bash
sudo apt update
sudo apt install -y git python3-pip python3-venv python3-dev python3-rpi.gpio python3-spidev

python3 -m venv --system-site-packages .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The application imports `mfrc522.SimpleMFRC522`. This module is not in `requirements.txt`. Install or copy the RC522 Python library that provides this import before running the project. The included `MFRC522.py` file is the low-level driver and does not provide the `mfrc522` import by itself.

## Configure Spotify

1. Create an application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Add this redirect URI to the application:

   `http://127.0.0.1:8888/callback`

3. Set the local values in the shell that will start the reader:

   ```bash
   export SPOTIFY_CLIENT_ID='your-client-id'
   export SPOTIFY_CLIENT_SECRET='your-client-secret'
   export SPOTIFY_USERNAME='your-spotify-username'
   export PUSHBULLET_API_KEY='your-pushbullet-key'
   ```

   `PUSHBULLET_API_KEY` is optional. Leave it unset to disable notifications.

4. Keep these values and the Spotify token cache out of Git. Do not edit credentials into `Read.py`.

The first run asks for Spotify authorization. Complete the browser flow, then return to the Pi. The account must have Spotify Premium and access to the target playback device.

The jukebox skips Spotify devices whose type is `phone` or `smartphone`. It selects an available non-phone Spotify Connect device, such as a computer or speaker. Pairing a Bluetooth speaker with the Pi does not make it a Spotify Connect device for this project. Use a Spotify Connect device shown by Spotify, or run a separate Spotify Connect client on the Pi.

If `PUSHBULLET_API_KEY` is set, configure at least one Pushbullet target device. If the key is unset or the account has no target device, playback continues without notifications.

## Register tags

Album mappings are stored in `spotifyURICollection.csv`. Add one row for each tag:

```csv
ID,Artist,Album,URI,Count
622616457857,The Beach Boys,Smiley Smile,spotify:album:37rNuexqEXWeSIOiJtn3A9,0
```

`ID` is the tag UID printed by the reader. Make sure the first header is exactly `ID`. The reader loads this file as `cp1252` (Windows-1252). Save the CSV as `cp1252` without a BOM. Plain ASCII text is also safe.

`Write.py` can write text to a tag:

```bash
python3 Write.py
```

The written text is not used for album lookup. Playback uses the tag UID and the matching `ID` row in the CSV.

## Run

Activate the virtual environment and start the reader:

```bash
cd /path/to/NFC-jukebox
. .venv/bin/activate
python3 Read.py
```

Then tap a registered tag. Stop the reader with `Ctrl+C`.

`launcher.sh` is also available:

```bash
chmod +x launcher.sh
./launcher.sh
```

The launcher finds its own project directory and runs `.venv/bin/python`. It does not assume a `pi` account or a fixed clone path. It uses `sudo -E` so the exported configuration values remain available. Running `Read.py` directly from the activated environment is the recommended method.

## Troubleshooting

- `ModuleNotFoundError: RPi.GPIO` or `spidev`: install the Pi packages above and recreate the virtual environment with `--system-site-packages`.
- `ModuleNotFoundError: mfrc522`: install the RC522 library that provides `mfrc522.SimpleMFRC522`.
- `Set SPOTIFY_CLIENT_ID before starting Read.py.`: export all required values in the same shell that starts the reader.
- Spotify authorization fails: check the client ID, client secret, username, and exact loopback redirect URI.
- No audio plays: confirm that Spotify shows the computer or speaker as an available Spotify Connect device. A phone is skipped.
- A tag is not mapped: confirm that its UID is in `spotifyURICollection.csv` and that the first header is exactly `ID`.
