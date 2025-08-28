import os
import glob
import random
import asyncio
import yt_dlp
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
from telethon import events
from repthon import zq_lo
from ..Config import Config

plugin_category = "الادوات"

def get_cookies_file():
    folder_path = f"{os.getcwd()}/rbaqir"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    return cookie_txt_file
    

@zq_lo.on(events.NewMessage(pattern='.بحث3 (.+)'))
async def download_music(event):
    query = event.pattern_match.group(1)
    await event.reply(f"جاري البحث عن: {query}...")

    # البحث عن الموسيقى
    results = YoutubeSearch(query, max_results=1).to_dict()
    
    if not results:
        await event.reply("لم يتم العثور على أي نتائج.")
        return

    video_url = f"https://www.youtube.com{results[0]['url_suffix']}"
    await event.reply(f"جاري تحميل: {results[0]['title']}...")

    # تحميل الموسيقى باستخدام yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'cookiefile': get_cookies_file(),

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # إرسال الملف إلى المحادثة
    file_name = f"{results[0]['title']}.mp3"
    if os.path.exists(file_name):
        await zq_lo.send_file(event.chat_id, file_name)
        os.remove(file_name)  # حذف الملف بعد الإرسال
    else:
        await event.reply("حدث خطأ أثناء تحميل الموسيقى.")
