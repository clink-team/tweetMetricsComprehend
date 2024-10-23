import tweepy

# Authenticate with Twitter OAuth 1.0a User Context
auth = tweepy.OAuth1UserHandler(
# API / Consumer Key here
"maj0SoKRqYqtA08BdSQzTXojj",
# API / Consumer Secret here
"ZpzBIeQyHwFc4ozE480nFEg64jueQPISPFMtige8EFfjFZevJc",
# Access Token here
"147812703-pHf2ZM1pML4CvYiMhHmhZmVjYy8N7etf3HVIfCvG",
# Access Token Secret here
"NnEDGFZKtS6u0SdDM2zERxtklRuKmBm925OTX38ciZgOs"
)
api = tweepy.API(auth)

# Get recent tweets from your home timeline
tweets = api.home_timeline(count=5)
for tweet in tweets:
    print(tweet.text,'\n')