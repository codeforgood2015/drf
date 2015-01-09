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

#Gets all statuses, or as many as possible before the rate limit is exceeded
def getStatuses(username, includeRetweets=False):
    statuses=[]
    canGetTweets=True
    i=tweepy.Cursor(api.user_timeline, screen_name=username).items()
    while canGetTweets:
        try:
            nextTweet=i.next()
            if (isRetweet(nextTweet) and includeRetweets) or (isRetweet(nextTweet)==False):
                statuses=statuses+[nextTweet]
        except (tweepy.error.TweepError, StopIteration):
             canGetTweets=False
    return statuses
    
#Returns True if the status given is a retweet; False is returned otherwise
def isRetweet(status):
    if 'RT'==status.text[0:2]:
        return True
    else:
        return False

#Some attributes of the Status object we can use (Add more if you find more useful ones)
#text
#created_at  #This is the post time
#retweet_count
#favorite_count
#entities    #This is a dictionary including things like media, urls, hashtags, user_mentions
