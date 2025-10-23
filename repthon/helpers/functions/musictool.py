import contextlib
import os
import re
import glob
import random
import yt_dlp
from pathlib import Path

import lyricsgenius
import requests
from bs4 import BeautifulSoup

from ...Config import Config
from ...core.managers import edit_or_reply
from ...core.logger import logging
from ...helpers.google_tools import chromeDriver
from ..utils.utils import runcmd
from .utube import name_dl, song_dl, video_dl

LOGS = logging.getLogger(__name__)
GENIUS = Config.GENIUS_API_TOKEN

def get_cookies_file():
    folder_path = f"{os.getcwd()}/rbaqir"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    return cookie_txt_file

class LyricGenius:
    def __init__(self):
        if GENIUS:
            self.genius = lyricsgenius.Genius(GENIUS)

    def songs(self, title):
        return self.genius.search_songs(title)["hits"]

    def song(self, title, artist=None):
        song_info = None
        with contextlib.suppress(AttributeError, IndexError):
            if not artist:
                song_info = self.songs(title)[0]["result"]
            else:
                for song in self.songs(title):
                    if artist in song["result"]["primary_artist"]["name"]:
                        song_info = song["result"]
                        break
                if not song_info:
                    for song in self.songs(f"{title} by {artist}"):
                        if artist in song["result"]["primary_artist"]["name"]:
                            song_info = song["result"]
                            break
        return song_info

    def lyrics(self, title, artist=None):
        lyrics = ""
        song_info = self.song(title, artist)
        title = song_info["title"]
        link = song_info["song_art_image_url"] or None
        if not artist:
            artist = song_info["primary_artist"]["name"]
        try:
            song = self.genius.search_song(title, artist)
            lyrics = song.lyrics.split(f"{title} Lyrics")
            if len(lyrics) > 1:
                lyrics = lyrics[1].replace("[", "\n\n[").replace("\n\n\n[", "\n\n[").replace("\n\n\n", "\n\n")
        except Exception:
            # try to scrap 1st
            url = f"https://www.musixmatch.com/lyrics/{artist.replace(' ', '-')}/{title.replace(' ', '-')}"
            soup, _ = chromeDriver.get_html(url)
            soup = BeautifulSoup(soup, "html.parser")
            lyrics_containers = soup.find_all(class_="lyrics__content__ok")
            for container in lyrics_containers:
                lyrics += container.get_text().strip()

            # if private data then show 30%
            if not lyrics:
                base_url = "https://api.musixmatch.com/ws/1.1/"
                endpoint = base_url + f"matcher.lyrics.get?format=json&q_track={title}&q_artist={artist}&apikey=bf9bfaeccae52f5a4366bcdb2a6b0c4e"
                response = requests.get(endpoint)
                data = response.json()
                lyrics = data["message"]["body"]["lyrics"]["lyrics_body"]
        return link, lyrics


LyricsGen = LyricGenius()


async def song_download(url, event, quality="128k", video=False, title=True, cookies_path=None):
    media_type = "المقطع الصوتي"
    media_ext = ["mp3", "mp4a"]

    if cookies_path is None:
        cookies_path = get_cookies_file()

    name_cmd_for_filename = f'yt-dlp --get-filename --skip-download "{url}" --cookies "{cookies_path}"'

    name_stdout, name_stderr, _, _ = await runcmd(name_cmd_for_filename)

    if name_stderr:
        LOGS.error(f"Error getting filename: {name_stderr}")
        return await edit_or_reply(event, f"**خطـأ في الحصول على اسم الملف :: {name_stderr}**")

    filename_only = os.path.basename(name_stdout)
    base_name, _ = os.path.splitext(filename_only)
    safe_base_name = re.sub(r'[\\/*?:"<>|]', "", base_name)
    download_dir = os.path.dirname(name_stdout) if os.path.dirname(name_stdout) else '.'
    if not download_dir.startswith('.'):
        download_dir = '.'

    actual_media_file_path = None
    for ext in media_ext:
        potential_file = Path(download_dir) / f"{safe_base_name}.{ext}"
        if potential_file.exists():
            actual_media_file_path = potential_file
            break

    if not actual_media_file_path:
        LOGS.error(f"Media file not found. Tried extensions: {media_ext} in dir: {download_dir} with base name: {safe_base_name}")
        return await edit_or_reply(event, f"**- عـذراً .. لا يمكنني العثور على {media_type} ⁉️ (الملف غير موجود)**")

    media_file = actual_media_file_path

    if video:
        media_type = "الفيديو"
        media_ext = ["mp4", "mkv"]
        
        media_cmd = video_dl.format(video_link=url, cookies_path=cookies_path) 
    else:
        media_cmd = song_dl.format(QUALITY=quality, video_link=url, cookies_path=cookies_path)

    stdout_dl, stderr_dl, _, _ = await runcmd(media_cmd)
    if stderr_dl:
        LOGS.error(f"Error during download command: {stderr_dl}")
        return await edit_or_reply(event, f"**خطـأ أثناء تنزيل {media_type} :: {stderr_dl}**")

    await edit_or_reply(event, f"**- جـارِ تحميـل {media_type} ▬▭...**")

    media_thumb = Path(f"{download_dir}/{safe_base_name}.jpg")
    if not media_thumb.exists():
        media_thumb = Path(f"{download_dir}/{safe_base_name}.webp")

    if not media_thumb.exists():
        media_thumb = None

    if title:
        media_title = actual_media_file_path.name.replace("_", "|") 
        return actual_media_file_path, media_thumb, media_title
    return actual_media_file_path, media_thumb
