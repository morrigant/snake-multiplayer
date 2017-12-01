from django.conf.urls import url

from .views import *

urlpatterns = [
	url(r'^$', MainView.as_view()),
	url(r'^channel$', ChannelView.as_view()),
	url(r'^lose$', LoseView.as_view())
]