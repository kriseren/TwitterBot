from datetime import datetime

import tweepy

from auth import auth_utilities
from music import music_utilities
from utilities.Printer import print_message, print_title_message


# Método principal del script.
def main(client: tweepy.Client):
    """
    Genera y publica un tweet diario como recomendación musical.

    Args:
        client (tweepy.Client): Cliente de Twitter autenticado.
    """
    # Imprime un mensaje indicando que se ha inicializado el script.
    print_title_message(f"MUSIC RECOMMENDATION SCRIPT INITIALISED AT {datetime.now()}")

    # Autentica al cliente de Spotify.
    sp = auth_utilities.authenticate_to_spotify()

    # Escoge una canción para recomendar y extrae sus datos.
    song = music_utilities.choose_song(sp)
    track_name = music_utilities.get_track_name()
    artist_name = music_utilities.get_artist_name()
    url = music_utilities.get_url()
    artist_genres = music_utilities.get_artist_name()
    album = music_utilities.get_album()

    # Construye el contenido del tweet a publicar dependiendo del número de géneros que tenga la canción.
    if len(artist_genres) > 1:
        tweet_content = (
                url +
                "\n🎵 CANCIÓN DEL DÍA 🎵\n'" + track_name + "' de " + artist_name +
                ".\nIncluida en el álbum " + album +
                ".\nGéneros principales: " + artist_genres[0] + ", " + artist_genres[1] +
                ".\n#music #songoftheday"
        )
    else:
        tweet_content = (
                url +
                "\n🎵 CANCIÓN DEL DÍA 🎵\n'" + track_name + "' de " + artist_name +
                ".\nIncluida en el álbum " + album +
                ".\nGénero principal: " + artist_genres[0] +
                ".\n#music #songoftheday"
        )

    # Publica el tweet.
    print_message("TWEET CONTENT", tweet_content)
    try:
        client.create_tweet(text=tweet_content)
        print_message("MUSIC RECOMMENDATION STATUS", "Music recommendation upload successful.", "green")
    except Exception as ex:
        print_message("MUSIC RECOMMENDATION STATUS", "Music recommendation upload failed", "red")
        print_message("ERROR MESSAGE", str(ex), "red")


if __name__ == "__main__":
    # Autentica al cliente de Twitter.
    client = auth_utilities.authenticate_to_twitter()

    # Llama al método principal con el cliente autenticado.
    main(client)
