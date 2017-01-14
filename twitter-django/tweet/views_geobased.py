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
xyz = api.API()
from tweepy import auth

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

consumer_key="hcOoYKIzVSSQgNGZTyxahsatI"
consumer_secret="zc9pqv59jxoktghY0QbUcs7I5s0nEhX7HFJB8XXY5G2tO7JJjP"
access_token="1233464466-ALmCWhhCAmYqxMssz3TSZQwM6q2QhIwwIPMOnVM"
access_token_secret="1zs4xJXyvr9OuzYG9WIQQpoUSggtAAHYk0aY42bYfeECq"

oauth = auth.OAuthHandler(consumer_key, consumer_secret)
oauth.set_access_token(access_token, access_token_secret)
api_request = api.API(oauth)

total_tweets = 0
COUNT = 0
LAST_ID = ''

'''
class Employee(db.Model):
  name = db.StringProperty(required=True)
  role = db.StringProperty(required=True,
                           choices=set(["executive", "manager", "producer"]))
  hire_date = db.DateProperty()
  new_hire_training_completed = db.BooleanProperty(indexed=False)
  email = db.StringProperty()
'''


class DictProperty(db.Property):
  data_type = dict

  def get_value_for_datastore(self, model_instance):
    value = super(DictProperty, self).get_value_for_datastore(model_instance)
    return db.Blob(pickle.dumps(value))

  def make_value_from_datastore(self, value):
    if value is None:
      return dict()
    return pickle.loads(value)

  def default_value(self):
    if self.default is None:
      return dict()
    else:
      return super(DictProperty, self).default_value().copy()

  def validate(self, value):
    if not isinstance(value, dict):
      raise db.BadValueError('Property %s needs to be convertible '
                         'to a dict instance (%s) of class dict' % (self.name, value))
    return super(DictProperty, self).validate(value)

  def empty(self, value):
    return value is None


class Tweet(db.Model):
  #tweet = DictProperty()
  text = db.StringProperty(multiline=True)
  fetch_date = db.DateProperty()
  state = db.StringProperty()
  geocode = db.StringProperty()
  created_at = db.StringProperty()
  user_name = db.StringProperty()


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
  def addTweets(self, tweets, search, state='', geocode=None, max_id=None):
      print 'addTweets Called:'
      print 'search=%s' % search
      print 'state=%s' % state
      print 'geocode=%s' % geocode

      tweet_list = []

      i = 0
      global total_tweets
      for tweet in tweets:
          logging.info('tweets %s' % tweet)
          #tweet = json.loads(str(tweet))
          max_id = tweet.id_str
          t = Tweet(text=str(tweet.text.encode('ascii', 'ignore')), user_name=tweet.user.name,
                    created_at=str(tweet.created_at),
                    fetch_date=datetime.datetime.now().date(), 
                    state=state, geocode=geocode)
          t.put()
          i +=  1
          total_tweets = total_tweets + 1

      logging.info("Tweets added to Appengine!")

      self.searchTweets(search, state, geocode, int(max_id)-1)


  '''
  searchTweets function to make a search request to the twitter api using tweepy.
  @param: search String hashtag used for the search.
  @param: state String name of the state.
  @param: geocode String geocode of the location in a state.
  @param: max_id  String id of the last tweet fetched from the previous search request.
  '''
  def searchTweets(self, search, state, geocode=None, max_id=None):
      print 'searchTweets called:'
      print 'search tweets for %s' % search
      print 'state=%s' % state
      print 'geocode=%s' % geocode
      global COUNT
      COUNT += 1
      if COUNT < 100:
            tweets = api_request.user_timeline(q=search, count=100, max_id=max_id)
            if len(tweets) != 0:
              self.addTweets(tweets, search, state, geocode, max_id)
            else:
              print tweets
              print 'No tweets found!'
      else:
        print "Don't fetch more tweets"
        pass


  '''
  getGeoCodes function to get the geo codes with states and the radius of the area.
  @return: dict dict_object geo codes with state name and the radius.
  '''
  def getGeoCodes(self):
    logging.info('4. getGeoCodes called')
    csv_file = 'http://storage.googleapis.com/hashtagtraversal.appspot.com/us_cities.csv'
    csv_file = 'us_cities.csv'
    dict_object = {}
    with open(csv_file) as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        state = row[1]
        geocode = row[2] + ',-' + row[3] + ',20mi'
        dict_object[geocode] = state
    return dict_object


  '''
  geoTweets function to fetch tweets based on geo locations.
  @param: search String hashtag used for fetching tweets.
  '''
  def geoTweets(self, search):
      logging.info('3. geoTweets called')
      geocodes = self.getGeoCodes()
      for geocode, state in geocodes.iteritems():
        if state in ['CA', 'FL', 'IA', 'NY', 'WA']:
          logging.info('geo code is %s' % geocode)
          self.searchTweets(search, state, geocode, None)



def fetchTweets():
  logging.info('2. fetchTweets called')
  traversal = Traversal()
  #get Tweets.
  xsearch=['#USSenate', '#Senate',
            '#senate2014', 
            '#FlipTheSenate', '#Democrats', '#WHITEHOUSE2014', '#JoniErnst', '#ObamaResign', 
            '#Clinton2016', '#StopHillary', '#Obama']

  search = ['obama'] 

  for value in search:
    COUNT = 0
    logging.info('seach tweets for %s' % value)
    traversal.geoTweets(search=value)

  logging.info('total tweets %s' % total_tweets)


'''
def home(request):
	e = Employee(name="John",
             role="manager",
             email='pku@iastate.edu')
	e.hire_date = datetime.datetime.now().date()
	e.put()
	return http.HttpResponse('Hello World!')
'''


def getTweets(request):
  logging.info('1. getTweets called')
  fetchTweets()
  return http.HttpResponse('Tweets saved!')

