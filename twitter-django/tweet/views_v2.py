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

from itertools import cycle
 
from tweepy import api

from tweepy import auth


class ApiRequest():
  def __init__(self):
    self.consumer_key=["XYF0V608bI5xmllxZuxtayPar", "jRM0SHeVWKODq3NIteJVsfL6V",
                       "d9UmoZGmGO9uYzJe3ovy42JwY", "LWtSeYatGGdrFy2oNmZGrCMyP"]
    self.consumer_secret=["WIeXHr69hm8bDYflybFmCJEZGzQD9PbiaEOdWF7M8ONl7uBkNf",
                          "eCxkQelePRrsVscq9pZ7ximu6iGNsTA54DZdE3Uevy3xcurvXj",
                          "5xuKF6OWu1Xg65Ncz7gJPLhkPlx6OU2YHJxOZohlQlwUs1WyyD",
                          "Cxqo8Iip833Dav2pQh5zAoW7C6cKah8a2YgSF8aCBpy1trSjnu"]
    self.access_token=["1233464466-NpTPhscTpE8S3q3i5E33rOnFi2cpb3dy5FYILYe",
                       "1233464466-Sk7F532jp8pNjniDa14p0MPZTD1zyjcfwV75geN",
                       "1233464466-bAiObz4tqasFGZ6IftI5x4YwBS1fApwEWHs4rXN",
                       "1233464466-Gv7Oxe0aU5X9RtdmvKZ0I7yv8s6c8oR3hcxE0Xo"]
    self.access_token_secret=["DLV5S5alKbmC2pFyrK7rFeZZNtMRINAa0OtdVK2GjlZQS",
                              "9j9dgfgGwfgEvx3cSfOmceawXOwSxjj6MMeYnO0kgIwkz",
                              "fw78xbxukkUxqQ2y0aYwMOkJH1OCmjAcAOPPHWgWQQHLG",
                              "ZnBC4O6oJ5OvzCRZT2C5PaQiv7d2iHFaZZFxsdSFskqRq"]
    
    self.oauthList = []
    for i in xrange(0,len(self.consumer_key)):
      self.oauth = auth.OAuthHandler(self.consumer_key[i], self.consumer_secret[i])
      self.oauth.set_access_token(self.access_token[i], self.access_token_secret[i])
      self.oauthList.append(self.oauth)

    self.myIterator = cycle(self.oauthList)

  def getApiRequest(self):
    return api.API(self.myIterator.next())


total_tweets = 0
LAST_ID = ''


class HashTag(db.Model):
  pass

class HashTagTweets(db.Model):
  text = db.StringProperty(multiline=True)
  fetch_date = db.DateProperty()
  created_at = db.StringProperty()
  hashtag = db.StringProperty()
  state = db.StringProperty()


class ProfileTweets(db.Model):
  #tweet = DictProperty()
  text = db.StringProperty(multiline=True)
  fetch_date = db.DateProperty()
  created_at = db.StringProperty()
  screen_name = db.StringProperty()


class Traversal:
  def __init__(self):
    self.apiRequest = ApiRequest()


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
          t = ProfileTweets(text=str(tweet.text.encode('ascii', 'ignore')), screen_name=user,
                    created_at=str(tweet.created_at),
                    fetch_date=datetime.datetime.now().date())
          t.put()
          i +=  1
          total_tweets = total_tweets + 1

      logging.info("Profile Tweets added to Appengine!")

      #self.searchTweets(user, int(max_id)-1)

  
  def getHashTags(self, entities):
    if 'hashtags' in entities:
      logging.info('hashtags>>>')
      logging.info(entities['hashtags'])
      return entities['hashtags']


  def addHashTags(self, tweets):
    for tweet in tweets:
      hashtags = self.getHashTags(tweet.entities)
      try:
        for hashtag in hashtags:
          logging.info('hashtag text')
          logging.info(hashtag['text'])
          HashTag.get_or_insert(hashtag['text'])
      except:
        pass


  '''
  searchTweets function to make a search request to the twitter api using tweepy.
  @param: search String hashtag used for the search.
  @param: state String name of the state.
  @param: geocode String geocode of the location in a state.
  @param: max_id  String id of the last tweet fetched from the previous search request.
  '''
  def getUserTweets(self, user, max_id=None):
    try:
      tweets = self.apiRequest.getApiRequest().user_timeline(screen_name=user, count=100, max_id=max_id)
      if len(tweets) != 0:
        self.addHashTags(tweets)
        return tweets
      else:
         logging.info('No tweets found!')
    except:
      logging.info("Exception caught! at line 146")





  def addHashTagTweets(self, tweets, hashtag, state, geocode, max_id):
      i = 0
      global total_tweets
      for tweet in tweets:
          #tweet = json.loads(str(tweet))
          max_id = tweet.id_str
          t = HashTagTweets(text=str(tweet.text.encode('ascii', 'ignore')), hashtag=hashtag,
                    created_at=str(tweet.created_at),
                    fetch_date=datetime.datetime.now().date(), state=state)
          t.put()
          i +=  1
          total_tweets = total_tweets + 1

      logging.info("Tweets for hashtag added to Appengine!")



  '''
  searchTweets function to make a search request to the twitter api using tweepy.
  @param: search String hashtag used for the search.
  @param: state String name of the state.
  @param: geocode String geocode of the location in a state.
  @param: max_id  String id of the last tweet fetched from the previous search request.
  '''
  def searchHashTagTweets(self, search, state, geocode, max_id=None):
    try:
      tweets = self.apiRequest.getApiRequest().search(q=search, count=100, max_id=max_id, geocode=geocode)
      if len(tweets) != 0:
        self.addHashTagTweets(tweets, search, state, geocode, max_id)
      else:
        logging.info("No tweets found!")
    except:
      logging.info("Exception caught! at line 183")



  '''
  getGeoCodes function to get the geo codes with states and the radius of the area.
  @return: dict dict_object geo codes with state name and the radius.
  '''
  def getGeoCodes(self):
    #print  'getGeoCodes called:'
    dict_object = {}
    with open('us_cities.csv') as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        state = row[1]
        geocode = row[2] + ',-' + row[3] + ',10mi'
        dict_object[geocode] = state
    return dict_object



  '''
  geoTweets function to fetch tweets based on geo locations.
  @param: search String hashtag used for fetching tweets.
  '''
  def geoTweets(self, search):
      #print  'geoTweets called:'
      #print  'search tweets for%s' % search
      geocodes = self.getGeoCodes()
      state_count = 0
      for geocode, state in geocodes.iteritems():
        ##print  state

        if state in ['CA', 'IA', 'FL', 'NY', 'WA']:
          #print  state
          self.searchHashTagTweets(search, state, geocode, None)
          #geo_count = + 1
          state_count = state_count + 1

      #print  'state count%s' % state_count


def getProfileTweets(traversal):
  #logging.info('2. fetchTweets called')
  #traversal = Traversal()

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
    tweets = traversal.getUserTweets(user=user)
    traversal.addTweets(tweets, user, max_id=None)

  #logging.info('total tweets %s' % total_tweets)

def getHashTagTweets(traversal):
  hashtags = HashTag.all()
  #hashtags=['obama']
  for h in hashtags:
    #logging.info('hashtags=%s', h)
    #logging.info('hashtag=%s', h.key().name())
    traversal.geoTweets(search=h)


def getTweets(request):
  traversal = Traversal()
  global COUNT
  COUNT = 0
  #logging.info('1. getTweets called')
  getProfileTweets(traversal)
  getHashTagTweets(traversal)
  return http.HttpResponse('Tweets saved!')

