import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from core.config import SPOTIPY_REDIRECT_URL
from db.base_repository import get_user_credentials

async def client_authentication():
  #user = await get_user_credentials()
  #auth_manager = SpotifyClientCredentials(user['client_id'], user['client_secret'])
  #return spotipy.Spotify(auth_manager=auth_manager)
  raise NotImplementedError

async def user_authentication(scope, client_id, client_secret):
  return spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id,
    client_secret,
    scope=scope,
    redirect_uri=SPOTIPY_REDIRECT_URL
  ))  

def get_spotify_user(scope):
  return scope.current_user()