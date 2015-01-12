import tweepy
import matplotlib.pyplot as plt
import numpy

#Login credentials to use tweepy
access_token = "220205585-QcUd5fxZNqn3NKuhjVhlUAyyQCFOc3NqUsU2IDtm"
access_token_secret = "T4GTzbMDztGyxtkXL3YKpcm5e1YOjWUsGQOLS9t0FpkLX"
consumer_key = "vPQJv4XS3ExYXS7PNN7fYN1EK"
consumer_secret = "26b1ab1JAuCQ30qg6id5dtrZeQCJOmrf4mkut1GLtVyyMe2LE3"


#Some initialization for logging in and setting up
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

#Returns True if the status given contains a photo; False is returned otherwise
def hasPhoto(status):
    try:
        return status.entities['media'][0]['type']=='photo'
    except KeyError:
        return False
    
#Returns True if the status given contains a video; False is returned otherwise
###############CAN BE IMPROVED!!!!!! Is there another way to figure out if it is a video besides looking at the link url?
def hasVideo(status):
    try:
        return (status.entities['urls'][0]['expanded_url'][0:15]=='http://youtu.be' or status.entities['urls'][0]['expanded_url'][0:15]=='http://youtube.' or status.entities['urls'][0]['expanded_url'][0:16]=='https://youtube.' or status.entities['urls'][0]['expanded_url'][0:16]=='https://youtube.')
    except IndexError:
        return False
    
#Returns the number of hashtags in the given status as an integer.  If there are none, 0 is returned.
def hashtagCount(status):
    return len(status.entities['hashtags'])

#Returns the number of links in the given status as an integer.  If there are none, 0 is returned.
def linkCount(status):
    return len(status.entities['urls'])

#Returns the number of user mentions in the given status as an integer.  If there are none, 0 is returned.
def mentionCount(status):
    return len(status.entities['user_mentions'])

#Returns True if the status given is a retweet; False is returned otherwise
def isRetweet(status):
    if 'RT'==status.text[0:2]:
        return True
    else:
        return False
            
#This is a class compiling all of the attributes of interest in an easier way to interpret
class easyStatus:
    def __init__(self,status):
        self.id=status.id
        self.text=status.text
        self.time=status.created_at
        
        if hasPhoto(status):
            self.photo=1
        else:
            self.photo=0
        if hasVideo(status):
            self.video=1
        else:
            self.video=0
            
        self.hashtags=hashtagCount(status)
        self.links=linkCount(status)
        self.mentions=mentionCount(status)
        
        self.retweets=status.retweet_count
        self.favorites=status.favorite_count

        if isRetweet(status):
            self.isRetweet=1
        else:
            self.isRetweet=0
    
#The rest is the execution

#Make sure you have only the correct username of interest uncommented
username="DisabRightsFund"
##username="UNICEF"
##username="TheArcUS"  

#This gets all the Status objects and converts themm into easyStatus objects
statuses=getStatuses(username)
easyStatuses=[]
for status in statuses:
    easyStatuses=easyStatuses+[easyStatus(status)]
    
#This gets the data
plainCount=0
plainEngagements=0
videoCount=0
videoEngagements=0
photoCount=0
photoEngagements=0
for status in easyStatuses:
    if status.video==1:
        videoCount=videoCount+1
        videoEngagements=videoEngagements+status.retweets+status.favorites
    elif status.photo==1:
        photoCount=photoCount+1
        photoEngagements=photoEngagements+status.retweets+status.favorites
    else:
        plainCount=plainCount+1
        plainEngagements=plainEngagements+status.retweets+status.favorites
if videoCount==0:
    videoAverage=0
else:
    videoAverage=videoEngagements/videoCount
if photoCount==0:
    photoAverage=0
else:
    photoAverage=photoEngagements/photoCount
if plainCount==0:
    plainAverage=0
else:
    plainAverage=plainEngagements/plainCount
averageEngagements=[plainAverage, photoAverage, videoAverage]
media=['Text','Photo','Video']

# Enable inline plotting
%matplotlib inline

data = averageEngagements

xDataLabels=media
yAxisLabel='Engagements'
title='Average Engagements by Medium'

ind = numpy.arange(len(data))  # This sets up the indices of the data given.  As far as I can tell, it uses the same order as the data you provide
widthOfColumns = 1      # the width of the bars. A width of one has them all touching

fig, ax = plt.subplots()
ax.bar(ind, data, widthOfColumns, color='b') #Can also take an argument called yerr

ax.set_ylabel(yAxisLabel)
ax.set_title(title)
ax.set_xticks(ind+[widthOfColumns/2])
ax.set_xticklabels(xDataLabels)

plt.show()
