import tokens as tkn
import utilities

# Authenticate into Twitter and Spotify
sp = utilities.authenticateToSpotify()
client = utilities.authenticateToTwitter()

# Get the mentions and print the last one.
mentions = client.get_users_mentions(id=utilities.twitter_id)
newMention = mentions.data[0]
print(f'New mention id: {newMention.id}')
print(f'New mention content: {newMention.text}')

# Read the last mention and compare it with the new mention
with open(tkn.installation_directory + 'lastMention.txt', 'r') as f:
    last_mention = f.readline()

with open(tkn.installation_directory + 'lastMention.txt', 'w') as f:
    print(f'Last mention content: {last_mention}')
    # Compare the mentions and if they are different, answer it
    if last_mention != newMention.text:
        print('There is a new mention.')
        # Like the tweet.
        client.like(newMention.id)
        #Call the answerMention method in utilities to create the reply content.
        tweet_content=utilities.answerTweet(newMention.text,sp)
        # Upload the reply to the last mention.
        try:
            client.create_tweet(text=tweet_content,in_reply_to_tweet_id=newMention.id)
            print('Tweet upload successful.')
            print('\n' + tweet_content)
            # Write the new mention to the file.
            f.write(newMention.text)
        except:
            print('The upload failed --> ' + tweet_content)
    else:
        print('There is no new mention.')
        f.write(last_mention) # Write the last mention back to the file.