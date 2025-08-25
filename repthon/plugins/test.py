import os
import glob
import random
import asyncio
from pytube import YouTube
from telethon import events
from telethon.errors import ChatAdminRequiredError, FloodWaitError, UserNotParticipantError
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
            
            # احصل على ملف الكوكيز العشوائي
            cookies_file = get_cookies_file()
            
            # ابحث عن الفيديو على يوتيوب باستخدام الكوكيز
            yt = YouTube(f'https://www.youtube.com/results?search_query={query}', cookies=cookies_file)
            
            # اختر أول فيديو في نتائج البحث
            video = yt.streams.filter(only_audio=True).first()
            if video is None:
                await event.reply('لم يتم العثور على فيديوهات مناسبة.')
                return
            
            # قم بتحميل الفيديو
            await event.reply('جاري تحميل الموسيقى...')
            video.download(output_path='downloads', filename='music.mp4')
            
            # أرسل الملف إلى Telegram
            await zq_lo.send_file(event.chat_id, 'downloads/music.mp4')
            await event.reply('تم تحميل وإرسال الموسيقى بنجاح!')
        
        except FileNotFoundError as e:
            await event.reply(f'خطأ: {str(e)}')
        except errors.FloodWaitError as e:
            await event.reply(f'خطأ: يجب الانتظار {e.seconds} ثانية قبل المحاولة مرة أخرى.')
            await asyncio.sleep(e.seconds)  # انتظر لمدة الوقت المحدد
        except errors.ChatAdminRequiredError as e:
            await event.reply('خطأ: تحتاج إلى أذونات المسؤول في هذه الدردشة.')
        except errors.UserNotParticipantError as e:
            await event.reply('خطأ: يجب أن تكون عضوًا في القناة لاستخدام هذه الميزة.')
        except Exception as e:
            await event.reply(f'حدث خطأ أثناء البحث أو التحميل: {str(e)}')
