# Twitter Sentiment Analysis and Cyberbullying Detection

## Description
Ce script Python utilise l'API Twitter pour récupérer les tweets d'un utilisateur spécifié, les nettoie, détecte la langue, effectue une analyse de sentiment et évalue le potentiel de cyberintimidation. Les résultats sont stockés dans une base de données SQLite locale.

## Features
- Connexion à l'API Twitter et récupération des tweets
- Nettoyage et prétraitement du texte des tweets
- Détection de la langue du tweet
- Analyse de sentiment des tweets en anglais avec VADER et en français avec le modèle CamemBERT
- Détection des tweets potentiellement cyberintimidants
- Stockage des données dans une base de données SQLite

## Installation
Pour utiliser ce script, vous devez installer les dépendances suivantes:

```bash
pip install tweepy configparser re sqlite3 langdetect transformers vaderSentiment
```

## Configuration
Avant d'exécuter le script, vous devez configurer vos clés d'API Twitter dans un fichier `config.ini` comme suit:

```ini
[TwitterAPI]
CONSUMER_KEY = VotreConsumerKey
CONSUMER_SECRET = VotreConsumerSecret
ACCESS_TOKEN = VotreAccessToken
ACCESS_TOKEN_SECRET = VotreAccessTokenSecret
```

## Usage
Pour exécuter le script, lancez simplement le fichier principal:

```bash
python main.py
```

## Database Schema
La base de données SQLite contient la table suivante:

```
tweets (
    id INTEGER PRIMARY KEY,
    tweet_text TEXT NOT NULL,
    language TEXT,
    sentiment_score REAL,
    potential_cyberbullying BOOLEAN
)
```

## License
Incluez des informations sur la licence ici, si applicable.

## Contributions
Les contributions à ce projet sont les bienvenues. Veuillez suivre les bonnes pratiques pour les contributions et les pull requests.

## Contact
Si vous avez des questions ou des commentaires, veuillez contacter [WebcressonTech] à [alexis@webcresson.com].
