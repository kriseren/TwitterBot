from random import randint
import tokens as tkn
import spotipy
import tweepy
from spotipy import SpotifyClientCredentials

# Attribute definition
spotify_id = tkn.spotify_id
twitter_id = tkn.twitter_id
client_id = tkn.client_id
playlists = ["https://open.spotify.com/playlist/0UWhRhaDPBoAaX2RfqEt0J?si=7dfb670d9b4447f7",
             "https://open.spotify.com/playlist/7iGBwaCkY7cDlYtaUVoGy2?si=c0ea546a64ba4887",
             "https://open.spotify.com/playlist/7lA1UfHBhLwL01CyIpQCLB?si=a509d0ae7bc34380",
             "https://open.spotify.com/playlist/37i9dQZEVXbNFJfN1Vw8d9?si=be30f9db0d4b4580",
             "https://open.spotify.com/playlist/37i9dQZF1DWUNNEvaozpW5?si=8d53ae2744f94854"]
url = ""
track_name = ""
artist_name = ""


def authenticateToSpotify():
    # Definition of Spotify tokens
    spotify_secret = tkn.spotify_secret
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
    client_secret = tkn.client_secret
    consumer_key = tkn.consumer_key
    consumer_secret = tkn.consumer_secret
    access_token = tkn.access_token
    access_token_secret = tkn.access_token_secret
    bearer_token = tkn.bearer_token
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
    global url, album, artist_genres, track_name, artist_name, track_uri

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
