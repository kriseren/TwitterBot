import tweepy
import spotipy 
import random
import utilities
from spotipy.oauth2 import SpotifyClientCredentials

#Definition of variables
tweet_content = ""
url = ""
playlists = ["https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=2664a7a33ed54dc8","https://open.spotify.com/playlist/37i9dQZF1DX2rVwh3lcWku?si=61d343c913594976","https://open.spotify.com/playlist/37i9dQZF1DWUNNEvaozpW5?si=d5423d82463f4f5e","https://open.spotify.com/playlist/37i9dQZEVXbNFJfN1Vw8d9?si=d0717c637e264f46","https://open.spotify.com/playlist/2DNLQuVm2SepjFP2ZLVksD?si=eb86d5340e234eea"]

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