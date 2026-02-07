import pandas as pd
import spotipy
import spotipy.util as util
import streamlit as st

st.set_page_config(page_title="SFG Spotify Stats Dashboard", layout="wide")
st.title("SFG Spotify Stats Dashboard")

CLIENT_ID = '1c644704e0a640d28ec466dc5f239516'
CLIENT_SECRET = '11a19e4b9e4c4e92b0deab421ef24065'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'

SCOPE = 'user-library-read user-top-read user-read-recently-played'
USERNAME = 'sfindlengolden'

token = util.prompt_for_user_token(
    USERNAME,
    SCOPE,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI
)
sp = spotipy.Spotify(auth=token)

time_ranges = ["short_term", "medium_term", "long_term"]
top_tables = {}
for tr in time_ranges:
    top_tracks = sp.current_user_top_tracks(limit=10, time_range=tr)
    tracks_list = []
    for i, track in enumerate(top_tracks["items"], start=1):
        song_dict = {
            'Rank': i, 
            'Song':track['name'],
            'Artist':track['artists'][0]['name'],
        }
        tracks_list.append(song_dict)
    top_tracks_df = pd.DataFrame(tracks_list)
    top_tables[f'{tr}_tracks'] = top_tracks_df

    top_artists = sp.current_user_top_artists(limit=10, time_range=tr)
    artist_list = []
    for i, artist in enumerate(top_artists["items"], start=1):
        art_dict = {
            'Rank': i, 
            'Artist':artist['name']
        }
        artist_list.append(art_dict)
    top_artists_df = pd.DataFrame(artist_list)
    top_tables[f'{tr}_artists'] = top_artists_df

displayed_dfs = top_tables.values()
# table_title_list = list(top_tables.keys())
table_title_list = [
    'Top Songs: Short-Term',
    'Top Artists: Short-Term',
    'Top Songs: Medium-Term',
    'Top Artists: Medium-Term',
    'Top Songs: Long-Term',
    'Top Artists: Long-Term'
]
cols = st.columns(2)

for i, df in enumerate(displayed_dfs):
    col_ind = i%2
    with cols[col_ind]:
        if not df.empty:
            st.subheader(table_title_list[i])
            def highlight_row(row):
                return f'<tr class="">' + "".join([f"<td>{row[c]}</td>" for c in df.columns]) + "</tr>"
            html_table = (
                "<table><tr>" +
                "".join(f"<th>{col}</th>" for col in df.columns) +
                "</tr>" +
                "".join(df.apply(highlight_row, axis=1)) +
                "</table>"
            )
            st.markdown(html_table, unsafe_allow_html=True)
