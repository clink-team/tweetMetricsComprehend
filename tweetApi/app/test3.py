import tweepy

# Authenticate with OAuth 2.0 Bearer Token (App only)
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAM8kwgEAAAAARtmzFQeA2DW7OzB7P67iJ6xZZcY%3DLphWUuKQ7X4q5gD9qZdUyJc5ynPgCqPCkQWG1NtYFXMVT4p4Pg')

# Pull tweets from twitter
query = '#elonmusk -is:retweet lang:en'
tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=10)
# Get tweets that contain the hashtag #TypeKeywordHere
# -is:retweet means I don't want retweets
# lang:en is asking for the tweets to be in english
# print pulled tweets
for tweet in tweets.data:
    print('\n**Tweet Text**\n',tweet.text)