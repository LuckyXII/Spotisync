from abc import ABC
from spotipy.exceptions import SpotifyException
from core.authenticate import get_spotify_user, user_authentication
from models.api_permission import APIPermission
from db.base_repository import set_user, set_username, get_user_credentials


class AuthRepository(ABC):
    async def authenticate(self, client_key_header: str):
        permission = APIPermission(client_key_header)

        scope = await user_authentication('playlist-read-private', permission.CLIENT_ID, permission.CLIENT_SECRET)
        if scope == None: 
            raise SpotifyException(http_status=401, msg='Client_key does not match, check values in spotify dashboard')

        user = await get_user_credentials(permission.CLIENT_ID, permission.CLIENT_SECRET)

        if user == None: 
            user = await set_user(permission.CLIENT_ID, permission.CLIENT_SECRET) 

        
        setattr(permission, 'CLIENT_SCOPE', scope)
        
        username = None
        if user.client_username == None:
            username = get_spotify_user(scope)['id']
            await set_username(permission.CLIENT_ID, username)

        setattr(
            permission, 
            'CLIENT_USERNAME',  
            username if user.client_username == None else user.client_username
        )
        return permission