import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import cred
import json

# Authentication - without user
# client_credentials_manager = SpotifyClientCredentials('9113128046364c78addccdfa39939cb0',
#                                                       '20f434b1adb14bf096f25a65b582fcc1')

username = sys.argv[0]


# might need to change scope
scope = "user-read-recently-played user-modify-playback-state user-read-private user-read-playback-state"

# token = spotipy.util.prompt_for_user_token(username, scope)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=cred.client_ID,
        client_secret=cred.client_SECRET,
        redirect_uri=cred.redirect_url,
        scope=scope,
    )
)


track = sp.search("Chaleya", type="album")
# Using json.dump() to write data to the file
with open("../song.json", "w") as json_file:
    json.dump(track, json_file, indent="\t")


# the ouput of this code is presented in song.json
