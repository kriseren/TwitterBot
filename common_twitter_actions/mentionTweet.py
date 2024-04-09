from auth import tokens as tkn
from auth import auth_utilities as utilities

# Autenticación en Spotify y Twitter.
sp = utilities.authenticateToSpotify()
client = utilities.authenticateToTwitter()

# Obtiene la última mención registrada.
with open('lastMention.txt', 'r') as f:
    last_mention = f.readline().strip()

# Obtiene las menciones y muestra la nueva.
mentions = client.get_users_mentions(id=utilities.twitter_id)
new_mention = mentions.data[0]
print(f'New mention id: {new_mention.id}')
print(f'New mention content: {new_mention.text}')

# Compara las menciones y si son diferentes responde.
if last_mention != new_mention.text:
    print('There is a new mention.')
    # Da me gusta al tweet.
    client.like(new_mention.id)
    # Llama al método answerMention en utilities para crear el contenido de la respuesta.
    tweet_content = utilities.answerTweet(new_mention.text, sp)
    # Publica la respuesta a la mención.
    try:
        # client.create_tweet(text=tweet_content, in_reply_to_tweet_id=new_mention.id)
        print('Tweet upload successful.')
        print('\n' + tweet_content)
        # Escribe la nueva mención en el fichero.
        with open('lastMention.txt', 'w') as f:
            f.write(new_mention.text)
    except Exception as ex:
        print('The upload failed --> ' + str(ex))
else:
    print('There is no new mention.')
    # Escribe la última mención de vuelta en el fichero.
    with open('lastMention.txt', 'w') as f:
        f.write(last_mention)
