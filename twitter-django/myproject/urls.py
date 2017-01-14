from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'fetchtweets', 'tweet.views.getTweets'),
    url(r'csv', 'tweet.views.getcsv'),
    url(r'tweetscount', 'tweet.views.tweetsCount'),
    url(r'gettags', 'tweet.views.gethashtag')
)
