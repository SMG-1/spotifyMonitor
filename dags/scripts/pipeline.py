import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yaml
import pandas as pd
import psycopg2

asdf


class Authenticator:
    def __init__(self, scope) -> None:

        with open("credentials/credentials.yml", "r") as stream:
            try:
                content = yaml.safe_load(stream)
            except yaml.YAMLError as exception:
                print(exception)

        self.client_id = content['SPOTIFY_CLIENT_ID']
        self.client_secret = content['SPOTIFY_SECRET_ID']
        self.redirect_uri='http://localhost:8888/callback/',
        self.scope = scope

    def create_spotify_object(self):

        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope))

def top_tracks_to_df(limit=30, time_range='medium_range') -> pd.DataFrame:

    auth = Authenticator('user-library-read')
    sp = auth.create_spotify_object()

    res = sp.current_user_top_tracks(limit=limit, time_range=time_range)['items']

    # create nested df
    df = pd.DataFrame(res)
    df_album = pd.json_normalize(pd.json_normalize(df['artists'])[0])

    df_album.rename(columns={'name': 'artistName'}, inplace=True)
    df = pd.concat([df, df_album[['artistName']]], axis=1)

    # keep relevant columns
    df = df[['name', 'popularity', 'artistName']]

    df.to_csv('top_tracks_airflow.csv')

    return df

def audio_features_to_df(track_list: pd.DataFrame) -> pd.DataFrame:

    auth = Authenticator('user-library-read')
    sp = auth.create_spotify_object()

    df = pd.DataFrame(sp.audio_features(track_list))

    cols_to_keep = [
        'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
        'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
        'id', 'duration_ms'
        ]

    return df[cols_to_keep]

def top_artists_to_df(limit=30, time_range='medium_range') -> pd.DataFrame:

    auth = Authenticator('user-library-read')
    sp = auth.create_spotify_object()

    df = pd.DataFrame(
        sp.current_user_top_artists(limit=limit, time_range=time_range)['items']
    )

    df_top_artists = df_top_artists.explode('genres')

    df.to_csv('top_artists_airflow.csv')

    return df

if __name__ == '__main__':

    auth=Authenticator('user-library-read')
    sp = auth.create_spotify_object()

    print(type(sp))

    print('Hello World!')

    conn = psycopg2.connect("dbname=postgres user=postgres password=Sebas-20221psql port=5432")
    conn.autocommit = True

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    # cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

    cur.execute(open("./warehouse_db_setup/create_wh.sql", "r").read())

    # cur.execute("SELECT * FROM test;")
    # print(cur.fetchall())

    # with conn.cursor() as cur:
    #     cur.execute("SELECT * FROM my_data")

    #     print(cur.fetchall())