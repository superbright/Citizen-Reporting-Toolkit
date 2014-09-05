
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
    #def on_event(self, status):
 	#	print status.text

    def on_data(self, data):
		io = StringIO(data)
		#post_id = collection.insert(json.load(io))
		#print json.load(io)
		data = json.load(io);
		

    # if this key is in the data, it meants its a retweet
		if "retweeted_status" in data:
			print "retweet"
			return True
		

    # scanning for tweets from asingle user here.	
		if data["user"]["screen_name"] == "140journos":
		  
		 	georesult = geolocator.geocode(data['text'])
			if georesult is None:
				print "non geocode result"
				lat = 0
				lng = 0
				address = addr
			else:
				address, (lat, lng) = georesult
			
	    #dump into mongodb
			#post = { 'id_str': data['id_str'], 'tweet': data['text'], 'created_at': data['created_at'], 'coords' : {'lat':lat,'lon':lng },"addr":address }
			#post_id = collection.insert(post)
			#print post_id;
			return True
		else:
			print "other user than what you are looking for"
			return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    list_users = ['140journos'];
    track_list = None
    stream = Stream(auth, l)
    #follow user ids, if you want to follow keyword use track=['keyworkd1','keyword2']
    stream.filter(follow=['456177793','2327222113'])

