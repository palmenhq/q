import os

import requests
import spotipy
import spotipy.oauth2
import spotipy.util
import yaml

SCOPES = ' '.join([
    'playlist-read-private',
    'playlist-modify-public',
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    'app-remote-control',
])

_BASE_URL = 'https://api.spotify.com'


class Spotify:
    token = None
    _client = None
    _credentials = None

    def __init__(self):
        self._credentials = self._load_credentials()
        try:
            self._client = spotipy.Spotify(auth=self._credentials['auth'])
            self._client.me()
        except:
            self.login_user()
            self._client = spotipy.Spotify(auth=self._credentials['auth'])
        self.token = self._credentials['auth']

    def login_user(self):
        token = spotipy.util.prompt_for_user_token(self._credentials['username'], SCOPES,
                                                   client_id=self._credentials['client_id'],
                                                   client_secret=self._credentials['client_secret'],
                                                   redirect_uri='http://localhost:1337/callback',
                                                   cache_path=os.path.expanduser(f"~/.q/spotify-cache-{self._credentials['username']}"))
        with open(os.path.expanduser("~/.q/spotify_credentials"), 'w') as stream:
            self._credentials['auth'] = token
            yaml.safe_dump(self._credentials, stream)

    def _load_credentials(self):
        with open(os.path.expanduser("~/.q/spotify_credentials"), 'r') as stream:
            return yaml.safe_load(stream)

    def currently_playing(self):
        return requests.request('GET', _BASE_URL + '/v1/me/player', headers={'Authorization': 'Bearer ' + self.token})

    def next(self):
        requests.post(_BASE_URL + '/v1/me/player/next', headers={'Authorization': 'Bearer ' + self.token})

    def prev(self):
        requests.post(_BASE_URL + '/v1/me/player/previous', headers={'Authorization': 'Bearer ' + self.token})

    def play(self):
        requests.put(_BASE_URL + '/v1/me/player/play', headers={'Authorization': 'Bearer ' + self.token})

    def pause(self):
        requests.put(_BASE_URL + '/v1/me/player/pause', headers={'Authorization': 'Bearer ' + self.token})
