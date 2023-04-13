import tweepy
import auth.tokens as tkn
import Main

# Definición de variables.
global last_mention

# Método que actualiza el registro de última mención.
def update_last_mention():
    global last_mention
    with open('common_actions/lastMention.txt', 'w') as f:
        f.write(str(new_mention.id))

# Método que comprueba si ha habido una nueva mención.
def check_new_mention(client):
    global new_mention
    global last_mention

    # Obtiene las menciones y muestra la nueva.
    mentions = client.get_users_mentions(id=tkn.twitter_id)
    new_mention = mentions.data[0]

    # Lee la última mención y la compara con la nueva.
    with open('common_actions/lastMention.txt', 'r') as f:
        last_mention = f.readline().strip()

    if last_mention != str(new_mention.id):
        return True
    else:
        return False


# Método principal del script.
def main(main_client: tweepy.Client):

    client = main_client
    # Comprueba si ha habido alguna mención nueva.
    if check_new_mention(client):
        Main.print_title_message(f"MENTION SCRIPT INITIALISED AT {Main.get_time()}")
        # Da me gusta al tweet.
        client.like(new_mention.id)
        # Comprueba el texto de la mención.
        Main.print_message("NEW MENTION TEXT",new_mention.text)
        # Escribe la nueva mención en el fichero de lastMention.txt para actualizar el registro.
        update_last_mention()


