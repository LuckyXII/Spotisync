import spotipy
from starlette.config import environ
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from core.config import SPOTIPY_REDIRECT_URL
from db.base_repository import get_user_credentials

async def client_authentication():
  user = await get_user_credentials()
  auth_manager = SpotifyClientCredentials(user['client_id'], user['client_secret'])
  return spotipy.Spotify(auth_manager=auth_manager)

async def user_authentication(scope, user):
  user = await get_user_credentials()
  return spotipy.Spotify(auth_manager=SpotifyOAuth(
    user['client_id'],
    user['client_secret'],
    scope=scope,
    redirect_uri=SPOTIPY_REDIRECT_URL
  ))  

def get_spotify_username():
  return spotipy.current_user()['name']