from django import http
import datetime
from google.appengine.ext import db
from google.appengine.api import users
from django.utils import simplejson as json
import pickle

import time
import datetime
import sys
import json
import csv
import logging
 
from tweepy import api

from tweepy import auth

COUNT = 0
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

consumer_key="RnnctjGXhDl00B8zYaW232TNG"
consumer_secret="QTwOq7mNtmELrtlg6HcgilhuNKv3YHQcNo2yQRPU3KHDiz7ERB"
access_token="1233464466-ALmCWhhCAmYqxMssz3TSZQwM6q2QhIwwIPMOnVM"
access_token_secret="1zs4xJXyvr9OuzYG9WIQQpoUSggtAAHYk0aY42bYfeECq"

oauth = auth.OAuthHandler(consumer_key, consumer_secret)
oauth.set_access_token(access_token, access_token_secret)
api_request = api.API(oauth)

total_tweets = 0
LAST_ID = ''



class Tweet(db.Model):
  #tweet = DictProperty()
  text = db.StringProperty(multiline=True)
  fetch_date = db.DateProperty()
  created_at = db.StringProperty()
  screen_name = db.StringProperty()


class Traversal:
  def __init__(self):
    pass


  '''
  addTweets function to add data to our graph database.
  @param: tweets json tweets fetched from the twitter.
  @param: search String hashtag used for the search.
  @param: state String name of the state to get the twitter messages.
  @param: geocode String geo code of the location used for fetching tweets.
  @param: max_id String id of the last tweet fetched from the previous request.
  '''
  def addTweets(self, tweets, user, max_id=None):
      #logging.info('addTweets Called:')
      #logging.info('search=%s' % user)


      tweet_list = []

      i = 0
      global total_tweets
      for tweet in tweets:
          #tweet = json.loads(str(tweet))
          max_id = tweet.id_str
          t = Tweet(text=str(tweet.text.encode('ascii', 'ignore')), screen_name=user,
                    created_at=str(tweet.created_at),
                    fetch_date=datetime.datetime.now().date())
          t.put()
          i +=  1
          total_tweets = total_tweets + 1

      logging.info("Tweets added to Appengine!")

      #self.searchTweets(user, int(max_id)-1)


  '''
  searchTweets function to make a search request to the twitter api using tweepy.
  @param: search String hashtag used for the search.
  @param: state String name of the state.
  @param: geocode String geocode of the location in a state.
  @param: max_id  String id of the last tweet fetched from the previous search request.
  '''
  def searchTweets(self, user, max_id=None):
      #logging.info('searchTweets called:')
      #logging.info('search tweets for %s' % user)
      global COUNT
      COUNT += 1
      if COUNT < 300:
        tweets = api_request.user_timeline(screen_name=user, count=100, max_id=max_id)
        if len(tweets) != 0:
          self.addTweets(tweets, user, max_id)
        else:
          #print tweets
           logging.info('No tweets found!')
      else:
        logging.info('Dont fetch more tweets')
        pass


def fetchTweets():
  #logging.info('2. fetchTweets called')
  traversal = Traversal()

  users = ['nat_herz', 'aliarau', 'AO_DKloap', 
           'melmason', 'joeybunch', 'capitolwatch', 'JWStarkey', 'kmcgrory', 
           'ajcpolitics', 'cynthiasewell', 'Jessiehellmann',
           'Indystartony', 'JasonnobleDMR', 'BryanLowry3', 'TomLoftus_CJ', 
           'MarshaShulerCNB', 'Stevemistler', 'ErinatTheSun',
           'JM_Bos', 'ChadLivengood', 'PatrickCondon', 'GeoffPender', 'J_Hancock', 
           'mikedennison', 'robynntysver', 'SteveSebelius',
           'Grayno2', 'SusanKLivio', 'DanBoydNM', 'JesseMckinley', 'bkcolin', 
           'MacphersonJA', 'JMBorchardt', 'rickrmgreen', 'IanKullgren',
           'inkyamy', 'kathyprojo', 'Jeremy_Borden', 'ArgusJellis', 'ricklocker', 
           'RobertTGarrett', 'LeeHDavidson', 'aprilburbank', 'patrickmwilson',
           'olympiajoe', 'PhilKabler', 'PatrickdMarley', 'Laurahancock', 
           'Jasonmdstein'] 

  for user in users:
    logging.info('seach tweets for %s' % user)
    traversal.searchTweets(user=user)

  #logging.info('total tweets %s' % total_tweets)


def getTweets(request):
  global COUNT
  COUNT = 0
  #logging.info('1. getTweets called')
  fetchTweets()
  return http.HttpResponse('Tweets saved!')

