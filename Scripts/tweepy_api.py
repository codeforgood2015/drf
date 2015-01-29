# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 16:58:19 2015

@author: LLP-admin
"""

import tweepy, json
from tweepy import StreamListener, Stream

consumer_key = 'sASEh024SKmPvq1KiikEYcsLr'
consumer_secret = '3oxUYDpxtSctph7pg2WBlpkHHeREBJvfpuYCs57MZBJwNraddD'
access_token = '2233842882-GyJ91dFwZAYud8U3GwLJkawS2tEb6uProNT8xpX'
access_token_secret = 'UCL2qOJ1KKQEPKDLeCLCi9999SYDiIzuabKl2f3JkbDuW'


#Ceration of the actual interface, using authentication
#api = tweepy.API(auth)

#api.update_status('Hello Tweepy API: this is test 2!')

#user = api.me()

class StdOutListener(StreamListener):
    """handles data received from the stream."""
    def __init__(self, fname,  api=None):
        self.nthLoop = 0
        self.api = api
        self.count = 0
        self.max_count = 10
        self.filename = 'stream_'+ fname + str(self.nthLoop)
        
    def saveTweet(self, tweet):
        with open(self.filename+'.txt', 'a') as f:
            f.write(tweet)
            
    def update(self):
        self.count = 0
        self.nthLoop += 1
        self.filename = self.filename[:-1] + str(self.nthLoop)
        
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print 'loop: ', self.nthLoop
        print 'count: ', self.count
        print '%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        tweet = decoded['text'].encode('ascii', 'ignore')
        
        
        if self.count < self.max_count:
            print '\ncount: ', self.count
#            print 'Tweet text: ', repr(status.text)
#            print 'Author: ', status.user.screen_name
#            for hashtag in status.entities['hashtags']:
#                print 'hashtag: ',hashtag['text']
        else:
            print 'max number of printing reached. New file open and start saving.'
            self.update()
            
        self.saveTweet(tweet)
        self.count += 1
        return True

#    def on_status(self,status):
#        if self.count < self.max_count:
#            print '\ncount: ', self.count
##            print 'Tweet text: ', repr(status.text)
##            print 'Author: ', status.user.screen_name
##            for hashtag in status.entities['hashtags']:
##                print 'hashtag: ',hashtag['text']
#        else:
#            print 'max number of printing reached. New file open and start saving.'
#            self.update()
#            
#        tweet = status.text.lower()
#        self.saveTweet(tweet)
#        self.count += 1
#        return True
        
    def on_error(self, status_code):
        print 'Got an error with error code', status_code
        return True #To continue listening
        
    def on_timeout(self):
        print 'Timeout ...'
        return True #To continue listening
        
if __name__ == '__main__':    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    follow_list = []
    track_list = ['chicago']
    listener = StdOutListener(fname = track_list[0] )
    stream = Stream(auth, listener)
    stream.filter(follow=follow_list, track=track_list)

        
        