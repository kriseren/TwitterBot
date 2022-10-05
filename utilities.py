from random import randint

import spotipy
import tweepy
from spotipy import SpotifyClientCredentials

#Attribute definition
spotify_id = "25f4311410c64275b0b8ba828163ea2d"
twitter_id = "1553856057885315073"
client_id = "SFplZXRkOGpOQUdYdFZXbjNiM0k6MTpjaQ"
playlists = ["https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=2664a7a33ed54dc8","https://open.spotify.com/playlist/37i9dQZF1DX2rVwh3lcWku?si=61d343c913594976","https://open.spotify.com/playlist/37i9dQZF1DWUNNEvaozpW5?si=d5423d82463f4f5e","https://open.spotify.com/playlist/37i9dQZEVXbNFJfN1Vw8d9?si=d0717c637e264f46","https://open.spotify.com/playlist/2DNLQuVm2SepjFP2ZLVksD?si=eb86d5340e234eea"]
url = ""
track_name = ""
artist_name = ""

def authenticateToSpotify():
    # Definition of Spotify tokens
    spotify_secret = "f0971b2780b44419b59550177a8ef4f7"
    # Authenticate to Spotify
    try:
        client_credentials_manager = SpotifyClientCredentials(client_id=spotify_id, client_secret=spotify_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        print("Spotify authentication successful.")
        return sp
    except:
        print("Spotify authentication failed.")

def authenticateToTwitter():
    # Definition of Twitter tokens
    client_secret = "TYgBZVhOonkL6WMpq8sX8dOpQPbeTWWK-asJCe1WpM04SNR12M"
    consumer_key = "Z8xMvxyLyWWqDHI3614M3bz1C"
    consumer_secret = "aVhlnV8wf8BtVFmAUWKqLKfoFMKvs0Jtt2vFiv3IJh3LMymmVG"
    access_token = "1553856057885315073-qrxZqS9CGUb74JfKPxiMCBkLhhUids"
    access_token_secret = "KgIF3EnSIZ2FJLh8WeumcVFJWUd1UBD3rbWL5nCww7P9O"
    bearer_token = "AAAAAAAAAAAAAAAAAAAAALLEfQEAAAAAKVOFRqOI2RRm%2BxnE0PAaSOnFJHI%3Dd6O8EUqeYsjVqyRiuumCRGLKXlB5zda5nglnQo0hfCE1eGEE8o"

    # Authenticate to Twitter
    try:
        client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret,
                               access_token=access_token, access_token_secret=access_token_secret)
        print("Twitter authentication successful.")
        return client
    except:
        print("Twitter authentication failed.")

def chooseSong(sp):
    # Extract all the tracks from the playlist
    global url, album, artist_genres, track_name, artist_name

    playlistNumber = randint(1, (
            len(playlists) - 1))  # Generate a random number to choose one playlist from the playlists list
    playlist_link = playlists[playlistNumber]  # Extract the chosen playlist link from the playlists list
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

    # Generate a random number within playlist length
    trackNumber = randint(0, 50)

    # Extract track information
    i = 0
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        i = i + 1
        if (i == trackNumber):
            track_uri = track["track"]["uri"]
            artist_uri = track["track"]["artists"][0]["uri"]
            artist_info = sp.artist(artist_uri)
            track_name = track["track"]["name"]
            artist_name = track["track"]["artists"][0]["name"]
            album = track["track"]["album"]["name"]
            artist_genres = artist_info["genres"]

    # Trim the URI so that we can build the URL
    track_uri_short = track_uri.split(":")
    url = "https://open.spotify.com/track/" + track_uri_short[2]

def getUrl():
    return url

def getArtistName():
    return artist_name

def getTrackName():
    return track_name

def getArtistGenres():
    return artist_genres

def getAlbum():
    return album