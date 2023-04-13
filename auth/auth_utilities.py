# Tokens es un fichero que ha de contener los tokens definidos como Strings.
import spotipy
import tweepy
from spotipy import SpotifyClientCredentials

import Main
from auth import tokens as tkn


# Método que inicia sesión en la API de Spotify.
def authenticate_to_spotify():
    # Definición de tokens de Spotify.
    spotify_secret = tkn.spotify_secret
    spotify_id = tkn.spotify_id

    # Inicio de sesión.
    try:
        client_credentials_manager = SpotifyClientCredentials(client_id=spotify_id, client_secret=spotify_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        Main.print_message("SP AUTH STATUS","Spotify authentication successful","green")
        return sp
    except Exception as ex:
        Main.print_message("SP AUTH STATUS", "Spotify authentication failed", "red")
        Main.print_message("ERROR MESSAGE",str(ex),"red")

# Método que inicia sesión en la API de Twitter.
def authenticate_to_twitter():
    # Definición de tokens de Twitter.
    consumer_key = tkn.consumer_key
    consumer_secret = tkn.consumer_secret
    access_token = tkn.access_token
    access_token_secret = tkn.access_token_secret
    bearer_token = tkn.bearer_token

    # Inicio de sesión.
    try:
        client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret,
                               access_token=access_token, access_token_secret=access_token_secret)
        Main.print_message("TW AUTH STATUS","Twitter authentication successful","green")
        return client
    except Exception as ex:
        Main.print_message("TW AUTH STATUS","Twitter authentication failed","red")
        Main.print_message("ERROR MESSAGE",str(ex),"red")
