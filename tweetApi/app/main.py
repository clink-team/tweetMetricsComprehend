import json
import os.path
import os
from time import sleep
from kafka.producer import KafkaProducer
import tweepy

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACESS_TOKEN")
access_token_secret = os.environ.get("ACESS_TOKEN_SECRET")
processed_tweets_file = "processed_tweets_file"

def task():
    kafka_server = os.environ.get("KAFKA_URL")
    print(f"kafka_server:::::>>  {kafka_server}")
    topic = "producer-twitter"
    max_retries = 10  # Defina o número máximo de tentativas de conexão
    retry_delay = 5  # Defina o tempo de espera entre as tentativas de conexão
    retry_count = 0

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
        try:
            producer = KafkaProducer(bootstrap_servers=kafka_server, value_serializer=lambda v: json.dumps(v).encode("utf-8"))
            break  # Se a conexão for bem-sucedida, saia do loop de retry
        except Exception as e:
            if retry_count >= max_retries:
                print("Excedeu o número máximo de tentativas de conexão. Saindo...")
                raise e
            print(f"Erro ao conectar ao broker Kafka. Tentando novamente em {retry_delay} segundos...")
            sleep(retry_delay)
            retry_count += 1

    while True:
        search_query = "'itau''boleto' -filter:retweets AND -filter:replies AND -filter:links"
        tweets = api.search_tweets(q=search_query, count=1, tweet_mode='extended', max_id=max_id)

        for tweet in tweets:
            tweet_id = tweet.id_str

            if tweet_id not in processed_tweets:
                tweet_dict = tweet._json
                print(tweets)
                producer.send(topic, value=tweet_dict['full_text'])
                producer.flush()
                processed_tweets.add(tweet_id)
                print(f"Tweet with ID {tweet_id} sent to Kafka.")

        save_processed_tweets(processed_tweets)

        # Atualiza o max_id para obter tweets mais recentes na próxima iteração
        if tweets:
            max_id = tweets[-1].id - 1

        sleep(30)

if __name__ == '__main__':
    task()
