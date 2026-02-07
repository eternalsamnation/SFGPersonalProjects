import pandas as pd
import spotipy
import spotipy.util as util

OUTPUT_PATH = 'SpotifyData/SFG_Spotify_Library.csv'
LIM_OUTPUT_PATH = 'SpotifyData/spotify_artists.csv'

CLIENT_ID = '1c644704e0a640d28ec466dc5f239516'
CLIENT_SECRET = '11a19e4b9e4c4e92b0deab421ef24065'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'

SCOPE = 'user-library-read user-top-read user-read-recently-played'
USERNAME = 'sfindlengolden'

def fetch_spotify_library():
    token = util.prompt_for_user_token(
        USERNAME,
        SCOPE,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI
    )
    sp = spotipy.Spotify(auth=token)

    response = {}
    paginating_count = 0
    if token:
        while paginating_count<1100:
            results = sp.current_user_saved_tracks(offset=paginating_count, limit=50)
            response[paginating_count] = results
            paginating_count+=50

    song_names = []
    album_names = []
    song_lengths = []
    song_popularities = []
    song_artists = []

    df_dump = pd.DataFrame(response)
    song_info = df_dump.loc['items']

    for song_subset in song_info:
        for song in song_subset:
            song_name = song['track']['name']
            album_name = song['track']['album']['name']
            song_length = song['track']['duration_ms'] / 1000
            length_m, length_s = divmod(song_length, 60)
            song_popularity = song['track']['popularity']
            song_artist = []
            for artist in song['track']['artists']:
                song_artist.append(artist['name'])

            song_names.append(song_name)
            album_names.append(album_name)
            if int(length_s) < 10:
                song_lengths.append(str(int(length_m)) + ':0' + str(int(length_s)))
            else:
                song_lengths.append(str(int(length_m)) + ':' + str(int(length_s)))
            song_popularities.append(song_popularity)
            song_artists.append(" ".join(song_artist))

    song_data = {
        'Name': song_names,
        'Artist(s)': song_artists,
        'Album': album_names,
        'Length': song_lengths,
        'Popularity': song_popularities
    }

    spotify_df = pd.DataFrame(song_data)
    spotify_df_lim = spotify_df.iloc[:,:2]

    spotify_df.to_csv(OUTPUT_PATH, index=False)
    spotify_df_lim.to_csv(LIM_OUTPUT_PATH, index=False)
    print('Spotify library data saved')
    return
