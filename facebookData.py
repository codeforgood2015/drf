from facepy import GraphAPI
#This comes from your Facebook and must be updated frequently.  Also, if you don't get it a certain way, it won't give you all the necessary permissions.  Let me know if you have trouble with this.
oauth_access_token='CAACEdEose0cBAJ04gZC1ZAWjEh79TdZCkWlITGzswjVoVJvCeCxECrXIspXkXzeF54tCdBrCrumcsgVLjgd8NKvsroZCfIBmTuEHwgr77i2OhX97ZAKfMY0EGQtlke9C824vGxI5l6gmARIgzW2AUAL5Gqpy6wKg0nKkDHrsQ7VZCjNRpGYhw3ZC3aFMIZB46EvmGUuBQomigqrShbpziP7S'
#This just gets access
graph = GraphAPI(oauth_access_token)

#This gets the words from a post. Sometimes, there aren't any, in which case "No words could be found for this post" is returned. I'm not sure why this happens
def getWords(post):
    try:
        words=post['message']
    except KeyError:
        try:
            words=post['story']
        except KeyError:
            words="No words could be found for this post"
    return words

#This returns the number of likes a post has.
def getLikes(post):
    try:
        likes=len(post['likes']['data'])
    except KeyError:
        likes=0
    return likes

#This returns the number of comments a post has.
def getComments(post):
    try:
        comments=len(post['comments']['data'])
    except KeyError:
        comments=0
    return comments

#This returns the number of shares a post has.
def getShares(post):
    try:
        shares=post['shares']['count']
    except:
        shares=0
    return shares

#This returns the type of post according to the GraphAPI.  There are lots of types, and I am not sure what they all mean, so there is still work to be done here
def getType(post):
    try:
        postType=post['status_type']
    except KeyError:
        postType=post['type']
    return postType

#This gets the time a post was posted.  I haven't looked into adjusting for timezone yet.
def getTime(post):
    try:
        time=post['created_time']
    except KeyError:
        time='No time could be found for this post'
    return time

#This provides a convenient way to work with post data.
class easyPost:
    def __init__(self, post):
        self.words=getWords(post)
        self.type=getType(post)
        self.time=getTime(post)
        
        self.likes=getLikes(post)
        self.comments=getComments(post)
        self.shares=getShares(post)

#This turns posts into easyPosts
def geteasyPosts(posts):
    easyPosts=[]
    try:
        for post in posts['posts']['data']:
            easyPosts=easyPosts+[easyPost(post)]
    except KeyError:
        for post in posts['data']:
            easyPosts=easyPosts+[easyPost(post)]
    return easyPosts

#This uses the paging of posts to get the next posts
def getNextPosts(posts):
    try:
        nextQuery=posts['posts']['paging']['next'][32:]
    except KeyError:
        nextQuery=posts['paging']['next'][32:]
    nextPosts=graph.get(nextQuery)
    return nextPosts

#This gets all posts from a page and turns them into easyPosts
def getAlleasyPosts(ID):
    posts=graph.get(ID+'/posts')
    easyPosts=geteasyPosts(posts)
    try:
        postArray=[getNextPosts(posts)]
        easyPosts=easyPosts+geteasyPosts(postArray[0])
        canContinue=True
    except KeyError:
        canContinue=False
    while canContinue:
        try:
            postArray=postArray+[getNextPosts(postArray[-1])]
            easyPosts=easyPosts+geteasyPosts(postArray[-1])
        except KeyError:
            canContinue=False
    return easyPosts

#This dictionary can be used to keep track of ID numbers we need
ID={'DRF': '182413241850729'} 

#Execution
easyPosts=getAlleasyPosts(ID['DRF'])
for post in easyPosts:
    print(post.words)
    print('Likes: '+str(post.likes)+' Comments: '+str(post.comments)+' Shares: '+str(post.shares)) 
