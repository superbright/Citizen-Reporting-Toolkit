from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
import json
from StringIO import StringIO
from geopy.geocoders import GoogleV3

# ENTER MONGO URI TO DUMP DATA INTO MONGODB
uri = "mongodb://URI"
client = MongoClient(uri)
db = client.app23187373
collection = db.logtest1


#instantiate google geocoder
geolocator = GoogleV3()

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key=""
consumer_secret=""

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token=""
access_token_secret=""

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """


    def on_data(self, data):
		io = StringIO(data)
		data = json.load(io);
		post = { 'id_str': data['id_str'], 'tweet': data['text'], 'created_at': data['created_at'], 'screen_name' : data["user"]["screen_name"] }
		
        #insert into mongo
        #post_id = collection.insert(post)
		#print post_id;
		return True
	

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    track_list = None
    stream = Stream(auth, l)
    stream.filter(track=['keyword'])

