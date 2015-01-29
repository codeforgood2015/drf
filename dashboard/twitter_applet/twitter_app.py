import datetime
import numpy as np
import pandas as pd
import tweepy
from facepy import GraphAPI
import facepy
import datetime
import facebookData as fbd


from bokeh.plotting import circle, rect, line
from bokeh.models import Plot, ColumnDataSource, HoverTool
from bokeh.properties import String, Instance
from bokeh.server.app import bokeh_app
from bokeh.models.widgets import HBox, VBox, VBoxForm, PreText, Select, TextInput
from bokeh.server.utils.plugins import object_page
from collections import OrderedDict

####################### User Inputs #######################
# DRF's Keys
CONSUMER_KEY = "rdCgZmY5utBp0YR7wol0ItBWX"
CONSUMER_SECRET = "GUZQKHhH6Oej6RpRnkISyWFid8rLZREYxqM8avMYtJsH575aTc"
OAUTH_TOKEN = "1347715296-651If19TfpqIFQCt1bHnwSHWjhCqzRZCQMd7iKH"
OAUTH_TOKEN_SECRET = "HRoXpMnbuFmhPNTqzMcaAVAKm74I0s5q7UoxJIVk2p3fb"


SCREEN_NAME = "disabrightsfund"
FB_ID = "182413241850729"
####################### Getting Data #######################
def run_tweepy():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

#Don't need to call b/c facepy handled in facebookData
def run_facepy():
    #Makes auth calls (takes time)
    oauth_access_token = facepy.utils.get_application_access_token(APP_ID, APP_SECRET)

    #This just gets access
    graph = GraphAPI(oauth_access_token)
    return graph

api = run_tweepy()

#Given a twitter screen_name (user name), as string,
#get dataframe of twitter data
def get_twitter_data(screen_name):
    df = pd.DataFrame(columns=('created_at', 'id', 'text', 'hashtag_count', 'retweet_count', 
                               'retweeted', 'favorites_count', 'has_photo'), dtype=None)
    
    #populating dataframe
    for item in tweepy.Cursor(api.user_timeline, screen_name=screen_name).items(100):
        index = len(df)

        hashtags=[]
        for ht in item.entities['hashtags']:
            hashtags.append(ht['text'])

        try:
            has_photo = item.entities['media'][0]['type']=='photo'
        except KeyError:
            has_photo = False

        try:
            has_video = (item.entities['urls'][0]['expanded_url'][0:15]=='http://youtu.be' 
                or item.entities['urls'][0]['expanded_url'][0:15]=='http://youtube.' 
                or item.entities['urls'][0]['expanded_url'][0:16]=='https://youtube.' 
                or item.entities['urls'][0]['expanded_url'][0:16]=='https://youtube.')
        except IndexError:
            has_video = False

        df.set_value(index, 'id', item.id)
        df.set_value(index, 'text', item.text)
        df.set_value(index, 'hashtags', str(hashtags))
        df.set_value(index, 'hashtag_count', len(hashtags))
        df.set_value(index, 'retweet_count', item.retweet_count)
        df.set_value(index, 'retweeted', is_retweet(item.text))
        df.set_value(index, 'favorites_count', item.favorite_count)
        df.set_value(index, 'created_at', item.created_at)
        df.set_value(index, 'has_photo', has_photo)
        df.set_value(index, 'has_video', has_video)

    df['hashtags'] = df['hashtags'].astype(object)
    df['retweet_count'] = df['retweet_count'].astype(int)
    df['favorites_count'] = df['favorites_count'].astype(int)
    df['month'] = [dt.month for dt in df['created_at']]
    df['weekday'] = [dt.weekday() for dt in df['created_at']]
    df['hour'] = [dt.hour for dt in df['created_at']]
    df['created_at'] = df['created_at'] - datetime.timedelta(hours=5)
    df['tweet_engagement'] = df['favorites_count'] + df['retweet_count']
    # df['time_fmt'] = [dt.strfttime("%x, %H:%M%p") for dt in df['created_at']]
    
    return df

def get_fb_data(id):
    posts = fbd.getAllEasyPosts(id)
    df = pd.DataFrame(columns=('time', 'type', 'text', 'likes_count', 'comments_count', 'shares_count', 'hour', 'weekday'), dtype=None)
    index = len(df)
    
    for post in posts:
        #2015-01-27T13:30:27+0000
        post_time = datetime.datetime.strptime(post.time, "%Y-%m-%dT%H:%M:%S+0000")    
        df.set_value(index, 'type', post.type)
        df.set_value(index, 'text', post.words)
        df.set_value(index, 'likes_count', post.likes)
        df.set_value(index, 'shares_count', post.shares)
        df.set_value(index, 'comments_count', post.comments)
        df.set_value(index, 'time', post_time)
        
        index+=1
    
    df['post_engagement'] = df['likes_count'] + 2 * df['shares_count'] + 3 * df['comments_count']
    df['hour'] = [dt.hour for dt in df['time']]
    df['weekday'] = [dt.weekday() for dt in df['time']]
    
    return df

