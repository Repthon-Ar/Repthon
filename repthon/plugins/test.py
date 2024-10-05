import asyncio
import youtube_dl
from telethon import TelegramClient, events
from repthon import zq_lo
from ..Config import Config

plugin_category = "البوت"


async def download_and_send(video_url):
    try:
        # إعداد خيارات التحميل
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': 'audio.%(ext)s',  # اسم الملف الناتج
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        # تحميل الفيديو
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # إرسال الملف عبر تيليجرام
        await client.send_file('me', 'audio.mp3')
        
        
    except Exception as e:
        await client.send_message('me', f"حدث خطأ: {e}")
    

@zq_lo.rep_cmd(
    pattern="test(?:\\s|$)([\\s\\S]*)",
    command=("test", plugin_category),
    info={
        "header": "تحميـل الاغـاني مـن يوتيوب .. فيسبوك .. انستا .. الـخ عـبر الرابـط",
        "مثــال": ["{tr}تحميل صوت بالــرد ع رابــط", "{tr}تحميل صوت + رابــط"],
    },
)
async def handler(event):
    search_query = event.pattern_match.group(1)
    await download_and_send(search_query)
    await event.reply('تم تحميل وإرسال الملف!') 
