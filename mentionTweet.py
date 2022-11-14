import tokens as tkn
import utilities

# Autenticación en Spotify y Twitter.
sp = utilities.authenticateToSpotify()
client = utilities.authenticateToTwitter()

# Obtiene las menciones y muestra la nueva.
mentions = client.get_users_mentions(id=utilities.twitter_id)
newMention = mentions.data[0]
print(f'New mention id: {newMention.id}')
print(f'New mention content: {newMention.text}')

# Lee la última mención y la compara con la nueva.
with open(tkn.installation_directory + 'lastMention.txt', 'r') as f:
    last_mention = f.readline()

with open(tkn.installation_directory + 'lastMention.txt', 'w') as f:
    print(f'Last mention content: {last_mention}')
    # Compara las menciones y si son diferentes la responde.
    if last_mention != newMention.text:
        print('There is a new mention.')
        # Da me gusta al tweet.
        client.like(newMention.id)
        #Llama al método answerMention en utilities para crear el contenido de la respuesta.
        tweet_content=utilities.answerTweet(newMention.text,sp)
        # Publica la respuesta a la mención.
        try:
            #client.create_tweet(text=tweet_content,in_reply_to_tweet_id=newMention.id)
            print('Tweet upload successful.')
            print('\n' + tweet_content)
            # Escribe la nueva mención en el fichero.
            f.write(newMention.text)
        except:
            print('The upload failed --> ' + tweet_content)
    else:
        print('There is no new mention.')
        # Escribe la última mención de vuelta en el fichero.
        f.write(last_mention)