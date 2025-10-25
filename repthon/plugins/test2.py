import io
import os
import re
import glob
import random

from telethon import types
from validators.url import url

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv, yt_search
from ..helpers.tools import media_type
from ..helpers.utils import reply_id
from . import zq_lo, song_download

plugin_category = "البحث"
LOGS = logging.getLogger(__name__)

def get_cookies_file():
    folder_path = f"{os.getcwd()}/rbaqir"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        # إذا لم يتم العثور على ملفات، يُفضل العودة بـ None أو مسار افتراضي لتجنب تعطل الـ plugin
        LOGS.warning("No .txt files found in rbaqir folder. Proceeding without cookies.")
        return None
    cookie_txt_file = random.choice(txt_files)
    return cookie_txt_file

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
SONG_SEARCH_STRING = "<code>wi8..! I am finding your song....</code>"
SONG_NOT_FOUND = "<code>Sorry !I am unable to find any song like that</code>"
SONG_SENDING_STRING = "<code>yeah..! i found something wi8..🥰...</code>"
SONG_FILE_ERROR = "<code>⚠️ عذراً، فشل في إيجاد/تحميل ملف الصوت. قد يكون الرابط غير صالح أو حدث خطأ في عملية التحويل.</code>"
# =========================================================== #


@zq_lo.rep_cmd(
    pattern=r"بحث4(320)?(?:\s|$)([\s\S]*)",
    command=("song", plugin_category),
    info={
        "header": "To get songs from youtube.",
        "description": "Basically this command searches youtube and send the first video as audio file.",
        "flags": {
            "320": "if you use song320 then you get 320k quality else 128k quality",
        },
        "usage": "{tr}song <song name>",
        "examples": "{tr}song memories song",
    },
)
async def song(event):
    "To search songs"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "What I am Supposed to find ")
    
    catevent = await edit_or_reply(event, SONG_SEARCH_STRING)
    video_link = await yt_search(str(query))
    
    if not url(video_link):
        return await catevent.edit(f"Sorry!. I can't find any related video/audio for {query}")
        
    cmd = event.pattern_match.group(1) if event.pattern_match.group(1) else None
    q = "320k" if cmd == "320" else "128k"
    
    cookies_path = get_cookies_file()
    
    # 1. تحميل الملف (باستخدام الدالة المحدثة)
    song_file, catthumb, title = await song_download(video_link, catevent, quality=q, cookies_path=cookies_path)
    
    # قائمة للملفات التي تحتاج تنظيف في النهاية
    files_to_clean = []
    if song_file:
        files_to_clean.append(song_file)
    if catthumb:
        files_to_clean.append(catthumb)
        
    try:
        # 2. التحقق من وجود الملف (السطر الذي كان يسبب الخطأ خارجياً)
        if not song_file or not os.path.exists(song_file):
            return await catevent.edit(SONG_FILE_ERROR) # هذا الـ return هو موضع المشكلة في الكود القديم

        await catevent.edit(SONG_SENDING_STRING)
        
        # 3. إرسال الملف
        await event.client.send_file(
            event.chat_id,
            song_file,
            force_document=False,
            caption=f"**Title:** {title}",
            thumb=catthumb if catthumb and os.path.exists(catthumb) else None, 
            supports_streaming=True,
            reply_to=reply_to_id,
        )
        
        await catevent.delete()
        
    except Exception as e:
        # 4. معالجة أي خطأ قد يحدث أثناء الإرسال
        LOGS.error(e)
        if catevent.is_edit:
            await catevent.edit(f"حدث خطأ أثناء إرسال الملف: \n`{e}`")
        
    finally:
        # 5. ضمان تنظيف الملفات المؤقتة
        for file_path in files_to_clean:
            try:
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as cleanup_e:
                LOGS.error(f"Failed to remove temporary file {file_path}: {cleanup_e}")
