import tweepy as tw
import pandas as pd
from os.path import join
from tqdm import tqdm

api_key = ''
api_key_secret = ''
access_token = ''
access_token_secret = ''
auth = tw.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


search_words = "#Bitcoin OR #bitcoin"
end_date = "2021-11-12"

max_id = None
for i in tqdm(range(25)):
    tweets = tw.Cursor(api.search_tweets,
                  q=search_words,
                  lang="en",
                  until=end_date, max_id=max_id
                  ).items(5000)
    l = []
    for tweet in tweets:
        l.append(tweet)
    df = pd.DataFrame({'user_name': [], 'id': [], 'user_location': [], 'user_description': [], 'user_created': [],
                      'user_followers': [], 'user_friends': [], 'user_favourites': [], 'date': [],
                       'text': [], 'source': []})
    for tweet in l:
        df = df.append(pd.DataFrame({'user_name': tweet.user.name,
                                     'id': tweet.id,
                                   'user_location': tweet.user.location,
                                   'user_description': tweet.user.description,
                                   'user_created': tweet.user.created_at,
                                   'user_followers': tweet.user.followers_count,
                                   'user_friends': tweet.user.friends_count,
                                   'user_favourites': tweet.user.favourites_count,
                                   'date': tweet.created_at,
                                   'text': tweet.text,
                                   'source': tweet.source}, index=[len(df)]))
    max_id = tweet.id - 1
    if len(df) > 0:
        df.to_csv(f'D:/tweet/data/11_12/bitcoin_{i}.csv')
