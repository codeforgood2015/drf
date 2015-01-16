# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 15:52:44 2015
My First twitter API exploration.
@author: Hayley Song
"""
import tweepy 
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter, defaultdict
from pandas import DataFrame, Series

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


def isRetweet(status):
    """Returns True if a status is either the user's retweet 
    or someone else's retweet (of the user's tweet).
    Note: the latter kind of a retweet is a better indicator of the user's 
    tweet's popularity. 
    """
    if re.match('RT @', status.text) != None:
        return True
    return False
    
    
#def countMyRetweets(screen_name, statuses):
#    """Returns how many times (purely) my tweets are retweeted.
#    """ 
#    #First exclude tweets retweeted by me (thus, not my own tweet)
#    c = 0
#    for status in statuses:
#        try: 
#            rs = status.retweeted_status
#            continue
#        except ()
#        if status.author.screen_name == screen_name and status.retweet_count > 0:
#            c += status.retweet_count
#    return c 
#        
def countRetweets(screen_name, statuses):
    """Returns how many times the user's tweets on his/her timeline have been 
    retweeted.
    """
#    statuses = getStatuses(username)
    nameLength = len(screen_name)
    c = 0
    for status in statuses:
        
#        if len(status.text) < 4 + nameLength:
#            continue
#        
#        if status.text[:4] == 'RT @' and status.text[4: 4+nameLength] == screen_name:
#            c += 1
        if re.match('RT @', status.text) != None:
            c+= 1
    return c 
    

#Extract only the data we are interested in.
statuses = getStatuses('DisabRightsFund')
texts = []
isRetweets = []
posted_bys = []
posted_ats = []
original_authors = []
favorite_counts = []
for status in statuses:
    texts.append(status.text)
    posted_ats.append(status.created_at)
    posted_bys.append(status.author.screen_name)
    if not isRetweet(status):
        isRetweets.append(False)
        original_authors.append(status.author.screen_name)
        favorite_counts.append(status.favorite_count)
    else:
        isRetweets.append(True)
        favorite_counts.append(None)
        try:
            original_authors.append(status.retweeted_status.author.name)
        except (tweepy.error.TweepError, AttributeError):
            original_authors.append('')
            
print 'Done extracting data.'

##Consturcut a dataframe
df = DataFrame.from_items([('text', texts), ('posted_at', posted_ats), \
                        ('original_author', original_authors),('posted_by', posted_bys),\
                        ('is_Retweet', isRetweets), ('favorite_count', favorite_counts)])
df.index = df['posted_at']
del df['posted_at']

#DataFrame without the tweets retweeted by the user (i.e. only the user's own tweets)
df_noRetweets = df[df['is_Retweet'] == False]
print 'Done building a dataframe without retweets.'

#Let's look at the actual ttext and count things to get an initial glance in to what's 
#talked about.
tokens = []
for text in df[['text']].values:
    text = map(str,text)[0]
    tokens.extend([t.lower().strip(":,.") for t in text.split()])
#Use a Counter to construct frequency tuples
tokens_counter = Counter(tokens)

#Display some of the most commonly occurring tokens
tokens_counter.most_common(10)

# Now we see too many stopwords.  Let's get rid of them and consider only
# more meaningful words.
import nltk
#nltk.download('stopwords')

#Remove stopwords to decrease noise
for t in nltk.corpus.stopwords.words('english'):
    try:
        tokens_counter.pop(t)
    except KeyError:
        continue
#Redisplay the data
tokens_counter.most_common(20)

words = []
freqs = []
for w,f in tokens_counter.most_common(20):
    words.append(w)
    freqs.append(f)
word_freq = Series(freqs, words)
word_freq.plot(kind = 'barh')

#First look at tweet entities: what are the most frequent tweet enetity?
entities = []
for text in df[['text']].values():
    text = map(str,text)[0]
    for t in text.split():
        if t.startswith('http') or t.startswith('@') or t.startswith('#') or t.startswith('RT @'):
            if not t.startswith('http'):
                t = t.lower()
            entities.append(t.strip(" :,"))
            
entities_counter = Counter(entities)
for entity, freq in entities_counter.most_common():
    print entity, freq