import asyncio
import csv
import os
import twikit
from datetime import datetime
from twikit import Client

# Configuration. On peut ajouter les pseudos à scrapper, et éventuellement créer plusierus groupes
GROUPS = {
    "Group1": [
        "user1", "user2", "user3"
    ],
    "Group2": [
        "user4", "user5", "user6"
    ],
    "Group3": [
        "user7", "user8", "user9"
    ]
}

# Paramètres à choisir
MAX_TWEETS_PER_USER = 1000
MIN_YEAR = 2020
DATA_FOLDER = 'data'

async def wait_for_rate_limit():
    """Gère la pause de 15 minutes en cas de code 429"""
    print("\nLimite X atteinte (429). Pause de 15 minutes.")
    for i in range(15, 0, -1):
        print(f"Reprise dans {i} minutes...", end="\r")
        await asyncio.sleep(60)
    print("\nReprise du scraping.")

async def scrape_user(client, username, group_name):
    """Scrape un utilisateur et extrait texte + images"""
    all_user_tweets = []
    cursor = None
    stop_user = False
    
    try:
        user = await client.get_user_by_screen_name(username)
        user_id = user.id
    except Exception as e:
        print(f"Impossible de trouver l'utilisateur @{username}: {e}")
        return []

    print(f"\nCible : @{username} (Groupe: {group_name})")

    while len(all_user_tweets) < MAX_TWEETS_PER_USER and not stop_user:
        try:
            tweets = await client.get_user_tweets(user_id, 'Tweets', count=20, cursor=cursor)
            
            if not tweets:
                print(f"Fin des tweets pour @{username}")
                break

            for tweet in tweets:
                # Conversion de la date
                tweet_date = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S %z %Y')
                
                if tweet_date.year < MIN_YEAR:
                    print(f"Année {tweet_date.year} atteinte pour @{username}. Passage au suivant.")
                    stop_user = True
                    break
                
                all_user_tweets.append({
                    'pseudo': username,
                    'date': tweet.created_at,
                    'text': tweet.text if tweet.text else "",
                    'retweets': tweet.retweet_count,
                    'likes': tweet.favorite_count,
                    'url': f"https://x.com/{username}/status/{tweet.id}"
                })

                if len(all_user_tweets) >= MAX_TWEETS_PER_USER:
                    break
            
            print(f"Progrès @{username}: {len(all_user_tweets)} tweets", end="\r")
            
            cursor = tweets.next_cursor
            if not cursor: break
            
            await asyncio.sleep(4) # Pause de 4 secondes pour éviter le ban entre chaque scrape.

        except twikit.errors.TooManyRequests:
            await wait_for_rate_limit()
            continue 
        except Exception as e:
            print(f"Erreur sur une page de @{username}: {e}")
            break

    return all_user_tweets

async def main():
    client = Client('en-US')
    try:
        client.load_cookies(path='cookies.json')
        print("Authentification réussie.")
    except:
        print("Erreur: cookies.json introuvable ou invalide.")
        return

    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    for group_name, users in GROUPS.items():
        group_data = []
        csv_path = os.path.join(DATA_FOLDER, f"{group_name}.csv")
        
        print(f"\n--- DÉBUT DU SCRAPING : {group_name.upper()} ---")
        
        for username in users:
            tweets = await scrape_user(client, username, group_name)
            if tweets:
                group_data.extend(tweets)
            
                # Sauvegarde immédiate après chaque utilisateur
                keys = group_data[0].keys()
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    dict_writer = csv.DictWriter(f, fieldnames=keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(group_data)

        print(f"\nFichier enregistré pour le groupe {group_name} : {csv_path}")

    print("\nTerminé.")

if __name__ == "__main__":
    asyncio.run(main())