import datetime
import numpy as np
import pandas as pd
import tweepy

from bokeh.plotting import circle, rect
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import String, Instance
from bokeh.server.app import bokeh_app
from bokeh.models.widgets import HBox, VBox, VBoxForm, PreText, Select, TextInput
from bokeh.server.utils.plugins import object_page

####################### User Inputs #######################
CONSUMER_KEY = "rdCgZmY5utBp0YR7wol0ItBWX"
CONSUMER_SECRET = "GUZQKHhH6Oej6RpRnkISyWFid8rLZREYxqM8avMYtJsH575aTc"
OAUTH_TOKEN = "1347715296-651If19TfpqIFQCt1bHnwSHWjhCqzRZCQMd7iKH"
OAUTH_TOKEN_SECRET = "HRoXpMnbuFmhPNTqzMcaAVAKm74I0s5q7UoxJIVk2p3fb"
SCREEN_NAME = "disabrightsfund"

####################### Getting Data #######################
def run_tweepy():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

api = run_tweepy()

#Given a twitter screen_name (user name), as string,
#get dataframe of twitter data
def get_data(screen_name):
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

        df.set_value(index, 'id', item.id)
        df.set_value(index, 'text', item.text)
        df.set_value(index, 'hashtags', str(hashtags))
        df.set_value(index, 'hashtag_count', len(hashtags))
        df.set_value(index, 'retweet_count', item.retweet_count)
        df.set_value(index, 'retweeted', is_retweet(item.text))
        df.set_value(index, 'favorites_count', item.favorite_count)
        df.set_value(index, 'created_at', item.created_at)
        df.set_value(index, 'has_photo', has_photo)

    df['hashtags'] = df['hashtags'].astype(object)
    df['retweet_count'] = df['retweet_count'].astype(int)
    df['favorites_count'] = df['favorites_count'].astype(int)
    df['month'] = [dt.month for dt in df['created_at']]
    df['weekday'] = [dt.weekday() for dt in df['created_at']]
    df['hour'] = [dt.hour for dt in df['created_at']]
    df['created_at'] = df['created_at'] - datetime.timedelta(hours=5)
    
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
    
    plot = Instance(Plot)
    source = Instance(ColumnDataSource)
    text = Instance(TextInput)
    # mainrow = Instance(HBox)
    
    def __init__(self, *args, **kwargs):
        super(TwitterApp, self).__init__(*args, **kwargs)
        self._dfs = {}

    @classmethod
    def create(cls):
        """
        Function is called once, creates all objects (plots, datasources, etc.)
        """

        obj = cls()

        #Layout widgets
        # obj.mainrow = HBox()

        obj.text = TextInput(
            title="title", name="name", value="value"
        )

        obj.make_source()

        #outputs
        obj.make_plots()

        #layout
        obj.set_children()
        return obj

    def make_source(self):
    	print 'make source'
        self.source = ColumnDataSource(data=self.df)

    def make_plots(self):
    	print 'make_plots'
        self.plot = circle(
            'created_at', 'retweet_count',
            title="Engagement by Day",
            source = self.source,
            plot_width=1000, plot_height=400,
            tools="pan,wheel_zoom,select"
        )

    def set_children(self):
        self.children = [self.plot, self.text]
    
    @property
    def df(self):
    	print 'df'
        df = get_data(SCREEN_NAME)
        print df.head(3)
        print
        return df
        # return df[['created_at', 'retweets_count']]

@bokeh_app.route("/bokeh/twitter/")
@object_page("twitter")
def make_object():
    app = TwitterApp.create()
    return app
################### EXECUTABLE STUFF ######################

# df = get_data(SCREEN_NAME)
# print df.head(2)
