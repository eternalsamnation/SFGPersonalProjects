import os
import time
import pandas as pd
import logging
import re

from mutagen.easyid3 import EasyID3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    filename='song_download_log.txt',   # log file path
    level=logging.WARNING,            # minimum level to log (DEBUG < INFO < WARNING < ERROR < CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # log message format
    filemode='a'                   # 'w' to overwrite, 'a' to append
)

DOWNLOAD_LINK = "https://cnvmp3.com/v51"
DOWNLOAD_DIR = 'C:/Users/sfind/Music/iTunes/iTunes Media/Spotify_Downloads'
SONG_DF = pd.read_csv('./modules/song_hub/SpotifyData/spotify_artists.csv')

firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

prefs = {
    "download.default_directory": os.path.abspath(DOWNLOAD_DIR),
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

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

def wait_for_latest_mp3(download_dir, timeout=60):
    """
    Waits for a new MP3 file to finish downloading and returns its path.
    """
    end_time = time.time() + timeout
    seen_files = set(os.listdir(download_dir))

    while time.time() < end_time:
        current_files = set(os.listdir(download_dir))
        new_files = current_files - seen_files

        mp3s = [f for f in new_files if f.lower().endswith(".mp3")]

        if mp3s:
            mp3_path = os.path.join(download_dir, mp3s[0])

            # Wait for Chrome to finish writing
            if not mp3_path.endswith(".crdownload"):
                return mp3_path

        time.sleep(1)

    raise TimeoutError("MP3 download timed out")

def tag_mp3(file_path, title, artist):
    audio = EasyID3(file_path)
    audio["title"] = title
    audio["artist"] = artist
    audio.save()

def selenium_song_downloader(wait_between: int = 5):
    for _, row in SONG_DF.iterrows():
        try:
            # Set Up Download Link
            song_title = row['Name']
            song_title_search = re.sub(r'[^a-zA-Z0-9]', '', song_title)
            artist_name = row['Artist(s)']

            search_query = f"{song_title_search} {artist_name} audio"
            file_path = f"{DOWNLOAD_DIR}/{song_title}-{artist_name}.mp3"

            if os.path.isfile(file_path):
                print(f'{file_path} exists, skipping download.')
                continue

            yt_download_link = fetch_link(search_query)

            # Set Up Selenium
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            wait = WebDriverWait(driver, 30)
            driver.get(DOWNLOAD_LINK)

            # Wait for input box
            input_box = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
            )

            input_box.clear()
            input_box.send_keys(yt_download_link)
            time.sleep(2)
            input_box.send_keys(Keys.ENTER)

            download_button = wait.until(EC.presence_of_element_located((
                By.XPATH,"//main//label//input[contains(@value, 'Download') or contains(., 'Download') or @type='button' or @type='submit']"
            )))
            wait.until(EC.element_to_be_clickable(download_button))
            driver.execute_script("arguments[0].click();", download_button)

            mp3_path = wait_for_latest_mp3(DOWNLOAD_DIR)

            tag_mp3(
                file_path=mp3_path,
                title=song_title,
                artist=artist_name
            )

            print(f"Tagged: {song_title} — {artist_name}")
            time.sleep(wait_between)

        except Exception as e:
            print(f"Error processing {song_title} by {artist_name} with link {yt_download_link}: {e}")
            logging.warning(f"Error processing {song_title} by {artist_name} with link {yt_download_link}\n")
            continue

        finally:
            driver.quit()

def selenium_song_downloader_jr(wait_between: int = 5):
    extra_links = [
        'https://www.youtube.com/watch?v=R5HSXZdcUJ0&list=RDR5HSXZdcUJ0', # Paris
        'https://www.youtube.com/watch?v=v0JzrFTvhgs&list=RDv0JzrFTvhgs', # Heartbeat Gambino
        'https://www.youtube.com/watch?v=COz9lDCFHjw&list=RDCOz9lDCFHjw', # Passionfruit Drake
        'https://www.youtube.com/watch?v=QKYkZnxZ3ZA&list=RDQKYkZnxZ3ZA', # Hold On We're Going Home Drake
        'https://www.youtube.com/watch?v=qblMC5qD3tQ&list=RDqblMC5qD3tQ', # Nina Cried Power
        'https://www.youtube.com/watch?v=OAxR_2uFO5I&list=RDOAxR_2uFO5I', # Lord Huron Harvest Moon
        'https://www.youtube.com/watch?v=6id53KyAycI&list=RD6id53KyAycI', # The Plural of Moose is Moose
        'https://www.youtube.com/watch?v=l3qi3E40aWE&list=RDl3qi3E40aWE', # For Once In My Live Stevie
    ]

    for yt_download_link in extra_links:
        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            wait = WebDriverWait(driver, 30)
            driver.get(DOWNLOAD_LINK)

            # Wait for input box
            input_box = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
            )

            input_box.clear()
            input_box.send_keys(yt_download_link)
            time.sleep(2)
            input_box.send_keys(Keys.ENTER)

            download_button = wait.until(EC.presence_of_element_located((
                By.XPATH,"//main//label//input[contains(@value, 'Download') or contains(., 'Download') or @type='button' or @type='submit']"
            )))
            wait.until(EC.element_to_be_clickable(download_button))
            driver.execute_script("arguments[0].click();", download_button)
            time.sleep(wait_between)

        except Exception as e:
            print(f"Error processing link {yt_download_link}: {e}")
            continue

        finally:
            driver.quit()
