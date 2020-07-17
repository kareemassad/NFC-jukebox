import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

urn = "spotify:artist:3jOstUTkEu2JkjvRdBA5Gu"
sp = spotipy.Spotify()

sp.trace = True  # turn on tracing
sp.trace_out = True  # turn on trace out

artist = sp.artist(urn)
print(artist)

user = sp.user("plamere")
print(user)
