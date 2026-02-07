import yt_dlp
from utils.config import *

def download_single_video(video_url, save_path):
    ydl_opts = {
        'outtmpl': save_path + '/%(title)s.%(ext)s',
        'ffmpeg_location': FFMPEG_PATH,
        'cookiesfrombrowser': ('firefox',),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_url)

def download_video_list(video_url_list, save_path):
    for video_url in video_url_list:
        try:
            download_single_video(video_url, save_path)
        except Exception as e:
            print(f"Error downloading {video_url}: {e}")

def download_playlist(playlist_url, save_path):
    ydl_opts = {
        'outtmpl': save_path + '/%(title)s.%(ext)s',
        'ffmpeg_location': FFMPEG_PATH,
        'cookiesfrombrowser': ('firefox',),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }],
        'yes_playlist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(playlist_url)