#Given data (as dataframe) and time_step (string: 'weekday', 'hour', month')
def plot_engagement(data, time_step):
    accepted_steps = ('month', 'weekday', 'hour')
    if time_step not in accepted_steps:
        print 'incorrect time step!'
        return False
    
    if time_step=='month':
        output = data[['retweet_count', 'favorites_count']].groupby(data['month']).agg(mean)
#         output.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Out', 'Nov', 'Dec']
    elif time_step=='weekday':               
        output = data[['retweet_count', 'favorites_count']].groupby(data['weekday']).agg(mean)
#         output.index = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    elif time_step=='hour':               
        output = data[['retweet_count', 'favorites_count']].groupby(data['hour']).agg(mean)
    
    output.plot(kind='bar', stacked='True')        
    return True


#Given twitter, message redetermines if it is retweet
#(if it begins with "RT @"...)
def is_retweet(msg):
    if len(msg)<4:
        return false
    return msg[0:4]=="RT @"

################## Making Graphs/Apps #####################
class TwitterApp(VBox):
    extra_generated_classes = [["TwitterApp", "TwitterApp", "VBox"]]
    jsmodel = "VBox"
    
    top_row = Instance(HBox) #contains engage_plot, tweet_info
    row_2 = Instance(HBox)
    row_3 = Instance(HBox)

    engage_plot = Instance(Plot)
    engage_fb_plot = Instance(Plot)
    tweet_text = Instance(PreText)
    # account_text = Instance(PreText)
    source_twitter = Instance(ColumnDataSource)
    source_fb = Instance(ColumnDataSource)
    # mainrow = Instance(HBox)
    
    def __init__(self, *args, **kwargs):
        super(TwitterApp, self).__init__(*args, **kwargs)
        self._dfs = {}

    @classmethod
    def create(cls):
        """
        Function is called once, creates all objects (plots, datasources, etc.)
        """
        
        #Layout widgets
        obj = cls()
        obj.top_row = HBox()
        obj.row_2 = HBox()
        obj.row_3 = HBox()

        obj.make_source()

        #outputs
        obj.tweet_text = PreText(text="", width=1000, height=150)
        # obj.account_text = PreText(text="", width=200)
        obj.make_plots()

        #layout
        obj.set_children()
        return obj

    def make_source(self):
    	print 'make source'
        self.source_twitter = ColumnDataSource(data=self.df_twitter)
        self.source_fb = ColumnDataSource(data=self.df_fb)

    def make_engagement_plot(self):
        print 'make_engagement'
        self.engage_plot = circle(
            'created_at', 'tweet_engagement',
            title="Twitter Engagement by Tweet",
            source = self.source_twitter,
            plot_width=800, plot_height=400,
            x_axis_type='datetime',
            size = 10,
            alpha = 0.7,
            tools="pan,box_zoom,select,hover,reset"
        )
        hover = self.engage_plot.select(dict(type=HoverTool))

        hover.tooltips = OrderedDict([
            ("Hashtags: ", "@hashtags"),
            ("# Favorites: ", "@favorites_count"),
            ("# Retweets: ", "@retweet_count")

        ])

    def make_fb_engagement_plot(self):
        print 'make fb engagement'
        self.engage_fb_plot = circle(
            'time', 'post_engagement',
            title = "Facebook Engagement by Post",
            source = self.source_fb,
            plot_width=800, plot_height=400,
            x_axis_type='datetime',
            size=15,
            alpha=0.7,
            tools="pan,box_zoom,select,hover,reset"
        )
        hover = self.engage_fb_plot.select(dict(type=HoverTool))

        # hover.tooltips = OrderedDict([
        #     ("Date: ", "@"
        # ])

    def make_stats(self):
        recent_tweets = self.df_twitter[['created_at', 'text', 'retweet_count', 'favorites_count']].sort(columns='created_at', ascending=False)
        self.tweet_text.text = recent_tweets.head(5).to_string()

    def make_plots(self):
        print 'make_plots'
        self.make_engagement_plot()
        self.make_fb_engagement_plot()
        self.make_stats()

    def set_children(self):
        self.children = [self.top_row, self.row_2, self.row_3]        
        self.top_row.children = [self.engage_plot]
        self.row_2.children = [self.tweet_text]
        self.row_3.children = [self.engage_fb_plot]
    
    @property
    def df_twitter(self):
    	print 'df_twitter'
        df_twitter = get_twitter_data(SCREEN_NAME)
        return df_twitter
    
    @property
    def df_fb(self):
        print 'df_fb'
        df_fb = get_fb_data(FB_ID)
        return df_fb

@bokeh_app.route("/bokeh/twitter/")
@object_page("twitter")
def make_object():
    app = TwitterApp.create()
    return app
