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

   `http://localhost:8888/callback`

3. Open `Read.py` and set the local Spotify and Pushbullet values:

   ```python
   client_id = "your-client-id"
   client_secret = "your-client-secret"
   username = "your-spotify-username"
   pushbullet_api_key = "your-pushbullet-key"
   ```

   The Pushbullet value must be a quoted key. The placeholder in the source causes a `NameError` until it is replaced, or the Pushbullet code is disabled.

4. Keep these values and the Spotify token cache out of Git.

The first run asks for Spotify authorization. Complete the browser flow, then return to the Pi. The Spotify account must have access to the target playback device.

The jukebox skips Spotify devices whose type is `phone` or `smartphone`. It selects an available non-phone Spotify Connect device, such as a computer or speaker. Bluetooth pairing is an operating-system task; pair and test the Pi audio device before starting the jukebox.

## Register tags

Album mappings are stored in `spotifyURICollection.csv`. Add one row for each tag:

```csv
ID,Artist,Album,URI,Count
622616457857,The Beach Boys,Smiley Smile,spotify:album:37rNuexqEXWeSIOiJtn3A9,0
```

`ID` is the tag UID printed by the reader. Make sure the first header is exactly `ID`. Save the CSV as UTF-8 without a BOM so the current reader can parse the header.

`Write.py` can write text to a tag:

```bash
python3 Write.py
```

The written text is not used for album lookup. Playback uses the tag UID and the matching `ID` row in the CSV.

## Run

Activate the virtual environment and start the reader:

```bash
cd /home/pi/git/NFC-jukebox
. .venv/bin/activate
python3 Read.py
```

Then tap a registered tag. Stop the reader with `Ctrl+C`.

`launcher.sh` is also available:

```bash
chmod +x launcher.sh
./launcher.sh
```

The launcher assumes the project is at `/home/pi/git/NFC-jukebox` and uses `sudo`. Edit that path if the project is installed elsewhere. Running `Read.py` directly from the activated environment is the recommended method.

## Troubleshooting

- `ModuleNotFoundError: RPi.GPIO` or `spidev`: install the Pi packages above and recreate the virtual environment with `--system-site-packages`.
- `ModuleNotFoundError: mfrc522`: install the RC522 library that provides `mfrc522.SimpleMFRC522`.
- Spotify authorization fails: check the client ID, client secret, username, and exact redirect URI.
- No audio plays: confirm that Spotify shows the computer or speaker as an available Spotify Connect device. A phone is skipped.
- A tag is not mapped: confirm that its UID is in `spotifyURICollection.csv` and that the first header is exactly `ID`.
