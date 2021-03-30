from abc import ABC
from core.authenticate import get_spotify_username, user_authentication
from models.api_permission import APIPermission
from db.base_repository import set_user, set_username, reset_user


class AuthRepository(ABC):
    async def authenticate(self, client_key_header: str):
        await reset_user()
        permission = APIPermission(client_key_header)
        user = await set_user(permission.CLIENT_ID, permission.CLIENT_SECRET)
        scope = await user_authentication('playlist-read-private', user)
        permission['CLIENT_SCOPE'] = scope
        set_username(permission.CLIENT_ID, get_spotify_username())
        return permission