import utilities

# Definition of variables
tweet_content = ""
keywords = ""

# Authenticate into Twitter and Spotify
sp = utilities.authenticateToSpotify()
client = utilities.authenticateToTwitter()

# Get the mentions and print the last one.
mentions = client.get_users_mentions(id=utilities.twitter_id)
newMention = mentions.data[0]
print(f'New mention id: {newMention.id}')
print(f'New mention content: {newMention.text}')

# Read the last mention and compare it with the new mention
with open('lastMention.txt','r') as f:
    last_mention = f.readline()


with open('lastMention.txt','w') as f:
    print(f'Last mention content: {last_mention}')
    # Compare the mentions and if they are different, answer it
    if last_mention != newMention.text:
        print('There is a new mention.')
        # Like the tweet.
        client.like(newMention.id)
        # Generate one song
        utilities.chooseSong(sp)
        track_name = utilities.getTrackName()
        artist_name = utilities.getArtistName()
        url = utilities.getUrl()
        # Build the answer with one song.
        tweet_content = url + "\nWell well...\nLooks like if you were a song, you'd be " + track_name + ' by ' + artist_name + "."
        # Upload the reply to the last mention.
        try:
            #client.create_tweet(text=tweet_content,in_reply_to_tweet_id=newMention.id)
            print('Tweet upload successful.')
            print('\n' + tweet_content)
        except:
            print('The upload failed --> ' + tweet_content)
        # Write the new mention to the file
        f.write(newMention.text)
    else:
        print('There is no new mention.')
