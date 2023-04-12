import tweepy
from auth import auth_utilities


# Método que comprueba si ha habido una nueva mención.
def check_new_mention(api, last_mention_id):

    #
    client = utilities.authenticateToTwitter()

    # Obtiene las menciones y muestra la nueva.
    mentions = client.get_users_mentions(id=utilities.twitter_id)
    newMention = mentions.data[0]

    # Lee la última mención y la compara con la nueva.
    with open('lastMention.txt', 'r') as f:
        last_mention = f.readline()

    if last_mention != newMention.text:
        return True
    else:
        return False
