from utils.config import *
from modules.chatgpt_summary.chatgpt_stats import run_chatgpt_stats
from modules.format_converters.heic_to_jpg import *
from modules.format_converters.mov_to_mp4 import convert_mov_to_mp4
from modules.song_hub.spotify_library import fetch_spotify_library
from modules.song_hub.yt_to_mp3 import download_single_video, download_video_list, download_playlist
from modules.song_hub.spotify_downloader_ytdlp import ytdlp_song_downloader
from modules.song_hub.spotify_downloader_selenium import selenium_song_downloader

# run_chatgpt_stats()
# convert_images(SINGLE_IMAGE_FILE_PATH)
# convert_mov_to_mp4(VIDEO_FOLDER_PATH,VIDEO_OUTPUT_PATH)
# fetch_spotify_library()
# download_single_video(VIDEO_URL, VIDEO_SAVE_PATH)
# download_video_list(VIDEO_LIST, VIDEO_SAVE_PATH)
# download_playlist(PLAYLIST_URL, PLAYLIST_SAVE_PATH)
# ytdlp_song_downloader()
selenium_song_downloader()
