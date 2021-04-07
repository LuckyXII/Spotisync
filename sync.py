import threading, time, logging, asyncio
from api.spoti import sync_linked_lists
from db.base_repository import get_all_users
from core.auth_repository import AuthRepository
from tortoise import Tortoise, run_async
from fastapi import HTTPException
from core.config import SQLITE_URL

async def init():
    await Tortoise.init(
        db_url=SQLITE_URL,
        modules={'models': ['models.models']},
    )

async def authenticate(client_key):
    permission = await AuthRepository().authenticate(client_key)
    if permission is None:
        raise HTTPException(status_code=401, detail='unathenticated: missing client_key')
    return permission

async def sync():
  users = await get_all_users()

  for user in users:
    permission = await authenticate(user.client_id+':'+user.client_secret)
    await sync_linked_lists(permission)

async def run_sync():
  await init()
  loop = asyncio.get_event_loop()
  try:
      loop.run_until_complete(await sync())
  finally:
      loop.close()
  
sync = run_async(run_sync())

  
