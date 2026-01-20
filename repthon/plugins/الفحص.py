# بس ابن الزنة وابن الحرام الي يغير حقوق
# ابن الكحبة الي يغير حقوقنا - @E_7_V
# خصيمة يوم القيامة تبقى ذمة غير مسامح بها يوم الدين

import random
import re
import time
import psutil
import os
from datetime import datetime
from platform import python_version

import requests
from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)

from . import StartTime, zq_lo, repversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import repalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus

plugin_category = "العروض"
STATS = gvarstatus("R_STATS") or "فحص"

RANDOM_MEDIA = [
    "https://graph.org/file/f4c01d51562507a36c07e.mp4",
    "https://graph.org/file/0b1e5679e24e735f870c5.mp4",
    "https://graph.org/file/cafa0e8a1320891a65ae2.mp4",
    "https://graph.org/file/b442b635cecca399dea39.mp4",
    "https://graph.org/file/534d48ffb4b1e22e4ee39.mp4",
    "https://graph.org/file/ec26c9d0a5532f17f85ac.mp4",
    "https://graph.org/file/5201ed73785e5a928c853.mp4",
    "https://graph.org/file/764e2427fafbe4aec2251.mp4",
    "https://graph.org/file/9501d29c6cccd86b22686.mp4",
    "https://graph.org/file/e30ff8013dd3f61f0735e.mp4",
    "https://graph.org/file/3b9dc775779767faeb774.mp4",
    "https://graph.org/file/1ee6a852367700b272a51.mp4",
    "https://graph.org/file/53809263bafc29ef6adee.mp4",
    "https://graph.org/file/4c6325935cb7e5494c77e.mp4",
    "https://graph.org/file/a6a25238f38a351da1e33.mp4",
    "https://graph.org/file/7aa8ce05fbcabdfd32090.mp4",
    "https://graph.org/file/e765806fb50294079a58c.mp4"
]

def get_platform():
    if "HEROKU_APP_NAME" in os.environ or "HEROKU_API_KEY" in os.environ:
        return "𝙷𝚎𝚛𝚘𝚔𝚞"
    elif "RENDER" in os.environ:
        return "𝚁𝚎𝚗𝚍𝚎𝚛"
    elif "KOYEB_SERVICE_NAME" in os.environ:
        return "𝙺𝚘𝚢𝚎𝚋"
    elif "RAILWAY_STATIC_URL" in os.environ:
        return "𝚁𝚊𝚒𝚕𝚠𝚊𝚢"
    else:
        return "𝚅𝙿𝚂 / 𝙻𝚘𝚌𝚊𝚕"

@zq_lo.rep_cmd(pattern=f"{STATS}$")
async def rep_alive(event):
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    start = datetime.now()
    repevent = await edit_or_reply(event, "**⎆┊جـاري .. فحـص البـوت الخـاص بك**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    
    rrd = gvarstatus("r_date") or f"{bt.year}/{bt.month}/{bt.day}"
    rrt = gvarstatus("r_time") or f"{bt.hour}:{bt.minute}"
    reppa = f"{rrd}┊{rrt}"

    R_EMOJI = gvarstatus("ALIVE_EMOJI") or "✥┊"
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "** بـوت ريبـــثون 𝗥𝗲𝗽𝘁𝗵𝗼𝗻 يعمـل .. بنجـاح ☑️ 𓆩 **"
    
    CUSTOM_PIC = gvarstatus("ALIVE_PIC")
    REP_LIST = CUSTOM_PIC.split() if CUSTOM_PIC else RANDOM_MEDIA
    PIC = random.choice(REP_LIST)
    platform_name = get_platform()
    USERID = zq_lo.uid if Config.OWNER_ID == 0 else Config.OWNER_ID
    ALIVE_NAME = gvarstatus("ALIVE_NAME") if gvarstatus("ALIVE_NAME") else "-"
    mention = f"[{ALIVE_NAME}](tg://user?id={USERID})"
    rep_caption = gvarstatus("ALIVE_TEMPLATE") or rep_temp
    caption = rep_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        R_EMOJI=R_EMOJI,
        mention=mention,
        uptime=uptime,
        reppa=reppa,
        rrd=rrd,
        rrt=rrt,
        telever=version.__version__,
        repver=repversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
        platform=platform_name 
    )
    
    try:
        await event.client.send_file(
            event.chat_id, PIC, caption=caption, reply_to=reply_to_id
        )
        await repevent.delete()
    except Exception:
        await edit_or_reply(repevent, caption)


rep_temp = """
⌬ ʀᴇᴘᴛʜᴏɴ ᴜsᴇʀʙᴏᴛ sᴛᴀᴛᴜs
──────────────────
⧓ ᴜsᴇʀ : {mention} 🫵🏻
⧓ ᴠᴇʀsɪᴏɴ : {repver} 🔥
⧓ ᴘʏᴛʜᴏɴ : {pyver} ✔️
⧓ ᴘɪɴɢ : {ping} мѕ
⧓ ᴜᴘᴛɪᴍᴇ : {uptime} 🕰️
⧓ ᴀʟɪᴠᴇ sɪɴᴇᴄ : {reppa} 🕐
⧓ sᴛᴀᴛᴜs : ꜰᴜʟʟʏ ᴀᴄᴛɪᴠᴇ 💪🏻
⧓ ʜᴏsᴛ : {platform} 🌐
──────────────────
◈ @Repthon ◈"""
