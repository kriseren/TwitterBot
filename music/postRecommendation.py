# SCRIPT QUE GENERA Y PUBLICA UN TWEET COMO RECOMENDACIÓN MUSICAL DIARIA.
import tweepy

import Main
from auth import auth_utilities
from music import music_utilities


# Método principal del script.
def main(client: tweepy.Client):

    Main.print_title_message(f"MUSIC RECOMMENDATION SCRIPT INITIALISED AT {Main.get_time()}")

    # Inicia sesión en la API de Spotify.
    sp = auth_utilities.authenticate_to_spotify()

    # Escoge una canción para recomendar y extrae sus datos.
    song = music_utilities.chooseSong(sp)
    track_name = music_utilities.getTrackName()
    artist_name = music_utilities.getArtistName()
    url = music_utilities.getUrl()
    artist_genres = music_utilities.getArtistGenres()
    album = music_utilities.getAlbum()

    # Construye el tweet a publicar dependiendo del número de géneros que tenga la canción.
    if (len(artist_genres) > 1):
        tweet_content = url + "\n🎵CANCIÓN DEL DÍA🎵\n'" + track_name + "' de " + artist_name + ".\nIncluída en el álbum " + album + ".\nGéneros principales: " + \
                        artist_genres[0] + ", " + artist_genres[1] + ".\n#music #songoftheday"
    else:
        tweet_content = url + "\n🎵CANCIÓN DEL DÍA🎵\n'" + track_name + "' de " + artist_name + ".\nIncluída en el álbum " + album + ".\nGénero principal: " + \
                        artist_genres[0] + ".\n#music #songoftheday"

    # Upload the tweet
    Main.print_message("TWEET CONTENT",tweet_content)
    try:
        client.create_tweet(text=tweet_content)
        Main.print_message("MUSIC RECOMMENDATION STATUS","Music recommendation upload successful.","green")
    except Exception as ex:
        Main.print_message("MUSIC RECOMMENDATION STATUS","Music recommendation upload failed","red")
        Main.print_message("ERROR MESSAGE",str(ex),"red")
