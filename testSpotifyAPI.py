from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pprint

username = '22wtiqz6ow2wcjaoopq5k4vyy'

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#sp.trace = True
user = sp.user(username)
pprint.pprint(user)