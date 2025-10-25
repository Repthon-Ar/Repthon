import os
import re
import glob
import random
from pathlib import Path

import lyricsgenius
import requests
from bs4 import BeautifulSoup

from ...Config import Config
from ...core.managers import edit_or_reply
from ...helpers.google_tools import chromeDriver
from ..utils.utils import runcmd
from .utube import name_dl, song_dl, video_dl

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
    media_exts = ["mp3", "mp4a"]
    
    if cookies_path is None:
        try:
            cookies_path = get_cookies_file()
        except FileNotFoundError:
            # إذا لم يتم العثور على ملف الكوكيز، تابع بدونه
            cookies_path = None 

    media_cmd = song_dl.format(QUALITY=quality, video_link=url, cookies_path=cookies_path or "")
    name_cmd = name_dl.format(video_link=url, cookies_path=cookies_path or "")
    
    if video:
        media_type = "الفيديو"
        media_exts = ["mp4", "mkv"]
        media_cmd = video_dl.format(video_link=url, cookies_path=cookies_path or "")

    media_name = None
    
    try:
        # 1. الحصول على اسم الملف المتوقع
        result = await runcmd(name_cmd)
        media_name, stderr = result[:2]
        
        if stderr:
            await edit_or_reply(event, f"**خطـأ في الحصول على الاسم :: {stderr}**")
            return None, None, None # العودة بـ 3 قيم لتجنب TypeError

        media_name_base = os.path.splitext(media_name.strip())[0].strip()
        
        await edit_or_reply(event, f"**- جـارِ تحميـل {media_type} ▬▭...**")
        
        # 2. تنزيل الملف فعلياً
        result = await runcmd(media_cmd)
        _, stderr_dl = result[:2]

        if stderr_dl and "ERROR: unable to download" in stderr_dl:
            await edit_or_reply(event, f"**خطـأ أثناء التنزيل :: {stderr_dl}**")
            return None, None, None # العودة بـ 3 قيم لتجنب TypeError
            
    except Exception as e:
        await edit_or_reply(event, f"**خطأ غير متوقع أثناء التنزيل :: {e}**")
        return None, None, None # العودة بـ 3 قيم لتجنب TypeError

    # 3. التحقق من وجود الملفات بعد التنزيل
    media_file = None
    for ext in media_ext:
        temp_file = Path(f"{media_name_base}.{ext}")
        if os.path.exists(temp_file):
            media_file = temp_file
            break

    if not media_file:
        await edit_or_reply(event, f"**- عـذراً .. لا يمكنني العثور على {media_type} ({media_name_base}) بعد التنزيل ⁉️**")
        return None, None, None # العودة بـ 3 قيم لتجنب TypeError
    
    # 4. تحديد صورة مصغرة (Thumb)
    media_thumb = None
    for ext in ["jpg", "webp"]:
        temp_thumb = Path(f"{media_name_base}.{ext}")
        if os.path.exists(temp_thumb):
            media_thumb = temp_thumb
            break

    # 5. إرجاع النتيجة
    if title:
        media_title = os.path.basename(media_name_base).replace("./temp/", "").replace("_", "|")
        return media_file, media_thumb, media_title
        
    return media_file, media_thumb, None
