from datetime import datetime
from core.config import SQLITE_URL
from models.models import LinkedLists, User
from tortoise.query_utils import Q
from tortoise.contrib.fastapi import register_tortoise

def init(app):
    register_tortoise(
        app,
        db_url=SQLITE_URL,
        modules={'models': ['models.models']},
        generate_schemas=True,
        add_exception_handlers=True,
    )

async def link_lists(sync_from, sync_to):    
    await LinkedLists.create(sync_from = sync_from, sync_to = sync_to)
    
async def unlink_list(sync_from = None, sync_to = None):
    if sync_from != None and sync_to != None:
        return await LinkedLists.filter(Q(sync_from = sync_from) & Q(sync_to = sync_to)).delete()
    elif sync_from != None and sync_to == None:
        return await LinkedLists.filter(sync_from = sync_from).delete()
    elif sync_from == None and sync_to != None:
        return await LinkedLists.filter(sync_to = sync_to).delete()
    else:
        return await LinkedLists.all().delete()

async def get_linked_lists():
    linked_list = await LinkedLists.all()
    return list(linked_list)

async def set_synced_date():
    await LinkedLists.all().update(last_synced=datetime.now())
    
async def set_user(client_id, client_secret):
    user = await User.create(client_id = client_id, client_secret = client_secret)
    return user

async def set_username(client_id, username):
    await User.filter(client_id = client_id).update(client_username = username)

async def get_user_credentials():
    await User.all()

async def reset_user():
    await User.all().delete()