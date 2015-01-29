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
import nltk
#import engagementsvsmedia
#nltk.download('stopwords')
from collections import Counter, defaultdict
from pandas import DataFrame, Series
#
###Login credentials to use tweepy; these are my credentials, but you probably need your own.
#access_token = "1347715296-651If19TfpqIFQCt1bHnwSHWjhCqzRZCQMd7iKH"
#access_token_secret = "HRoXpMnbuFmhPNTqzMcaAVAKm74I0s5q7UoxJIVk2p3fb"
#consumer_key = "rdCgZmY5utBp0YR7wol0ItBWX"
#consumer_secret = "GUZQKHhH6Oej6RpRnkISyWFid8rLZREYxqM8avMYtJsH575aTc"


###If the rate is exceeded, alternate with the below keys.
access_token = "2233842882-Q7gMjff1xDrSkJCFl8p27vqM8Vid1pSFEGekkO9"
access_token_secret = "Gbi7D04wxwD95dcjynbQqDOnAFbgSb8RqVhPvXbzGv2xc"
consumer_key = "5y1IFTVt5L4NaQrsmZuplj1je"
consumer_secret = "kiRGUe7p535v0mD3yiLTJHKkO7QmM9OBVWNRwDI4ZvPnkXMyy4"

#Third tokens
#consumer_secret = "3oxUYDpxtSctph7pg2WBlpkHHeREBJvfpuYCs57MZBJwNraddD"
#access_token = "2233842882-47QJOE6KkJQjyvxf5EwGvnUZ1eYROLWZmyWqWJX"
#access_token_secret = "OkpI7OG7bCocqSbCWQBcCNDCa3Zb0AfP5CBfVzB0nYHfq"
#consumer_key = "sASEh024SKmPvq1KiikEYcsLr"


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
    return status.text.startswith('RT @')
        

def isReply(status):
    return status.text.startswith('@') or status.text.startswith('.@')

def filterWordDict():
    """Removes meaningless words, stopwords, punctuations, '@username',
    etc
    """
    pass
def createDF():
    """
    """
    pass

def topN(df):
    """
    Returns a new dataframe sorted by the 
    """
    pass
def getWordFreq(screen_name, n = 20):
    """Counts the word frequency in the top n most 'engaging' (i.e. attractive 
    to retweets and favorites) tweets and returns a bar graph of the result.
    """

    statuses = getStatuses(screen_name)
    
    texts = []
    isRetweets = []
    isReplys=[]
    posted_bys = []
    posted_ats = []
    original_authors = []
    favorite_counts = []
    retweet_counts = []
    for status in statuses:
        texts.append(status.text)
        posted_ats.append(status.created_at)
        posted_bys.append(status.author.screen_name)
        isRetweets.append(isRetweet(status))
        isReplys.append(isReply(status))
        
        if not isRetweet(status): #not a retweet
            original_authors.append(status.author.screen_name)
            favorite_counts.append(status.favorite_count)
            retweet_counts.append(status.retweet_count)
        else:
            favorite_counts.append(None)
            retweet_counts.append(None)
            try:
                original_authors.append(status.retweeted_status.author.name)
            except (tweepy.error.TweepError, AttributeError):
                original_authors.append('')
                
    print 'Done extracting data.'
    
    ##Consturcut a dataframe
    df = DataFrame.from_items([('text', texts), ('posted_at', posted_ats), \
                            ('original_author', original_authors),('posted_by', posted_bys),\
                            ('is_retweet', isRetweets), ('is_reply', isReplys),\
                            ('favorite_count', favorite_counts),\
                            ('retweet_count', retweet_counts)])
    df['engagement_count'] = df['favorite_count'] + df['retweet_count']
    
    df.index = df['posted_at']
    del df['posted_at']
    
    #DataFrame without the tweets retweeted by the user (i.e. only the user's own tweets)
    #and without the user's replies
    #df_cleaned is the dataframe with only the tweets "purely" by the user.
    df_cleaned = df[(df.is_retweet == False) & (df.is_reply == False)]
    print 'Done building a dataframe without retweets and replies.'
    
    #Order df_noRetweets by #engagements
    df_cleaned.sort('engagement_count', inplace = True, ascending = False)
    
    #Want to look at top n most engaging tweets:
    df_topN = df_cleaned[:n]
    
    #Let's look at the actual text and count things to get an initial glance in to what's 
    #talked about.
    tokens = []
    for text in df_topN[['text']].values:
        text = map(lambda x: x.encode('utf-8'),text)[0]
        wList = text.split()
        filtered = []
        for w in wList:
            if not (w.startswith('http://') or w.startswith('@') or w.startswith('#') or w.startswith('&') or w.startswith ('-') or w.isdigit()):
                filtered.append(w.strip('.,-*').lower())
                
        tokens.extend(filtered)
    #Use a Counter to construct frequency tuples
    tokens_counter = Counter(tokens)
    
    #Display some of the most commonly occurring tokens
    print tokens_counter.most_common(15)
    
    
    #Remove stopwords to decrease noise
    for t in nltk.corpus.stopwords.words('english'):
        try:
            tokens_counter.pop(t)
        except KeyError:
            continue
    
    #Redisplay the data
    tokens_counter.most_common(15)
    
    words = []
    freqs = []
    for w,f in tokens_counter.most_common(15):
        words.append(w)
        freqs.append(f)
    word_freq = Series(freqs, words)
    word_freq.plot(kind = 'barh', title = screen_name)
    return word_freq


##First look at tweet entities: what are the most frequent tweet entity?
#entities = Counter()
#for text in df['text']:
#    text = str(text)
#    if text.startswith('@') or text.startswith('.@'):
#        entities['reply'] += 1
#    elif text.startswith('RT @'):
#        entities['retweet']+= 1
#    else: 
#        entities['my_own'] += 1
#e_dict = dict()
#for e, freq in entities.iteritems():
#    e_dict[e] = freq
#e_freq = Series(e_dict)
#Series.sort(e_freq,ascending = False, inplace = True)
#e_freq.plot(kind='bar')
#
#    
##Make a pie graph of entities.
#nTot = e_freq.sum()
#labels = []
#fracs = []
#for k,v in e_dict.iteritems():
#    labels.append(k)
#    fracs.append(v)
#fracs = map(lambda x: (x*100)/float(nTot), fracs)
#plt.pie(fracs, labels = labels, autopct='%1.1f%%', startangle = 90, shadow=True)
#plt.legend(title = 'Entities', loc = "best")
#plt.axis('equal')
#plt.tight_layout()
#
##Now, I want to analyze the engagement rates vs time/media
##First add a new column, 'media'.
#dates = Series(df_topN.index.format())
#df_topN['text'].str.contains('people')
#video = df[df['posted_at'] == 2012]


#screen_name = "TheArcUS"
#screen_name = "InclusionIntl"
#screen_name = "DisabRightsFund"
#screen_name = "unicefusa"
#screen_name = "gatesfoundation"
#screen_name = "Pontifex"  #Pope Francis
#screen_name = "nytimes"
#screen_name = "BarackObama"
#myStatuses = getStatuses('breathsong')
#nList = ["HI_UnitedStates", "InclusionIntl", "DisabRightsFund", "unicefusa", "gatesfoundation"]
#getWordFreq(screen_name, n = 50)