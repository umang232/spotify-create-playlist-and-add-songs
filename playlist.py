import requests
import json
from secrets import spotify_token, id
import urllib


def create_playlist(name, description):
    """Create A New Playlist"""
    request_body = json.dumps({
        "name": name,
        "description": description,
        "public": False
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(id)
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
    response_json = response.json()
    print(response_json)
    print(response_json['id'])
    return response_json['id']


def search_song(artist, track):
    query = urllib.parse.quote(f'{artist} {track}')
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }
    )
    response_json = response.json()
    print(response_json)
    results = response_json['tracks']['items']
    print(results[0])
    if results:
        # let's assume the first track in the list is the song we want
        return results[0]['id']
    else:
        raise Exception(f"No song found for {artist} = {track}")


def add_song_to_spotify(playlist_id, song_id):
    url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
    req_body = json.dumps(
        {
            "uris": [f"spotify:track:{song_id}"
                     ]
        }
    )
    response = requests.post(
        url,
        req_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }
    )
    print(response.json())

    return response.ok


if __name__ == '__main__':
    name = input("Enter the name of the playlist : ")
    description = input("Enter the description of the playlist : ")
    playlist = create_playlist(name, description)
    while True:
        artist = input("Enter artist name : ")
        track = input("Enter the track name : ")
        song = search_song(artist, track)
        add_song_to_spotify(playlist, song)
        opt = input("Enter 'y' to add more songs : ")
        if opt == 'y':
            continue
        else:
            break
    print("Thanks!!!")
