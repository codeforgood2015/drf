#Returns True if the status given contains a photo; False is returned otherwise
def hasPhoto(status):
    try:
        return status.entities['media'][0]['type']=='photo'
    except KeyError:
        return False
    
#Returns True if the status given contains a video; False is returned otherwise
###############CAN BE IMPROVED!!!!!! Is there another way to figure out if it is a video besides looking at the link url?  This method is pretty lacking right now.
def hasVideo(status):
    try:
        return (status.entities['urls'][0]['expanded_url'][0:15]=='http://youtu.be' or status.entities['urls'][0]['expanded_url'][0:15]=='http://youtube.')
    except IndexError:
        return False
    
#Returns the number of hashtags in the given status as an integer.  If there are none, 0 is returned.
def hashtagCount(status):
    return len(status.entities['hashtags'])

#Returns the number of links in the given status as an integer.  If there are none, 0 is returned.
def linkCount(status):
    if hasVideo(status):
      return 0
    else:
      return len(status.entities['urls'])

#Returns the number of user mentions in the given status as an integer.  If there are none, 0 is returned.
def mentionCount(status):
    return len(status.entities['user_mentions'])

#Returns True if the status given is a retweet; False is returned otherwise
def isRetweet(status):
    if 'RT '==status.text[0:2]:
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
