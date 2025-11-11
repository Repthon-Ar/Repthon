import user_agent
import random
import glob
import os
import asyncio
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch 
from repthon import zq_lo
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from ..Config import Config

plugin_category = "البوت"

def get_cookies_file():
    """Get a random cookies file from the specified folder."""
    folder_path = f"{os.getcwd()}/rbaqir"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    return random.choice(txt_files)

@zq_lo.rep_cmd(pattern="بحث3(?: |$)(.*)")
async def get_song(event):
    song_name = event.pattern_match.group(1)
    message = await event.reply(f"جاري البحث عن الأغنية: **{song_name}**...")

    try:
        videosSearch = VideosSearch(song_name, limit = 1)
        results = videosSearch.result()
        
        if not results['result']:
            await message.edit("عذرًا، لم يتم العثور على أي نتائج لهذا البحث.")
            return
            
        video_url = results['result'][0]['link']
        title = results['result'][0]['title']
        uploader = results['result'][0]['channel']['name']
        
        ydl_opts = {
            "format": "bestaudio/best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "320"},
                {"key": "FFmpegMetadata"},
            ],
            "outtmpl": f"{title}.%(ext)s",
            "logtostderr": False,
            "quiet": True,
            "no_warnings": True,
            "cookiefile": get_cookies_file(),
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            
            filename = ydl.prepare_filename(info).replace(info.get('ext'), 'mp3')
            thumbnail_filename = ydl.prepare_filename(info).replace(info.get('ext'), 'jpg')

            await message.edit(f"تم العثور على الأغنية: **{title}**، جاري إرسال الملف...")

            if os.path.exists(thumbnail_filename):
                audio = MP3(filename, ID3=ID3)
                with open(thumbnail_filename, 'rb') as img_file:
                    audio.tags.add(
                        APIC(
                            encoding=3,
                            mime='image/jpeg',
                            type=3,
                            desc='Cover',
                            data=img_file.read()
                        )
                    )
                audio.save()

            caption = f"بحثك: **{title}**\nالمغني أو الناشر: **{uploader}**\nتم التحميل بواسطة @Repthon"
            await zq_lo.send_file(event.chat_id, filename, caption=caption)

            os.remove(filename)
            if os.path.exists(thumbnail_filename):
                os.remove(thumbnail_filename)

    except Exception as e:
        # R
        print(f"حدث خطأ أثناء التحميل: {e}")
        await message.edit("عذرًا، حدثت مشكلة أثناء البحث أو التحميل. يرجى المحاولة مرة أخرى.")
