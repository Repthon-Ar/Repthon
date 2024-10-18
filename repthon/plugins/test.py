import yt_dlp
import os
from telethon import TelegramClient, events
from yt_dlp import YoutubeDL
from repthon import zq_lo
from ..Config import Config

plugin_category = "البوت"


@zq_lo.on(events.NewMessage(pattern='.بحث3 (.*)'))
async def get_song(event):
    song_name = event.pattern_match.group(1)
    await event.reply(f"جاري البحث عن الأغنية: {song_name}...")

    # إعداد خيارات yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'nocookies': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
            title = info['entries'][0]['title']
            filename = f"{title}.mp3"

            await event.reply(f"تم العثور على الأغنية: {title}nجاري إرسال الملف...")

            # إرسال الملف إلى تيليجرام
            await client.send_file(event.chat_id, filename)

            # حذف الملف بعد الإرسال
            os.remove(filename)
        except Exception as e:
            await event.reply(f"حدث خطأ أثناء البحث عن الأغنية: {e}")
