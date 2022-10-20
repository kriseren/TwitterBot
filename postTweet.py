import tweepy
import spotipy 
import random
import utilities
from spotipy.oauth2 import SpotifyClientCredentials

#Definition of variables
tweet_content = ""
url = ""
playlists = utilities.playlists

#Authenticate into Twitter and Spotify
sp = utilities.authenticateToSpotify()
client = utilities.authenticateToTwitter()

#Generate one song
utilities.chooseSong(sp)
track_name = utilities.getTrackName()
artist_name = utilities.getArtistName()
url = utilities.getUrl()
artist_genres = utilities.getArtistGenres()
album = utilities.getAlbum()

#Build the tweet content depending on the number of genres
if(len(artist_genres)>1):
    tweet_content = url+"\n🎵SONG OF THE DAY🎵\n"+track_name+" from "+artist_name+".\nIncluded in the album "+album+".\nMain genres: "+artist_genres[0]+", "+artist_genres[1]+".\n#music #songoftheday"
else:
    tweet_content = url+"\n🎵SONG OF THE DAY🎵\n"+track_name+" from "+artist_name+".\nIncluded in the album "+album+".\nMain genre: "+artist_genres[0]+".\n#music #songoftheday"

#Upload the tweet
print("[TWEET STATUS]")
try:
    client.create_tweet(text=tweet_content)
    print("Tweet upload successful.")
    print("\n"+tweet_content)
except:
    print("The upload failed --> "+tweet_content)