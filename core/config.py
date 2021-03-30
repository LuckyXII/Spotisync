from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "Spotisync"
VERSION = "1.0.0"

SECRET_KEY = config("SECRET_KEY", cast=Secret, default="llamaduck")

SPOTIPY_REDIRECT_URL = config('SPOTIPY_REDIRECT_URL', cast=str, default='http://localhost:8080')

#SPOTIPY_CLIENT_ID =   config('SPOTIPY_CLIENT_ID', cast=str, default=None)
#SPOTIPY_CLIENT_SECRET = config('SPOTIPY_CLIENT_SECRET' ,cast=str, default=None)
#SPOTIPY_CLIENT_USERNAME = config('SPOTIPY_CLIENT_USERNAME' ,cast=str, default=None)

SQLITE_DB_FILE = config('SQLITE_DB_FILE' ,cast=str, default=f'./db/db.sqlite3')
SQLITE_URL = config(
  'SQLITE_URL',
  cast=str,
  default=f'sqlite://{SQLITE_DB_FILE}'
)  
