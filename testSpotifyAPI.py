import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

user = sp.user('22wtiqz6ow2wcjaoopq5k4vyy')

print(user)

#device = sp.devices(user)

#print(device)