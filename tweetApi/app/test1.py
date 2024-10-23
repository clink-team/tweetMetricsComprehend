import tweepy

consumer_key = 'maj0SoKRqYqtA08BdSQzTXojj'
consumer_secret = 'ZpzBIeQyHwFc4ozE480nFEg64jueQPISPFMtige8EFfjFZevJc'
access_token = '147812703-pHf2ZM1pML4CvYiMhHmhZmVjYy8N7etf3HVIfCvG'
access_token_secret = 'NnEDGFZKtS6u0SdDM2zERxtklRuKmBm925OTX38ciZgOs'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
max_id = None

# search_query = "'casimiro' -filter:retweets AND -filter:replies AND -filter:links"
# print(f"Iniciando busca dos tweets query: {search_query}")
# tweets = api.search_tweets(q=search_query, count=1, tweet_mode='extended', max_id=max_id)
# for tweet in tweets.data:
#     print(tweet.text)
status = api.user_timeline(screen_name = 'SamsungNewsroom', count=1)[0]
print(status.text)