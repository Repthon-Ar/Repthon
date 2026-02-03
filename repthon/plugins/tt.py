import json
import os
import random
import string
import requests

try:
    import mimetypes
except ModuleNotFoundError:
    os.system("pip3 install mimetypes")
    import mimetypes

import user_agent
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions
from telethon.utils import get_display_name
from urlextract import URLExtract

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv
from . import BOTLOG, BOTLOG_CHATID, zq_lo, reply_id

# دالة الرفع المحسنة: ترجع المسار فقط وتتجنب الأخطاء
def safe_upload_file(file_path):
    try:
        # تحديد نوع الملف تلقائياً
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, mime_type)}
            response = requests.post('https://graph.org/upload', files=files, headers=headers)
        
        if response.status_code == 200:
            res_json = response.json()
            if isinstance(res_json, list) and len(res_json) > 0:
                return res_json[0]['src']
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Upload Error: {e}")
        return None

def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

LOGS = logging.getLogger(__name__)
plugin_category = "utils"
extractor = URLExtract()
telegraph = Telegraph()

try:
    telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
except Exception:
    pass

@zq_lo.rep_cmd(
    pattern=r"(t(ele)?g(raph)?) ?(m|t|media|text)(?:\s|$)([\s\S]*)",
    command=("telegraph", plugin_category),
)
async def _(event):
    "To get telegraph link."
    catevent = await edit_or_reply(event, "`جاري المعالجة... ⏳`")
    
    if not event.reply_to_msg_id:
        return await catevent.edit("`يرجى الرد على رسالة أولاً.`")

    start = datetime.now()
    r_message = await event.get_reply_message()
    input_str = (event.pattern_match.group(4)).strip()

    if input_str in ["media", "m"]:
        if not r_message.media:
            return await catevent.edit("`الرسالة لا تحتوي على ميديا!`")
            
        file_path = await event.client.download_media(r_message, Config.TEMP_DIR)
        
        if file_path.endswith((".webp")):
            resize_image(file_path)
            
        try:
            media_path = safe_upload_file(file_path)
            if not media_path:
                return await catevent.edit("`فشل الرفع.. ربما السيرفر مضغوط أو الملف غير مدعوم.`")
            end = datetime.now()
            ms = (end - start).seconds
            
            await catevent.edit(
                f"**تم الرفع بنجاح ✅**\n\n**الرابط : **[اضغط هنا](https://graph.org{media_path})\n"
                f"**الوقت : **`{ms} ثانية.`",
                link_preview=True,
            )
        except Exception as exc:
            await catevent.edit(f"**خطأ :**\n`{exc}`")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    elif input_str in ["text", "t"]:
        page_content = r_message.message.replace("\n", "<br>")
        try:
            response = telegraph.create_page("Repthon Post", html_content=page_content)
            cat = f"https://graph.org/{response['path']}"
            await catevent.edit(f"**الرابط :** [اضغط هنا]({cat})", link_preview=True)
        except Exception as e:
            await catevent.edit(f"**خطأ :** `{e}`")
