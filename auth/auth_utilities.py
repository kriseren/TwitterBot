import spotipy
import tweepy
from spotipy import SpotifyClientCredentials

from auth import tokens as tkn
from utilities import Printer


def authenticate_to_spotify():
    """
    Inicia sesión en la API de Spotify utilizando los tokens definidos en el fichero tokens.

    Returns:
        Spotify: Objeto de autenticación de Spotify.
    """
    # Obtener tokens de Spotify
    spotify_secret = tkn.spotify_secret
    spotify_id = tkn.spotify_id

    try:
        # Iniciar sesión en Spotify
        client_credentials_manager = SpotifyClientCredentials(client_id=spotify_id, client_secret=spotify_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        Printer.print_message("SP AUTH STATUS", "Autenticación de Spotify exitosa", "green")
        return sp
    except Exception as ex:
        Printer.print_message("SP AUTH STATUS", "Autenticación de Spotify fallida", "red")
        Printer.print_message("ERROR MESSAGE", str(ex), "red")

def authenticate_to_twitter():
    """
    Inicia sesión en la API de Twitter utilizando los tokens definidos en el fichero tokens.

    Returns:
        tweepy.Client: Objeto de autenticación de Twitter.
    """
    # Obtener tokens de Twitter
    consumer_key = tkn.consumer_key
    consumer_secret = tkn.consumer_secret
    access_token = tkn.access_token
    access_token_secret = tkn.access_token_secret
    bearer_token = tkn.bearer_token

    try:
        # Iniciar sesión en Twitter
        client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret,
                               access_token=access_token, access_token_secret=access_token_secret)
        Printer.print_message("TW AUTH STATUS", "Autenticación de Twitter exitosa", "green")
        return client
    except Exception as ex:
        Printer.print_message("TW AUTH STATUS", "Autenticación de Twitter fallida", "red")
        Printer.print_message("ERROR MESSAGE", str(ex), "red")
