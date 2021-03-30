from db.base_repository import get_user_credentials

def get_user_playlists(scope):
    return list(map(
        lambda i : {"id": i['id'], "name": i['name']}, 
        scope.user_playlists(get_user_credentials()['name'])['items']
    ))
    

def get_linked_playlists(scope,linked_lists):
    new_playlists = []
    username = get_user_credentials()['name']
    for ll in linked_lists:
        from_list = scope.user_playlist(username, ll.sync_from)
        to_list = scope.user_playlist(username, ll.sync_to) 
        #to_list = to_list[0] #don't ask why

        new_playlists.append(
        {
            "sync_from": {"id":from_list['id'], "name":from_list['name']}, 
            "sync_to": {"id":to_list['id'], "name":to_list['name']}, 
            "last_sync": ll.last_synced
        }) 
    return new_playlists

    
def print_playlists(playlists):
  for playlist in playlists['items']:
      print(f'ID: {playlist["id"]} | Name: {playlist["name"]} | By: {playlist["owner"]["id"]}')
  
def add_tracks_to_playlist(scope,playlist,tracks):
    scope.playlist_add_items(playlist,tracks['items'])

            
def get_newest_track(scope,playlist,last_sync):
    new_tracks = []
    while playlist:
        for track in playlist['items']:
            if(last_sync < track['added_at']):
                print(f'Added: {track["added_at"]} | Name: {track["track"]["name"]} | Album: {track["track"]["album"]["name"]}')
                new_tracks.add(track)
        if playlist['next']:
            playlist = scope.next(playlist)
        else:
            playlist = None
    return new_tracks
