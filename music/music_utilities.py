import auth.tokens as tkn
from random import randint
import spotipy
import tweepy

# Definición de variables.
spotify_id = tkn.spotify_id
twitter_id = tkn.twitter_id
client_id = tkn.client_id
playlists = ["https://open.spotify.com/playlist/0UWhRhaDPBoAaX2RfqEt0J?si=7dfb670d9b4447f7",
             "https://open.spotify.com/playlist/7iGBwaCkY7cDlYtaUVoGy2?si=c0ea546a64ba4887",
             "https://open.spotify.com/playlist/7lA1UfHBhLwL01CyIpQCLB?si=a509d0ae7bc34380",
             "https://open.spotify.com/playlist/37i9dQZEVXbNFJfN1Vw8d9?si=be30f9db0d4b4580",
             "https://open.spotify.com/playlist/37i9dQZF1DWUNNEvaozpW5?si=8d53ae2744f94854"]


def answer_music_tweet(mentionText, sp):
    # Build the answer with one song.
    if randint(0, 2):  # To add human expressions, each time the bot uses one verb.
        verb = "fueses"
    else:
        verb = "fueras"

    # The keywords definition.
    keywords1 = ["canción soy", "canción sería"]
    keywords2 = ["recomiéndame", "recomiendas", "recomendación", "recomendar"]
    keywords3 = ["ropa", "ponerme", "pongo", "ponga"]

    # Depending on the mentionText contains keywords, the answer will be different.
    if keywords1[0] in mentionText.lower() or keywords1[1] in mentionText.lower():
        # Generate one song
        chooseSong(sp)
        track_name = getTrackName()
        artist_name = getArtistName()
        url = getUrl()

        # Define el contenido del tweet.
        tweet_content = url + "\nBueno bueno...\nParece que si " + verb + " una canción serías " + track_name + ' de ' + artist_name + "."

    elif keywords2[0] in mentionText.lower() or keywords2[1] in mentionText or keywords2[2] in mentionText or keywords2[
        3] in mentionText:
        # Generate one song
        chooseSong(sp)
        track_name = getTrackName()
        artist_name = getArtistName()
        url = getUrl()
        # Define el contenido del tweet.
        tweet_content = url + "\nDéjame que piense...\nVale, te recomiendo " + track_name + ' de ' + artist_name + "."
    else:
        tweet_content = "No te he entendido, consulta mi perfil para ver qué tipo de cosas puedo hacer 🙂"

    return tweet_content

# Método que escoge una canción de todas las playlists.
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
