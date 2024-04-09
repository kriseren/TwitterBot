from auth import auth_utilities as utilities, tokens as tkn
from utilities.Printer import print_message, print_title_message


def follow_back():
    """
    Función que sigue de vuelta a los seguidores en Twitter que no están siendo seguidos actualmente.
    """
    # Autenticación en Twitter y Spotify
    sp = utilities.authenticate_to_spotify()
    client = utilities.authenticate_to_twitter()
    twitter_id = tkn.twitter_id

    # Obtener mis seguidores y seguirlos de vuelta
    print_title_message("FOLLOW BACK SCRIPT")
    followers = client.get_users_followers(id=twitter_id)
    following = client.get_users_following(id=twitter_id)
    for user in followers.data:
        if user in following.data:
            print_message("INFO", f"Ya siguiendo a {user.username}")
        else:
            print_message("INFO", f"Comenzando a seguir a {user.username}")
            client.follow_user(user.id)


def main():
    """
    Función principal del script.
    """
    follow_back()


if __name__ == "__main__":
    main()
