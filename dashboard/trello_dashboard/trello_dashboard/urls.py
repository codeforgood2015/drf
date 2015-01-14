from django.conf.urls import patterns, include, url
from django.contrib import admin
from dashing.utils import router
from widgets import CustomWidget

router.register(CustomWidget, 'custom_widget')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'trello_dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include(router.urls)),
    # url(r'^trello_cards/$', TrelloCards.as_view(), name='trello_cards_widget'),
)

