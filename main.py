
import tweepy
from tweepy import Forbidden, OAuthHandler
from tweepy.errors import TooManyRequests, Forbidden
import configparser
import re
import sqlite3
from sqlite3 import Error
from langdetect import detect
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

def create_connection():
    """ Créer une connexion à la base de données SQLite """
    db_path = "data/base.db"  # Chemin relatif à partir de l'emplacement du script Python
    try:
        conn = sqlite3.connect(db_path)
    except Error as e:
        print(f"Erreur lors de la connexion à la base de données: {e}")
    return conn

def create_table(conn):
    """ Créer une table dans la base de données SQLite """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweets (
                id INTEGER PRIMARY KEY,
                tweet_text TEXT NOT NULL,
                language TEXT,
                sentiment_score REAL,
                potential_cyberbullying BOOLEAN
            );
        """)
        conn.commit()
    except Error as e:
        print(f"Erreur lors de la création de la table: {e}")

def twitter_api_setup(config_file):
    """ Configurer l'API Twitter """
    config = configparser.ConfigParser()
    config.read(config_file)

    consumer_key = config['TwitterAPI']['CONSUMER_KEY']
    consumer_secret = config['TwitterAPI']['CONSUMER_SECRET']
    access_token = config['TwitterAPI']['ACCESS_TOKEN']
    access_token_secret = config['TwitterAPI']['ACCESS_TOKEN_SECRET']

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def clean_tweet(tweet):
    """ Nettoyer le texte du tweet """
    tweet = re.sub(r'@\w+', '', tweet)
    tweet = re.sub(r'#\w+', '', tweet)
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub(r'\n', ' ', tweet)
    return tweet.strip()

def initialize_sentiment_analyzers():
    """ Initialiser les analyseurs de sentiment """
    vader_analyzer = SentimentIntensityAnalyzer()
    camembert_analyzer = pipeline('sentiment-analysis', model='tblard/tf-allocine')
    return vader_analyzer, camembert_analyzer

def get_sentiment(text, lang, vader_analyzer, camembert_analyzer):
    """ Obtenir le score de sentiment en fonction de la langue """
    if lang == 'en':
        return vader_analyzer.polarity_scores(text)['compound']
    elif lang == 'fr':
        result = camembert_analyzer(text)[0]
        return result['score'] if result['label'] == 'LABEL_1' else -result['score']
    else:
        return None

def insert_tweet_data(conn, tweet_data):
    """ Insérer les données du tweet dans la base de données """
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tweets(tweet_text, language, sentiment_score, potential_cyberbullying)
            VALUES(?,?,?,?)
        """, tweet_data)

def analyze_and_save_tweets(username, max_tweets, api, vader_analyzer, camembert_analyzer):
    """ Analyser et enregistrer les tweets dans la base de données. """
    conn = create_connection()
    if conn is None:
        print("Connexion à la base de données échouée.")
        return

    try:
        with conn:
            for tweet in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended').items(max_tweets):
                cleaned_tweet = clean_tweet(tweet.full_text)
                tweet_lang = detect(cleaned_tweet)
                sentiment_score = get_sentiment(cleaned_tweet, tweet_lang, vader_analyzer, camembert_analyzer)
                potential_cyberbullying = sentiment_score is not None and sentiment_score < -0.5
                tweet_data = (cleaned_tweet, tweet_lang, sentiment_score, potential_cyberbullying)
                insert_tweet_data(conn, tweet_data)
                if potential_cyberbullying:
                    print(f"Potential cyberbullying case detected: {cleaned_tweet}")
    except Forbidden:
        print("Accès refusé à l'API Twitter. Vérifie les autorisations de ton application.")
    except TooManyRequests:
        print("Tu as dépassé la limite de taux de l'API Twitter. Essaie de nouveau après un certain temps.")
    except tweepy.TweepError as e:
        print(f"Erreur Tweepy: {e}")
    finally:
        conn.close()

def main():
    """ Fonction principale """
    config_file = 'config.ini'
    username = '@Al3xkiss93190'
    max_tweets = 10
    api = twitter_api_setup(config_file)
    vader_analyzer, camembert_analyzer = initialize_sentiment_analyzers()
    analyze_and_save_tweets(username, max_tweets, api, vader_analyzer, camembert_analyzer)

if __name__ == "__main__":
    main()
