# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 15:52:44 2015
My First twitter API exploration.
@author: Hayley Song
"""
import tweepy 

#Login credentials to use tweepy; these are my credentials, but you probably need your own.
access_token = "220205585-QcUd5fxZNqn3NKuhjVhlUAyyQCFOc3NqUsU2IDtm"
access_token_secret = "T4GTzbMDztGyxtkXL3YKpcm5e1YOjWUsGQOLS9t0FpkLX"
consumer_key = "vPQJv4XS3ExYXS7PNN7fYN1EK"
consumer_secret = "26b1ab1JAuCQ30qg6id5dtrZeQCJOmrf4mkut1GLtVyyMe2LE3"


#This is the logging in part
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api=tweepy.API(auth)
    
def getStatuses(username, includeRetweets = False):
    """Returns a list of the user's statuses"""
    statuses = []
    for status in tweepy.Cursor(api.user_timeline, screen_name = username).items():
        statuses.append(status)
    return statuses

#statuses = getStatuses('TheArcUS')

#def isRetweet(status):
#    """Returns True if the status is a retweet, else False.
#    Recall: a retweet starts with @
#    """
#    try:
#        s0.retweeted_status

def countRetweets(username):
    """Returns how many times the user's tweets have been retweeted.
    """
    statuses = getStatuses(username)
    nameLength = len(username)
    c = 0
    for status in statuses:
        if len(status.text) < 4 + nameLength:
            continue
        
        if status.text[:4] == 'RT @' and status.text[4: 4+nameLength] == username:
            c += 1
    print c
    return c 
countRetweets('TheArcUS')