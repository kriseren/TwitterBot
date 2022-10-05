#Imports
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#Spotify authentication
client_credentials_manager = SpotifyClientCredentials(client_id="25f4311410c64275b0b8ba828163ea2d", client_secret="f0971b2780b44419b59550177a8ef4f7")
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#Playlist extraction
playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=2664a7a33ed54dc8"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

#Tracks extraction
for track in sp.playlist_tracks(playlist_URI)["items"]:
    #URI
    track_uri = track["track"]["uri"]
    
    #Track name
    track_name = track["track"]["name"]
    
    #Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)
    
    #Name, popularity, genre
    artist_name = track["track"]["artists"][0]["name"]
    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]
    
    #Album
    album = track["track"]["album"]["name"]
    
    #Popularity of the track
    track_pop = track["track"]["popularity"]

    print(track_uri)
    print(track_name)
    print(artist_name)
    print(artist_genres)
    print(album)
    print()