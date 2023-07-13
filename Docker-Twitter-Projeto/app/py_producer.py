import json
import os.path
from time import sleep
from kafka.producer import KafkaProducer
import tweepy

consumer_key = 'YOLEGmQb0GyK5h32Whqq7ueUD'
consumer_secret = '434qzo0Nr7tepVYzxnMxEoFcNTVZcZK0KOddSz5woJtu0YXwie'
access_token = '1390889232529567744-ja5tpzG84GQYQnCHqaZT8wn8H6gnZB'
access_token_secret = '341nObKQXei6PDKIyiWSRL8qtcApItQO7ouo03bDqb7r5'
processed_tweets_file = "processed_tweets_file"

def task():
    kafka_server = "localhost:9091"
    topic = "producer-twitter"
    producer = KafkaProducer(bootstrap_servers=kafka_server, value_serializer=lambda v: json.dumps(v).encode("utf-8"))

    def auth():
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

    def load_processed_tweets():
        if not os.path.isfile(processed_tweets_file):
            return set()
        with open(processed_tweets_file, "r") as file:
            return set(file.read().splitlines())

    def save_processed_tweets(processed_tweets):
        with open(processed_tweets_file, "w") as file:
            file.write("\n".join(processed_tweets))

    api = auth()
    processed_tweets = load_processed_tweets()
    max_id = None

    while True:
        search_query = "'itau''boleto' -filter:retweets AND -filter:replies AND -filter:links"
        tweets = api.search_tweets(q=search_query, count=1, tweet_mode='extended', max_id=max_id)

        for tweet in tweets:
            tweet_id = tweet.id_str

            if tweet_id not in processed_tweets:
                tweet_dict = tweet._json
                print(tweets)
                producer.send(topic, value=tweet_dict)
                producer.flush()
                processed_tweets.add(tweet_id)
                print(f"Tweet with ID {tweet_id} sent to Kafka.")

        save_processed_tweets(processed_tweets)

        # Atualiza o max_id para obter tweets mais recentes na próxima iteração
        if tweets:
            max_id = tweets[-1].id - 1

        sleep(30)

task()
