from django.conf import settings
from dashing.widgets import NumberWidget
#from trello import TrelloAi

#trello = TrelloApi(settings.TRELLO_APP_KEY)

class TrelloCards(NumberWidget):
    title = 'Trello Dev Cards'
    def get_more_info(self):
        return '{} closed'.format(len(trello.boards.get_card_filter('closed', 
        '4d5ea62fd76aa1136000000c')))
    
    def get_change_rate(self):
        return '{} open'.format(len(trello.boards.get_card_filter('open', 
        '4d5ea62fd76aa1136000000c')))

    def get_value(self):
        return len(trello.boards.get_card_filter('all', '4d5ea62fd76aa1136000000c'))

class CustomWidget(NumberWidget):
    title = "Benji\'s Custom Widget"
    value = 15

    def get_more_info(self):
        more_info = "Benji was here."
        return more_info


