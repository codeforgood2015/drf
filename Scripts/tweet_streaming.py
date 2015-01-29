# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 13:33:53 2015
Twitter Streaming
@author: Hayley Song
"""
import tweepy
from tweepy import StreamListener
import json, time, sys

# Authentication details. To  obtain these visit dev.twitter.com
consumer_key = 'sASEh024SKmPvq1KiikEYcsLr'
consumer_secret = '3oxUYDpxtSctph7pg2WBlpkHHeREBJvfpuYCs57MZBJwNraddD'
access_token = '2233842882-GyJ91dFwZAYud8U3GwLJkawS2tEb6uProNT8xpX'
access_token_secret = 'UCL2qOJ1KKQEPKDLeCLCi9999SYDiIzuabKl2f3JkbDuW'

# This is the listener, resposible for receiving data
class SListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        return True

    def on_error(self, status):
        print 'error: ', status
        return True
        

if __name__ == '__main__':
    l = SListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print "Showing all new tweets for #programming:"

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['boston'])