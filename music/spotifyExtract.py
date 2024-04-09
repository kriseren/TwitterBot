import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Autenticación de Spotify
client_credentials_manager = SpotifyClientCredentials(client_id="25f4311410c64275b0b8ba828163ea2d",
                                                      client_secret="f0971b2780b44419b59550177a8ef4f7")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def extract_tracks(playlist_uri):
    """
    Extrae información sobre cada pista de una lista de reproducción de Spotify.

    Args:
        playlist_uri (str): URI de la lista de reproducción de Spotify.
    """
    # Extrae las pistas de la lista de reproducción
    tracks = sp.playlist_tracks(playlist_uri)["items"]

    # Procesa cada pista
    for track in tracks:
        # URI de la pista
        track_uri = track["track"]["uri"]

        # Nombre de la pista
        track_name = track["track"]["name"]

        # Artista principal
        artist = track["track"]["artists"][0]
        artist_name = artist["name"]
        artist_uri = artist["uri"]

        # Información adicional del artista
        artist_info = sp.artist(artist_uri)
        artist_popularity = artist_info["popularity"]
        artist_genres = artist_info["genres"]

        # Álbum
        album_name = track["track"]["album"]["name"]

        # Popularidad de la pista
        track_popularity = track["track"]["popularity"]

        # Imprime la información de la pista
        print("Track URI:", track_uri)
        print("Track Name:", track_name)
        print("Artist Name:", artist_name)
        print("Artist Genres:", artist_genres)
        print("Album Name:", album_name)
        print("Track Popularity:", track_popularity)
        print()


def main():
    """
    Función principal del script.
    """
    # Enlace de la lista de reproducción
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=2664a7a33ed54dc8"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    # Ejecuta la función para extraer y mostrar la información de las pistas
    extract_tracks(playlist_URI)


if __name__ == "__main__":
    main()
