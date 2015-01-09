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

#This gets all statuses from a profile with the given username and returns them as a list; I find it to be a helpful place to start
#An improvement that can be made is on how to stop it before the rate limit is reached.
def getStatuses(username):
    statuses=[]
    for status in tweepy.Cursor(api.user_timeline, screen_name=username).items():
        statuses=statuses+[status]
        if len(statuses)>180:
            break        
    return statuses

#Some attributes of the Status object we can use (Add more if you find more useful ones)
#text
#created_at  #This is the post time
#retweet_count
#favorite_count
#entities    #This is a dictionary including things like media, urls, hashtags, user_mentions
