#Show top 10 retweeted orginial tweets i.e. retweeted=false in descending order.
MATCH (t:Tweet) where t.retweet_count>0 AND t.retweeted = false return t.retweet_count AS count,t.text as Tweet order by t.retweet_count desc limit 10;


# Show top 10 hash tags that travel the most number of states.
MATCH (c:State)<-[FROM]-(t:Tweet)<-[TAGGED]-(h:Hashtag) return (count(distinct(c.name))) AS Longest_Path,h.name AS Hashtag order by Longest_Path desc limit 10;

# Show the longest path of states that "football" hashtag travels within a given time period.
MATCH (c:State)<-[FROM]-(t:Tweet)<-[TAGGED]-(h:Hashtag) where h.name = "football" and t.created_at < 1428987471269 and t.created_at > 1351798658000 return (count(distinct(c.name))) AS Longest_Path;

# Show contents of the most retweeted tweet for a hashtag "football" and the state "NY" where it was posted originally.
match (c:State)<-[FROM]-(t:Tweet)<-[:TAGGED]-(h:Hashtag)  where c.name = "NY" and h.name = "football" and t.retweeted = false  return t.text AS Tweet,c.name AS Location,t.retweet_count AS Retweet_Count order by t.retweet_count desc limit 1;

# Show users and their location, which have used hashtag "football" and also used hash tag B in their tweets.

MATCH (h1:Hashtag)-[TAGGED]->(t:Tweet)<-[:TAGGED]-(h2:Hashtag) where h1.name = "football" with t MATCH (h3:Hashtag)-[TAGGED]->(t)<-[POSTED]-(u:User) WHERE h3.name = "tyrants" return u.name AS Name,u.location AS Location;;

#  Show top 10 platforms used for tweeting of a "football" hashtag.
MATCH (h:Hashtag)-[:TAGGED] -> (t:Tweet)-[:USING] -> (s:Source) where h.name = "football"  RETURN s as Source_Name, count(t) as Tweet_Count ORDER BY Tweet_Count DESC LIMIT 10;

# Show the top 10 tweeting user for "football" hashtag.

MATCH (h:Hashtag)-[TAGGED]->(t)<-[POSTED]-(u:User) WHERE h.name = "football" and t.retweeted = false return count(t) AS Count,u.name AS User order by Count desc Limit 10;


# Show the maximum count of tweet using "football" hashtag, by a user who has maximum followers.

MATCH (u:User)-[POSTED]->(t:Tweet)<-[TAGGED]-(h:Hashtag) WITH u ORDER BY u.followers DESC LIMIT 1 MATCH (u)-[POSTED]->(t:Tweet)<-[TAGGED]-(h:Hashtag) where h.name = "football" return count(t) as Count order by Count desc limit 1;

# Show the verified users for "football" hashtag.

match (h:Hashtag)-[TAGGED]->(t:Tweet)<-[:POSTED]-(u:User) where h.name='football' and u.verified=true return count(u);






