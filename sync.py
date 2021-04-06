import threading
from api.spoti import sync_linked_lists
from db.base_repository import get_all_users
from core.auth_repository import AuthRepository
from fastapi import HTTPException


async def authenticate(client_key):
    permission = await AuthRepository().authenticate(client_key)
    if permission is None:
        raise HTTPException(status_code=401, detail='unathenticated: missing client_key')
    return permission

async def sync():
  users = get_all_users()

  for user in users:
    permission = await authenticate(user.client_id+':'+user.client_secret)
    await sync_linked_lists(permission)
