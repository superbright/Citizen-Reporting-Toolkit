from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
import json
from StringIO import StringIO
from geopy.geocoders import GoogleV3
import tweepy
from tweepy import Cursor
import simplejson as json

# ENTER MONGO URI TO DUMP DATA INTO MONGODB
uri = "mongodb://mongouri"
client = MongoClient(uri)
db = client.app23187373
collection = db.journostwitter


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


if __name__ == '__main__':
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	user = '140journos'

	api = tweepy.API(auth)
	user = api.get_user(user)


	print "retreive " + user.screen_name + " timeline"

	secim_array =  api.user_timeline(id=user,include_rts=False,exclude_replies=True,count=1000)

	for status in reversed(secim_array):
	    # process status here
		post = { 'id_str': status.id_str, 'tweet': status.text, 'created_at': status.created_at }
		#mongo dump
		#post_id = collection.insert(post)

