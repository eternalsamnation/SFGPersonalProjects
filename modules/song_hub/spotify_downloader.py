import time
import pandas as pd
import re
import os
import yt_dlp

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from mutagen.easyid3 import EasyID3
from config import *

OUTPUT_PATH = 'C:/Users/sfind/Music/iTunes/iTunes Media/Spotify_Downloads'

firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")

def fetch_link(search_query):
    driver = webdriver.Firefox(options=firefox_options)

    try:
        driver.get("https://www.youtube.com")

        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(3)  # wait for results

        first_video = driver.find_element(
            By.XPATH,
            '(//ytd-video-renderer//a[@id="thumbnail"])[1]'
        )

        video_url = first_video.get_attribute("href")

        if video_url:
            playlist_index = video_url.find("&")
            return video_url[:playlist_index] if playlist_index != -1 else video_url

        return None

    except Exception as e:
        print(f"Error fetching link for query '{search_query}': {e}")
        return None

    finally:
        driver.quit()

def song_downloader():
    df = pd.read_csv('./SpotifyData/spotify_artists.csv')

    for _, row in df.iterrows():
        song_title = row['Name']
        song_title_search = re.sub(r'[^a-zA-Z0-9]', '', song_title)
        artist_name = row['Artist(s)']

        search_query = f"{song_title_search} {artist_name} audio"
        file_path = f"{OUTPUT_PATH}/{song_title}-{artist_name}.mp3"

        if os.path.isfile(file_path):
            print(f'{file_path} exists, skipping download.')
            continue

        yt_download_link = fetch_link(search_query)
        print(f'Link for {song_title} by {artist_name}: {yt_download_link}')
        with open('song_links.csv', 'a') as log_file:
            log_file.write(f"{song_title},{artist_name},{yt_download_link}\n")
        if not yt_download_link:
            print("No link found, skipping.")
            continue
        # yt_download_link = f"ytsearch1:{search_query}"

        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': f"{OUTPUT_PATH}/{song_title}-{artist_name}.%(ext)s",
            'ffmpeg_location': FFMPEG_PATH,
            'cookiesfrombrowser': ('firefox',),
            'js_runtime': 'node',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                }
            },
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0',
            }],
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([yt_download_link])

            audio = EasyID3(file_path)
            audio['title'] = song_title
            audio['artist'] = artist_name
            audio.save()

            print(f"Metadata for {file_path} updated successfully")

        except Exception as e:
            pass
            # print(f"Error downloading {song_title} by {artist_name}: {e}")
            # with open('missed_songs.txt', 'a') as log_file:
                # log_file.write(f"{song_title} - {artist_name}\n")
