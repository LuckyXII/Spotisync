
from db.base_repository import get_linked_lists, set_synced_date
from datetime import datetime

async def get_user_playlists(permission):
    return list(map(
        lambda i : {"id": i['id'], "name": i['name']}, 
        permission.CLIENT_SCOPE.user_playlists(permission.CLIENT_USERNAME)['items']
    ))

async def get_linked_playlists(permission):
    linked_lists = await get_linked_lists()
    new_playlists = []
    scope = permission.CLIENT_SCOPE
    username = permission.CLIENT_USERNAME
    for ll in linked_lists:
        from_list = scope.user_playlist(username, ll.sync_from)
        to_list = scope.user_playlist(username, ll.sync_to)

        new_playlists.append(
        {
            "sync_from": {"id":from_list['id'], "name":from_list['name']}, 
            "sync_to": {"id":to_list['id'], "name":to_list['name']}, 
            "last_sync": ll.last_synced
        }) 
    return new_playlists

async def get_linked_spotipy_playlists(permission):
    linked_lists = await get_linked_lists()
    new_playlists = []
    scope = permission.CLIENT_SCOPE
    username = permission.CLIENT_USERNAME
    for ll in linked_lists:
        from_list = scope.user_playlist(username, ll.sync_from)
        to_list = scope.user_playlist(username, ll.sync_to)

        new_playlists.append(
        {
            'sync_from_playlist': from_list, 
            'sync_to_playlist': to_list, 
            'last_sync': ll.last_synced
        }) 
    return new_playlists

    
def print_playlists(playlists):
  for playlist in playlists['items']:
      print(f'ID: {playlist["id"]} | Name: {playlist["name"]} | By: {playlist["owner"]["id"]}')
  
def add_tracks_to_playlist(permission,playlist,tracks):
    scope = permission.CLIENT_SCOPE
    scope.playlist_add_items(playlist['id'],tracks)

            
def get_newest_track(permission,playlist,last_sync):
    new_tracks = []       
    for track in playlist['tracks']['items']:
        added_at = datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ').date()
        if(last_sync < added_at):
            print(f'Added: {track["added_at"]} | Name: {track["track"]["name"]} | Album: {track["track"]["album"]["name"]}')
            new_tracks.append(track['track']['id'])
    return new_tracks



async def sync_list(permission ,from_playlist, to_playlist, last_sync):
    new_tracks = get_newest_track(permission, from_playlist,last_sync)
    add_tracks_to_playlist(permission, to_playlist, new_tracks)
    await set_synced_date(from_playlist['id'])


async def sync_linked_lists(permission):
    linked_lists = await get_linked_spotipy_playlists(permission)
    for ll in linked_lists:
        #print(f'{ll['sync_from_playlist']}, {ll['sync_to_playlist']}, {ll['last_sync']}')
        await sync_list(permission, ll['sync_from_playlist'], ll['sync_to_playlist'], ll['last_sync'])
    
    
