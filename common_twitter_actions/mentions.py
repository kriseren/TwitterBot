from datetime import datetime

import tweepy
import auth.tokens as tkn
from utilities.Printer import print_message,print_title_message
# Definición de variables globales.
global last_mention


def update_last_mention():
    """
    Actualiza el registro de la última mención en el archivo 'lastMention.txt'.
    """
    global last_mention
    with open('common_twitter_actions/lastMention.txt', 'w') as f:
        f.write(str(new_mention.id))


def check_new_mention(client):
    """
    Comprueba si ha habido una nueva mención en Twitter.

    Args:
        client (tweepy.Client): Cliente de Twitter para realizar la comprobación.

    Returns:
        bool: True si hay una nueva mención, False en caso contrario.
    """
    global new_mention
    global last_mention

    # Obtiene las menciones y muestra la nueva.
    mentions = client.get_users_mentions(id=tkn.twitter_id)
    new_mention = mentions.data[0]

    # Lee la última mención y la compara con la nueva.
    with open('common_twitter_actions/lastMention.txt', 'r') as f:
        last_mention = f.readline().strip()

    return last_mention != str(new_mention.id)


def main(main_client: tweepy.Client):
    """
    Función principal para gestionar las nuevas menciones en Twitter.

    Args:
        main_client (tweepy.Client): Cliente principal de Twitter.
    """
    client = main_client

    # Comprueba si ha habido alguna mención nueva.
    if check_new_mention(client):
        print_title_message(f"MENTION SCRIPT INITIALISED AT {datetime.now()}")

        # Da me gusta al tweet.
        client.like(new_mention.id)

        # Muestra el texto de la mención.
        print_message("NEW MENTION TEXT", new_mention.text)

        # Actualiza el registro de la última mención.
        update_last_mention()
