from spotipy.oauth2 import SpotifyOAuth
import spotipy
import pprint

username = '22wtiqz6ow2wcjaoopq5k4vyy'
scope = 'user-read-playback-state'

#client_credentials_manager = SpotifyClientCredentials()
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

sp.trace = True
user = sp.user(username)
allDevices = sp.devices()
pprint.pprint(allDevices)