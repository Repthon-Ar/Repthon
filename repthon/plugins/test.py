import os
import glob
import random
import asyncio
from pytube import YouTube
from telethon import events
from youtube_search import YoutubeSearch
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

@zq_lo.on(events.NewMessage)
async def handler(event):
    if event.message.text.startswith('.بحث3'):
        try:
            query = event.message.text.split(' ', 1)[1]  # احصل على استعلام البحث
            await event.reply('جاري البحث عن الموسيقى...')
            
            # ابحث عن الفيديو على يوتيوب باستخدام youtube-search-python
            results = YoutubeSearch(query, max_results=1).to_dict()
            
            if results:
                video_url = f"https://www.youtube.com{results[0]['url_suffix']}"
                print(f"تم العثور على الفيديو: {results[0]['title']}")
                
                # تحميل الفيديو باستخدام pytube
                yt = YouTube(video_url)  # لا نمرر الكوكيز هنا
                
                video = yt.streams.filter(only_audio=True).first()
                
                if video is None:
                    await event.reply('لم يتم العثور على فيديوهات مناسبة.')
                    return
                
                # قم بتحميل الفيديو
                await event.reply('جاري تحميل الموسيقى...')
                output_path = 'downloads'
                os.makedirs(output_path, exist_ok=True)  # تأكد من وجود مجلد التحميل
                video.download(output_path=output_path, filename='music.mp4')
                
                # أرسل الملف إلى Telegram
                await zq_lo.send_file(event.chat_id, os.path.join(output_path, 'music.mp4'))
                await event.reply('تم تحميل وإرسال الموسيقى بنجاح!')
            else:
                await event.reply("لم يتم العثور على نتائج.")

        except Exception as e:
            await event.reply(f'حدث خطأ أثناء البحث أو التحميل: {str(e)}')
