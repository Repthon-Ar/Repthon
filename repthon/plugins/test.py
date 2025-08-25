import os
import glob
import random
import asyncio
from youtube_search import YoutubeSearch
from youtube_dl import YoutubeDL
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
                print(f"رابط الفيديو: {video_url}")  # طباعة رابط الفيديو
                
                # إعداد خيارات التحميل مع ملفات تعريف الارتباط
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'extractaudio': True,  # استخراج الصوت فقط
                    'audioformat': 'mp3',  # تنسيق الصوت
                    'outtmpl': 'downloads/%(title)s.%(ext)s',  # مسار حفظ الملف
                    'cookiefile': 'get_cookies_file()',  # مسار ملف تعريف الارتباط
                }
                
                # تحميل الفيديو باستخدام youtube-dl
                await event.reply('جاري تحميل الموسيقى...')
                os.makedirs('downloads', exist_ok=True)  # تأكد من وجود مجلد التحميل
                
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                
                # احصل على اسم الملف المحمل
                filename = f'downloads/{results[0]["title"]}.mp3'
                
                # أرسل الملف إلى Telegram
                await zq_lo.send_file(event.chat_id, filename)
                await event.reply('تم تحميل وإرسال الموسيقى بنجاح!')
            else:
                await event.reply("لم يتم العثور على نتائج.")

        except Exception as e:
            await event.reply(f'حدث خطأ أثناء البحث أو التحميل: {str(e)}')
