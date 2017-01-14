'''
Twitter Hashtag traversal.

@author Prashant Kumar

@version: 1.0 2015

Copyright 2015

'''
import time
import csv
import datetime
import sys
import json
import csv
import random


from itertools import cycle


#get neo4j set up
#note, you have to have neo4j running and on the default port
from py2neo import Graph

# set up authentication parameters
#neo4j.authenticate("neo4j.cs.iastate.edu:9002", "root", "nQ88pFdFWqP")
#graph_db = neo4j.GraphDatabaseService("https://neo4j.cs.iastate.edu:9002/db/data/")
graph_db = Graph("http://localhost:7474/db/data/")


# Add uniqueness constraints.
graph_db.cypher.execute("CREATE CONSTRAINT ON (t:Tweet) ASSERT t.id IS UNIQUE;")
graph_db.cypher.execute("CREATE CONSTRAINT ON (u:User) ASSERT u.screen_name IS UNIQUE;")
graph_db.cypher.execute("CREATE CONSTRAINT ON (h:Hashtag) ASSERT h.name IS UNIQUE;")
graph_db.cypher.execute("CREATE CONSTRAINT ON (l:Url) ASSERT l.expanded_url IS UNIQUE;")
graph_db.cypher.execute("CREATE CONSTRAINT ON (c:State) ASSERT c.name IS UNIQUE;")

GEOCOUNT = 0
total_tweets = 0
COUNT = 0
LAST_ID = ''


class Traversal:
    def __init__(self):
      pass

    '''
    addTweets function to add data to our graph database.
    @param: tweets json tweets fetched from the twitter.
    @param: user String hashtag used for the search.
    '''
    def addTweets(self):
        f = open('somefilename.csv', 'rU')
        csv_f = csv.reader(f)
        for row in csv_f:
		  for h in row[12].split(','):
		    print h
          data = {
            'text': row[0],
            'created_at': row[1],
            'state': row[2],
            'category': row[3],
            'sub_category': row[4],
            'tweet_id': row[5],
            'retweeted_status': row[6],
            'retweet_count': row[7],
            'user_screen_name': row[8],
            'user_name': row[9],
            'followers_count': row[10],
            'friends_count': row[11],
            'hashtags': row[12].split(','),
            'urls': row[13].split(','),
            'user_mentioned': row[14].split(','),
            'year': row[15],
            'day': row[16],
            'month': row[17],
            'monthId': row[18],
            'dayId': row[19]
          }

          # Pass dict to Cypher and build query.
          query = """ 
			  UNWIND {hashtags} AS hashtagFromCollection
              UNWIND {user_mentioned} AS user_mentionedFromCollection
			  UNWIND {urls} AS urlFromCollection

              MERGE (tweet:Tweet {id:{tweet_id}})
              SET tweet.text = {text},
                  tweet.created_at = {created_at},
                  tweet.retweet_count = {retweet_count},
                  tweet.day = {day},
                  tweet.year = {year},
                  tweet.month = {month},
                  tweet.retweeted = {retweeted_status}
              MERGE (user:User {screen_name:{user_screen_name}})
              SET user.location = {state},
                  user.name = {user_name},
                  user.followers = {followers_count},
                  user.following = {friends_count},
                  user.category = {category},
                  user.sub_category = {sub_category}
              MERGE (user)-[:POSTED]->(tweet)
              MERGE (state: State {name: {state}})
              MERGE (user)-[:FROM]->(state)
              MERGE (c:Century{century: 21})
              MERGE (y:Year{year:{year}})
              MERGE (c)-[:HAS_YEAR]->(y)
              MERGE (m:Month{id:{monthId}})
              SET m.month={month}
              MERGE (d:Day{id:{dayId}})
              SET d.day = {day}
              MERGE (y)-[:HAS_MONTH]->(m)
              MERGE (m)-[:HAS_DAY]->(d)
			  
              MERGE (tag:Hashtag {name:hashtagFromCollection})
              MERGE (tag)-[:TAGGED]->(tweet)
              MERGE (d)-[:HAS_TAG]->(tag)
              MERGE (user)-[:USED]->(tag)
              MERGE (state)-[:APPEARED]->(tag)
              
              MERGE (mentioned:User {screen_name: user_mentionedFromCollection})
              SET mentioned.name = user_mentionedFromCollection
              MERGE (tweet)-[:MENTIONED]-(mentioned)
              
              MERGE (url: Url {url: urlFromCollection})
              MERGE (tweet)-[:URL_USED]-(url) 
              """

          # Send Cypher query.
          graph_db.cypher.execute_one(query, parameters=None, **data)
        print("Tweets added to graph!\n")


def main():
  traversal = Traversal()
  traversal.addTweets()


if __name__ == '__main__':
  main()



