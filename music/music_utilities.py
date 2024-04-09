import auth.tokens as tkn
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import randint

# Definición de variables.
spotify_id = tkn.spotify_id
twitter_id = tkn.twitter_id
client_id = tkn.client_id
playlists = [
    "https://open.spotify.com/playlist/0UWhRhaDPBoAaX2RfqEt0J?si=7dfb670d9b4447f7",
    "https://open.spotify.com/playlist/7iGBwaCkY7cDlYtaUVoGy2?si=c0ea546a64ba4887",
    "https://open.spotify.com/playlist/7lA1UfHBhLwL01CyIpQCLB?si=a509d0ae7bc34380",
    "https://open.spotify.com/playlist/37i9dQZEVXbNFJfN1Vw8d9?si=be30f9db0d4b4580",
    "https://open.spotify.com/playlist/37i9dQZF1DWUNNEvaozpW5?si=8d53ae2744f94854"
]

# Autenticación de Spotify
auth_manager = SpotifyClientCredentials(client_id=spotify_id, client_secret=tkn.spotify_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


def answer_music_tweet(mentionText):
    """
    Genera una respuesta para un tweet relacionado con música basado en el texto mencionado.
    Args:
        mentionText (str): Texto mencionado en el tweet.

    Returns:
        str: Contenido del tweet de respuesta.
    """
    # Construye la respuesta con una canción.
    if randint(0, 2):  # Para agregar expresiones humanas, cada vez que el bot usa un verbo.
        verb = "fueses"
    else:
        verb = "fueras"

    # Definición de palabras clave.
    keywords1 = ["canción soy", "canción sería"]
    keywords2 = ["recomiéndame", "recomiendas", "recomendación", "recomendar"]

    # Dependiendo de si mentionText contiene palabras clave, la respuesta será diferente.
    if any(keyword.lower() in mentionText.lower() for keyword in keywords1):
        choose_song()
        tweet_content = f"{get_url()}\nBueno bueno...\nParece que si {verb} una canción serías {get_track_name()} de {get_artist_name()}."

    elif any(keyword.lower() in mentionText.lower() for keyword in keywords2):
        choose_song()
        tweet_content = f"{get_url()}\nDéjame que piense...\nVale, te recomiendo {get_track_name()} de {get_artist_name()}."

    else:
        tweet_content = "No te he entendido, consulta mi perfil para ver qué tipo de cosas puedo hacer 🙂"

    return tweet_content


def choose_song():
    """
    Elige una canción aleatoria de las playlists disponibles.
    """
    playlist_link = playlists[randint(0, len(playlists) - 1)]  # Elegir una playlist aleatoria
    playlist_uri = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_uri)["items"]]
    track_uri = track_uris[randint(0, len(track_uris) - 1)]

    track_info = sp.track(track_uri)
    artist_info = sp.artist(track_info["artists"][0]["uri"])

    global url, track_name, artist_name, album, artist_genres
    url = track_info["external_urls"]["spotify"]
    track_name = track_info["name"]
    artist_name = track_info["artists"][0]["name"]
    album = track_info["album"]["name"]
    artist_genres = artist_info["genres"]


# Métodos para obtener información de la canción elegida
def get_url():
    """
    Obtiene la URL de la canción.
    """
    return url


def get_track_name():
    """
    Obtiene el nombre de la canción.
    """
    return track_name


def get_artist_name():
    """
    Obtiene el nombre del artista de la canción.
    """
    return artist_name


def get_album():
    """
    Obtiene el nombre del álbum de la canción.
    """
    return album


def main():
    # Ejemplo de cómo usar la función answer_music_tweet
    mention_text = "Hola, ¿cuál sería la canción perfecta para mí?"
    response_tweet = answer_music_tweet(mention_text)
    print(response_tweet)


if __name__ == "__main__":
    main()
