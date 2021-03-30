from fastapi import FastAPI, HTTPException, Depends, Security
from models.api_permission import APIPermission
from fastapi.security.api_key import APIKeyHeader
from fastapi import FastAPI
from fastapi.security.api_key import APIKeyHeader
import uvicorn
from core.auth_repository import AuthRepository
from api.spoti import get_user_playlists, get_linked_playlists
from db.base_repository import init, link_lists,unlink_list,get_linked_lists


app = FastAPI()
client_key = APIKeyHeader(name='client_key')

@app.on_event("startup")
async def startup_event():
    init(app)
    global scope 

async def authenticate(
        client_key: str = Security(client_key)
    ): 
    permission = await AuthRepository().authenticate(client_key)
    if permission is None:
        raise HTTPException(status_code=401, detail='unathenticated: missing client_key')
    return permission


@app.get("/playlists")
async def my_playlists(permission: APIPermission = Depends(authenticate)):
    try:
        pl = get_user_playlists(permission.CLIENT_SCOPE)
    except Exception as e:
        raise HTTPException(status_code=500, detail= e)
    finally:
        if len(pl) == 0: 
            raise HTTPException(status_code=404, detail="no playlists found")
        return pl
        
@app.get("/linked-playlists")
async def linked_playlists(permission: APIPermission = Depends(authenticate)):
    try:
        ll = await get_linked_lists()
        pl = get_linked_playlists(permission.CLIENT_SCOPE, ll)
    except Exception as e:
        raise HTTPException(status_code=500, detail= e)
    finally:
        if len(pl) == 0: 
            raise HTTPException(status_code=404, detail="no playlists found")
        return pl

@app.post("/linked_playlists/{sync_from_id}/{sync_to_id}")
async def link_playlists(sync_from_id, sync_to_id):
    try:
        await link_lists(sync_from=sync_from_id, sync_to=sync_to_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail= e)
    finally: return 'Success!'


@app.delete("/linked_playlists/{sync_from_id}/{sync_to_id}")
async def unlink_playlists(sync_from_id, sync_to_id):
    try:
       delete_count = await unlink_list(sync_from=sync_from_id, sync_to=sync_to_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail= e)
    finally:
        if delete_count == 0: 
            raise HTTPException(
                status_code=404, 
                detail=f"playlists with id: {sync_from_id} not found for deletion"
            )
        return f'deleted {delete_count} items'


@app.delete("/linked_playlist/{sync_from_id}")
async def unlink_playlists(sync_from_id):
    try:
       delete_count = await unlink_list(sync_from=sync_from_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail= e)
    finally:
        if delete_count == 0: 
            raise HTTPException(
                status_code=404, 
                detail=f"playlists with id: {sync_from_id} not found for deletion"
            )
        return f'deleted {delete_count} items'
 
@app.delete("/linked_playlist/{sync_to_id}")
async def unlink_playlists(sync_to_id):
    try:
      delete_count = await unlink_list(sync_to=sync_to_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail= e)
    finally:
        if delete_count == 0: 
            raise HTTPException(
                status_code=404, 
                detail=f"playlists with id: {sync_to_id} not found for deletion"
            )
        return f'deleted {delete_count} items'


@app.delete("/linked_playlists")
async def unlink_playlists():
    try:
       delete_count = await unlink_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail= e)
    finally:
        if delete_count == 0: 
            raise HTTPException(
                status_code=404, 
                detail=f"no playlists found for deletion"
            )
        return f'deleted {delete_count} items'


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
