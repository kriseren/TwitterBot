
import os.path
from random import randint
import utilities

#Definition of variables
tweet_content = ""
file = open("lastMention.txt","w")

#Authenticate into Twitter and Spotify
sp = utilities.authenticateToSpotify()
client = utilities.authenticateToTwitter()

#Generate one song
utilities.chooseSong(sp)
track_name = utilities.getTrackName()
artist_name = utilities.getArtistName()
url = utilities.getUrl()

#Get the mentions and print the last one.
mentions = client.get_users_mentions(id=utilities.twitter_id)
newMention = mentions.data[0]
print(newMention.id)
print("Tweet content: "+newMention.text)

#Check if the file containing the last mentioned tweet exists and read it
if(os.path.exists('lastMention.txt')):
    print("The file exists and it'll be read.")
    f = open("lastMention.txt")
    lastMentionID = f.readline()
    print(lastMentionID)
else:
    print("The file doesn't exist and it'll be created.")
    f = open("lastMention.txt","w")
    f.write(newMention.id)

print(os.path.exists("lastMention.txt"))

#Build the answer with one song.
tweet_content = url+"\nWell well...\nLooks like if you were a song, you'd be "+track_name+" by "+artist_name+"."

#Upload the reply to the last mention.
try:
     #client.create_tweet(text=tweet_content,in_reply_to_tweet_id=tweet.id)
    print("Tweet upload successful.")
    print("\n"+tweet_content)
except:
    print("The upload failed --> "+tweet_content)