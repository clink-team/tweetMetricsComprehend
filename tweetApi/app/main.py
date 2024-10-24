import json
import os.path
import os
from time import sleep
from kafka.producer import KafkaProducer
import tweepy
import sys
import urllib.request
import json
import requests

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACESS_TOKEN")
access_token_secret = os.environ.get("ACESS_TOKEN_SECRET")
processed_tweets_file = "processed_tweets_file"

def task():
    kafka_server = os.environ.get("KAFKA_URL")
    print(f"kafka_server:::::>>  {kafka_server}")
    topic = "producer-twitter"
    max_retries = 10
    retry_delay = 5
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
            print("Iniciando a conexão com o kafka")
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

        search_query = "'casimiro' -filter:retweets AND -filter:replies AND -filter:links"
        print(f"Iniciando busca dos tweets query: {search_query}")
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


# task()


client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
processed_naver_search_results_file = "processed_naver_search_results_file"

def task_naver_search(client_id, client_secret, query, display=10, start=1, sort='sim'):
    kafka_server = os.environ.get("KAFKA_URL")
    print(f"kafka_server:::::>>  {kafka_server}")
    topic = "producer-naver-search"
    try_once = False # FIXME for testing only
    max_retries = 10
    retry_delay = 5
    retry_count = 0

    def load_processed_naver_search_results():
        if not os.path.isfile(processed_naver_search_results_file):
            return set()
        with open(processed_naver_search_results_file, "r") as file:
            return set(file.read().splitlines())

    def save_processed_naver_search_results(processed_naver_search_results):
        with open(processed_naver_search_results_file, "w") as file:
            file.write("\n".join(processed_naver_search_results))

    processed_naver_search_results = load_processed_naver_search_results()

    while True:
        try:
            print("Starting the connection with Kafka")
            producer = KafkaProducer(bootstrap_servers=kafka_server, value_serializer=lambda v: json.dumps(v).encode("utf-8"))
            break  # If the connection is successful, exit the retry loop
        except Exception as e:
            if retry_count >= max_retries:
                print("Exceeded the maximum number of connection attempts. Leaving...")
                raise e
            print(f"Error connecting to Kafka broker. Trying again at {retry_delay} seconds...")
            sleep(retry_delay)
            retry_count += 1

    # while True:

    #     encText = urllib.parse.quote(query)
    #     url = "https://openapi.naver.com/v1/search/cafearticle?query=" + encText + \
    #             "&display=" + str(display) + "&start=" + str(start) + "&sort=" + sort
    #     print(f"Starting naver search query: {url}")

    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id",client_id)
    #     request.add_header("X-Naver-Client-Secret",client_secret)
    #     response = urllib.request.urlopen(request)
    #     rescode = response.getcode()
    #     if(rescode==200):
    #         response_body = response.read()
    #         response_json = json.loads(response_body)

    #         items = response_json['items']
    #         for item in items:
    #             link = item['link']
                
    #             if link not in processed_naver_search_results:
    #                 print(item)
    #                 producer.send(topic, value=item['description'])
    #                 producer.flush()
    #                 processed_naver_search_results.add(link)
    #                 print(f"Search result with link {link} sent to Kafka.")

    #         save_processed_naver_search_results(processed_naver_search_results)

    #         sleep(30)
            
    #         if try_once:
    #             break
    #     else:
    #         print("Error Code:" + rescode)
    while True:
        base_url = "https://openapi.naver.com/v1/search/cafearticle"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        params = {
            "query": query,
            "display": display,
            "start": start,
            "sort": sort
        }

        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            items = data['items']
            for item in items:
                link = item['link']
                
                if link not in processed_naver_search_results:
                    print(item)
                    producer.send(topic, value=item['title'])
                    # producer.send(topic, value=item['description'])
                    producer.flush()
                    processed_naver_search_results.add(link)
                    print(f"Search result with link {link} sent to Kafka.")

            save_processed_naver_search_results(processed_naver_search_results)

            sleep(30)
            
            if try_once:
                break
        else:
            print(f'Error: {response.status_code}')

query = '전기차' # FIXME for testing only
display=100
start=1
sort='sim'

task_naver_search(client_id, client_secret, query, display, start, sort)
