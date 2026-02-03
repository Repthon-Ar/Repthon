import json
import os
import random
import string
import requests

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



def safe_upload_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                'https://graph.org/upload',
                files={'file': ('file', f, 'image/jpeg')}
            )
        
        if response.status_code != 200:
            return f"Error: Server returned {response.status_code}"
            
        return response.json()
    except Exception as e:
        return str(e)


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

LOGS = logging.getLogger(__name__)
plugin_category = "utils"
extractor = URLExtract()
telegraph = Telegraph()

try:
    r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
    auth_url = r["auth_url"]
except Exception:
    auth_url = "https://telegra.ph"


@zq_lo.rep_cmd(
    pattern=r"(t(ele)?g(raph)?) ?(m|t|media|text)(?:\s|$)([\s\S]*)",
    command=("telegraph", plugin_category),
    info={
        "header": "To get telegraph link.",
        "description": "يرفع النصوص والوسائط (صور/فيديو) إلى تلغراف.",
        "usage": "{tr}tgm (بالرد على ميديا) أو {tr}tgt (بالرد على نص)",
    },
)
async def _(event):
    "To get telegraph link."
    catevent = await edit_or_reply(event, "`جاري المعالجة........`")
    
    optional_title = event.pattern_match.group(5)
    if not event.reply_to_msg_id:
        return await catevent.edit("`يرجى الرد على رسالة للحصول على رابط تلغراف.`")

    start = datetime.now()
    r_message = await event.get_reply_message()
    input_str = (event.pattern_match.group(4)).strip()

    if input_str in ["media", "m"]:
        if not r_message.media:
            return await catevent.edit("`الرسالة التي رددت عليها لا تحتوي على ميديا!`")
            
        downloaded_file_name = await event.client.download_media(r_message, Config.TEMP_DIR)
        await catevent.edit(f"`تم التحميل.. جاري الرفع الآن..`")
        if downloaded_file_name.endswith((".webp")):
            resize_image(downloaded_file_name)
            
        try:
            media_urls = safe_upload_file(downloaded_file_name)
            end = datetime.now()
            ms = (end - start).seconds
            
            await catevent.edit(
                f"**تم الرفع بنجاح ✅**\n\n**الرابط : **[اضغط هنا](https://graph.org{media_urls[0]})\n"
                f"**الوقت المستغرق : **`{ms} ثانية.`",
                link_preview=True,
            )
        except Exception as exc:
            await catevent.edit(f"**خطأ أثناء الرفع : **\n`{exc}`")
        finally:
            if os.path.exists(downloaded_file_name):
                os.remove(downloaded_file_name)

    elif input_str in ["text", "t"]:
        user_object = await event.client.get_entity(r_message.sender_id)
        title_of_page = get_display_name(user_object)
        
        if optional_title:
            title_of_page = optional_title
            
        page_content = r_message.message
        if r_message.media:
            if page_content != "":
                title_of_page = page_content
            downloaded_file_name = await event.client.download_media(r_message, Config.TEMP_DIR)
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            for m in m_list:
                page_content += m.decode("UTF-8") + "\n"
            os.remove(downloaded_file_name)
            
        page_content = page_content.replace("\n", "<br>")
        try:
            response = telegraph.create_page(title_of_page, html_content=page_content)
        except Exception:
            title_of_page = "".join(random.choice(string.ascii_letters) for _ in range(16))
            response = telegraph.create_page(title_of_page, html_content=page_content)
            
        end = datetime.now()
        ms = (end - start).seconds
        cat = f"https://graph.org/{response['path']}"
        await catevent.edit(
            f"**تم إنشاء الصفحة بنجاح ✅**\n\n**الرابط : ** [اضغط هنا]({cat})\n"
            f"**الوقت المستغرق : **`{ms} ثانية.`",
            link_preview=True,
        )
