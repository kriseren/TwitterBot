import tweepy
import utilities

#Authenticate into Twitter and Spotify
sp = utilities.authenticateToSpotify()
client = utilities.authenticateToTwitter()
twitter_id = utilities.twitter_id

#Get my followers and follow them back
print("[FOLLOW BACK SCRIPT]")
followers = client.get_users_followers(id=twitter_id)
following = client.get_users_following(id=twitter_id)
for user in followers.data:
    if user in following.data:
        print("Already following "+user.username)
    else:
        print("Started following "+user.username)
        client.follow_user(user.id)