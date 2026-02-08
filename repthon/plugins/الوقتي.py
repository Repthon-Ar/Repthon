# @Repthon - Roger
# Copyright (C) 2022 RepthonArabic. All Rights Reserved
#< https://t.me/Repthon >
# This file is a part of < https://github.com/Repthon-Arabic/RepthonAr/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/Repthon-Arabic/RepthonAr/blob/master/LICENSE/>.
#كـود الصورة الوقتيه كتـابتي وتعديلـي من زمان ومتعوب عليها 
#+ كـود زخـرفة الصورة الوقتيه
#+ دددي لا ابلـع حســابك بـانـد بطـعـم الليمــون 🍋😹🤘
#بـاقـر يـ ولــد - حقــوق لـ التــاريـخ ®
#هههههههههههههههههههههههههههههههههههههههههههههههههه

import asyncio
import math
import os
import shutil
import time
import urllib3
import urllib.request
import aiohttp
import base64
import requests
from datetime import datetime as dt
from pytz import timezone

from PIL import Image, ImageDraw, ImageFont
from urlextract import URLExtract
from pySmartDL import SmartDL
from catbox import CatboxUploader
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from telethon.errors import FloodWaitError
from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.errors.rpcerrorlist import AboutTooLongError

from ..Config import Config
from ..helpers.utils import _format
from ..core.managers import edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import edit_delete, zq_lo, logging, BOTLOG, BOTLOG_CHATID, mention

plugin_category = "الادوات"
LOGS = logging.getLogger(__name__)
CHANGE_TIME = int(gvarstatus("CHANGE_TIME")) if gvarstatus("CHANGE_TIME") else 60
FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

normretext = "1234567890"

autopic_path = os.path.join(os.getcwd(), "repthon", "original_pic.png")
digitalpic_path = os.path.join(os.getcwd(), "repthon", "digital_pic.png")
autophoto_path = os.path.join(os.getcwd(), "repthon", "photo_pfp.png")


NAUTO = gvarstatus("R_NAUTO") or "(الاسم تلقائي|الاسم الوقتي|اسم وقتي|اسم تلقائي)"
NAAUTO = gvarstatus("R_NAAUTO") or "(الاسم تلقائي2|الاسم الوقتي2|اسم وقتي2|اسم تلقائي2)"
PAUTO = gvarstatus("R_PAUTO") or "(البروفايل تلقائي|الصوره الوقتيه|الصورة الوقتية|صوره وقتيه|البروفايل)"
BAUTO = gvarstatus("R_BAUTO") or "(البايو تلقائي|البايو الوقتي|بايو وقتي|نبذه وقتيه|النبذه الوقتيه)"

extractor = URLExtract()
uploader = CatboxUploader()

if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)

async def digitalpicloop():
    DIGITALPICSTART = gvarstatus("digitalpic") == "true"
    i = 0
    while DIGITALPICSTART:
        try:
            if not os.path.exists(digitalpic_path):
                digitalpfp = gvarstatus("DIGITAL_PIC")
                async with aiohttp.ClientSession() as session:
                    async with session.get(digitalpfp) as response:
                        if response.status == 200:
                            data = await response.read()
                            with open(digitalpic_path, 'wb') as f:
                                f.write(data)
                        else:
                            await asyncio.sleep(CHANGE_TIME)
                            continue
        except Exception as e:
            print(f"خطأ: {e}")
            await asyncio.sleep(5)
            continue
        repfont = gvarstatus("DEFAULT_PIC") if gvarstatus("DEFAULT_PIC") else "repthon/helpers/styles/REPTHONEMOGE.ttf" #Code by T.me/RR0RT
        shutil.copy(digitalpic_path, autophoto_path)
        Image.open(autophoto_path)
        TIME_ZONE = gvarstatus("T_Z") if gvarstatus("T_Z") else Config.TZ
        RTZone = dt.now(timezone(TIME_ZONE))
        RTime = RTZone.strftime('%H:%M')
        RT = dt.strptime(RTime, "%H:%M").strftime("%I:%M")
        #current_time = dt.now().strftime("%I:%M")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(f"{repfont}", 35) #Code by T.me/RR0RT
        drawn_text.text((140, 70), RT, font=fnt, fill=(280, 280, 280)) #Code by T.me/RR0RT
        img.save(autophoto_path)
        file = await zq_lo.upload_file(autophoto_path)
        try:
            if i > 0:
                await zq_lo(
                    functions.photos.DeletePhotosRequest(
                        await zq_lo.get_profile_photos("me", limit=1)
                    )
                )
            i += 1
            await zq_lo(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return
        DIGITALPICSTART = gvarstatus("digitalpic") == "true"


async def autoname_loop():
    while AUTONAMESTART := gvarstatus("autoname") == "true":
        #DM = time.strftime("%d-%m-%y")
        #HM = time.strftime("%I:%M")
        TIME_ZONE = gvarstatus("T_Z") if gvarstatus("T_Z") else Config.TZ
        RTZone = dt.now(timezone(TIME_ZONE))
        RTime = RTZone.strftime('%H:%M')
        RT = dt.strptime(RTime, "%H:%M").strftime("%I:%M")
        for normal in RT:
            if normal in normretext:
              namerefont = gvarstatus("BA_FN") or "𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬" 
              namefont = namerefont[normretext.index(normal)]
              RT = RT.replace(normal, namefont)
        REPT = gvarstatus("CUSTOM_ALIVE_EMREP") or " 𓏺" #Code by T.me/@RR0RT
        name = f"{RT}{REPT}"
        LOGS.info(name)
        try:
            await zq_lo(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)
        AUTONAMESTART = gvarstatus("autoname") == "true"


async def auto2name_loop(): #Code by T.me/@RR0RT
    while AUTO2NAMESTART := gvarstatus("auto2name") == "true":
        #DM = time.strftime("%d-%m-%y")
        #HM = time.strftime("%I:%M")
        TIME_ZONE = gvarstatus("T_Z") if gvarstatus("T_Z") else Config.TZ
        RTZone = dt.now(timezone(TIME_ZONE))
        RTime = RTZone.strftime('%H:%M')
        RT = dt.strptime(RTime, "%H:%M").strftime("%I:%M")
        for normal in RT:
            if normal in normretext:
              namerefont = gvarstatus("BA_FN") or "𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬" 
              namefont = namerefont[normretext.index(normal)]
              RT = RT.replace(normal, namefont)
        REPT = gvarstatus("CUSTOM_ALIVE_EMREP") or "𓏺 " #Code by T.me/@RR0RT
        name = f"{REPT}{RT}"
        LOGS.info(name)
        try:
            await zq_lo(functions.account.UpdateProfileRequest(last_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)
        AUTO2NAMESTART = gvarstatus("auto2name") == "true"


async def autobio_loop():
    AUTOBIOSTART = gvarstatus("autobio") == "true"
    while AUTOBIOSTART:
        #DMY = time.strftime("%d.%m.%Y")
        #HM = time.strftime("%I:%M")
        TIME_ZONE = gvarstatus("T_Z") if gvarstatus("T_Z") else Config.TZ
        RTZone = dt.now(timezone(TIME_ZONE))
        RTime = RTZone.strftime('%H:%M')
        RT = dt.strptime(RTime, "%H:%M").strftime("%I:%M")
        for normal in RT:
            if normal in normretext:
              namerefont = gvarstatus("BA_FN") or "𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬"
              namefont = namerefont[normretext.index(normal)]
              RT = RT.replace(normal, namefont)
        DEFAULTUSERBIO = gvarstatus("DEFAULT_BIO") or "‏{وَتَوَكَّلْ عَلَى اللَّهِ ۚ وَكَفَىٰ بِاللَّهِ وَكِيلًا}" #Code by T.me/zzzzl1l
        bio = f"{DEFAULTUSERBIO} ⏐ {RT}" 
        LOGS.info(bio)
        try:
            await zq_lo(functions.account.UpdateProfileRequest(about=bio))
        except AboutTooLongError:
            delgvar("autobio")
            DEFAULTUSERBIO = gvarstatus("DEFAULT_BIO") or "الحمد الله على كل شئ"
            await zq_lo(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await zq_lo.send_message(BOTLOG_CHATID, "**⎉╎البايو طويل جداً على الحد المسموح به من تيليجرام ✖️**\n**⎉╎ قم باضافة بايو اقصر عبر الرد على البايو بالأمر (** `.اضف فار البايو` **)**")
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)
        AUTOBIOSTART = gvarstatus("autobio") == "true"

@zq_lo.rep_cmd(pattern=f"{PAUTO}$")
async def _(event):
    rep = await edit_or_reply(event, "**• جـارِ تفعيـل البروفايـل الوقتي...**")
    downloaded_file_name = await event.client.download_profile_photo(
        zq_lo.uid,
        Config.TMP_DOWNLOAD_DIRECTORY + str(zq_lo.uid) + ".jpg",
        download_big=True,
    )
    if not downloaded_file_name:
        return await rep.edit("**⎉╎فشل في تحميل الصورة**")
    try:
        media_url = uploader.upload_file(downloaded_file_name)
        addgvar("DIGITAL_PIC", media_url)
        addgvar("digitalpic", "true")
        await rep.edit("**⎉╎تم تفعيل البروفايل الوقتي ✓**")
        await digitalpicloop()
    except Exception as e:
        await rep.edit(f"**⎉╎خطأ: {str(e)}**")
    finally:
        if os.path.exists(downloaded_file_name):
            os.remove(downloaded_file_name)

@zq_lo.rep_cmd(pattern=f"{NAUTO}$")
async def _(event):
    if gvarstatus("auto2name") is not None and gvarstatus("auto2name") == "true":
        delgvar("auto2name")
    if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
        return await edit_or_reply(event, "**⎉╎الاسـم الوقتـي .. تم تفعيلـه سابقـاً**")
    rrr = await edit_or_reply(event, "**• جـارِ تفعيـل الاسـم الوقتـي ⅏. . .**")
    user = await event.client.get_me()
    DEFAULTUSER = gvarstatus("ALIVE_NAME") if gvarstatus("ALIVE_NAME") else Config.ALIVE_NAME
    if ("𝟬" not in user.first_name) or ("𝟎" not in user.first_name) or ("٠" not in user.first_name) or ("₀" not in user.first_name) or ("⁰" not in user.first_name) or ("✪" not in user.first_name) or ("⓿" not in user.first_name) or ("⊙" not in user.first_name) or ("⓪" not in user.first_name) or ("𝟢" not in user.first_name) or ("𝟶" not in user.first_name) or ("𝟘" not in user.first_name) or ("０" not in user.first_name):
        baqir = user.first_name if user.first_name else "-"
        await event.client(functions.account.UpdateProfileRequest(last_name=baqir))
    elif ("𝟬" not in DEFAULTUSER) or ("𝟎" not in DEFAULTUSER) or ("٠" not in DEFAULTUSER) or ("₀" not in DEFAULTUSER) or ("⁰" not in DEFAULTUSER) or ("✪" not in DEFAULTUSER) or ("⓿" not in DEFAULTUSER) or ("⊙" not in DEFAULTUSER) or ("⓪" not in DEFAULTUSER) or ("𝟢" not in DEFAULTUSER) or ("𝟶" not in DEFAULTUSER) or ("𝟘" not in DEFAULTUSER) or ("０" not in DEFAULTUSER):
        baqir = user.first_name if user.first_name else "-"
        await event.client(functions.account.UpdateProfileRequest(last_name=baqir))
    else:
        baqir = DEFAULTUSER
        await event.client(functions.account.UpdateProfileRequest(last_name=baqir))
    addgvar("autoname", True)
    await rrr.edit("<b>⎉╎تـم بـدء الاسـم الوقتـي🝛 .. بنجـاح ✓</b>\n<b>⎉╎زخـارف الاسـم الوقتـي ↶ <a href = https://t.me/Repthon_vars/24>⦇  اضـغـط هنــا  ⦈</a> </b>", parse_mode="html", link_preview=False)
    await autoname_loop()


@zq_lo.rep_cmd(pattern=f"{NAAUTO}$")
async def _(event): #Code by T.me/@RR0RT
    if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
        delgvar("autoname")
    if gvarstatus("auto2name") is not None and gvarstatus("auto2name") == "true":
        return await edit_delete(event, "**⎉╎الاسـم الوقتـي² .. تم تفعيلـه سابقـاً**")
    zzz = await edit_or_reply(event, "**• جـارِ تفعيـل الاسـم الوقتـي² ⅏. . .**")
    addgvar("auto2name", True)
    await zzz.edit("<b>⎉╎تـم بـدء الاسـم الوقتـي²🝛 .. بنجـاح ✓</b>\n<b>⎉╎زخـارف الاسـم الوقتـي ↶ <a href = https://t.me/Repthon_vars/24>⦇  اضـغـط هنــا  ⦈</a> </b>", parse_mode="html", link_preview=False)
    await auto2name_loop()


@zq_lo.rep_cmd(pattern=f"{BAUTO}$")
async def _(event):
    if gvarstatus("DEFAULT_BIO") is None:
        return await edit_delete(event, "**- فار النبـذة الوقتيـه غيـر موجـود ؟!**\n**- ارسـل نـص النبـذه ثم قم بالـرد عليهـا بالامـر :**\n\n`.اضف البايو`")
    if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
        return await edit_delete(event, "**⎉╎النبـذه الوقتـيه .. مفعلـه سابقـاً**")
    addgvar("autobio", True)
    await edit_delete(event, "**⎉╎تـم بـدء الـنبذة الوقتيـه .. بنجـاح ✓**")
    await autobio_loop()


@zq_lo.rep_cmd(
    pattern="الغاء(?: |$)(.*)",
    command=("الغاء", plugin_category),
    info={
        "header": "To stop the functions of autoprofile",
        "description": "If you want to stop autoprofile functions then use this cmd.",
        "options": {
            "digitalpfp": "To stop difitalpfp",
            "autoname": "To stop autoname",
            "autobio": "To stop autobio",
        },
        "usage": "{tr}end <option>",
        "examples": ["{tr}end autopic"],
    },
)
async def _(event):  # sourcery no-metrics
    "To stop the functions of autoprofile plugin"
    input_str = event.pattern_match.group(1)
    if input_str == "البروفايل تلقائي" or input_str == "البروفايل" or input_str == "البروفايل التلقائي" or input_str == "الصوره الوقتيه" or input_str == "الصورة الوقتية":
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف البروفـايل الوقتـي .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎البروفـايل الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "الاسم تلقائي" or input_str == "الاسم" or input_str == "الاسم التلقائي" or input_str == "الاسم الوقتي" or input_str == "اسم الوقتي":
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            DEFAULTUSER = gvarstatus("ALIVE_NAME") if gvarstatus("ALIVE_NAME") else Config.ALIVE_NAME
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER, last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي .. بنجـاح ✓**")
        if gvarstatus("auto2name") is not None and gvarstatus("auto2name") == "true": #Code by T.me/RR0RT
            delgvar("auto2name")
            await event.client(
                functions.account.UpdateProfileRequest(last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي² .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎الاسـم الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "البايو تلقائي" or input_str == "البايو" or input_str == "البايو التلقائي" or input_str == "البايو الوقتي" or input_str == "النبذه الوقتيه" or input_str == "النبذة الوقتية" or input_str == "بايو الوقتي" or input_str == "نبذه الوقتي":
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            DEFAULTUSERBIO = gvarstatus("DEFAULT_BIO") or "الحمد الله على كل شئ - @Repthon"
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف النبـذه الوقتيـه .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎النبـذه الوقتيـه .. غيـر مفعـله اصـلاً ؟!**")


@zq_lo.rep_cmd(
    pattern="انهاء(?: |$)(.*)",
    command=("انهاء", plugin_category),
    info={
        "header": "To stop the functions of autoprofile",
        "description": "If you want to stop autoprofile functions then use this cmd.",
        "options": {
            "digitalpfp": "To stop difitalpfp",
            "autoname": "To stop autoname",
            "autobio": "To stop autobio",
        },
        "usage": "{tr}end <option>",
        "examples": ["{tr}end autopic"],
    },
)
async def _(event):  # sourcery no-metrics
    "To stop the functions of autoprofile plugin"
    input_str = event.pattern_match.group(1)
    if input_str == "البروفايل تلقائي" or input_str == "البروفايل" or input_str == "البروفايل التلقائي" or input_str == "الصوره الوقتيه" or input_str == "الصورة الوقتية":
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف البروفـايل الوقتـي .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎البروفـايل الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "الاسم تلقائي" or input_str == "الاسم" or input_str == "الاسم التلقائي" or input_str == "الاسم الوقتي" or input_str == "اسم الوقتي":
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            DEFAULTUSER = gvarstatus("ALIVE_NAME") if gvarstatus("ALIVE_NAME") else Config.ALIVE_NAME
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER, last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي .. بنجـاح ✓**")
        if gvarstatus("auto2name") is not None and gvarstatus("auto2name") == "true": #Code by T.me/zzzzl1l
            delgvar("auto2name")
            await event.client(
                functions.account.UpdateProfileRequest(last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي² .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎الاسـم الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "البايو تلقائي" or input_str == "البايو" or input_str == "البايو التلقائي" or input_str == "البايو الوقتي" or input_str == "النبذه الوقتيه" or input_str == "النبذة الوقتية" or input_str == "بايو الوقتي" or input_str == "نبذه الوقتي":
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            DEFAULTUSERBIO = gvarstatus("DEFAULT_BIO") or "الحمد الله على كل شئ - @ZedThon"
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف النبـذه الوقتيـه .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎النبـذه الوقتيـه .. غيـر مفعـله اصـلاً ؟!**")

 



@zq_lo.rep_cmd(
    pattern="ايقاف(?: |$)(.*)",
    command=("ايقاف", plugin_category),
    info={
        "header": "To stop the functions of autoprofile",
        "description": "If you want to stop autoprofile functions then use this cmd.",
        "options": {
            "digitalpfp": "To stop difitalpfp",
            "autoname": "To stop autoname",
            "autobio": "To stop autobio",
        },
        "usage": "{tr}end <option>",
        "examples": ["{tr}end autopic"],
    },
)
async def _(event):  # sourcery no-metrics
    "To stop the functions of autoprofile plugin"
    input_str = event.pattern_match.group(1)
    if input_str == "البروفايل تلقائي" or input_str == "البروفايل" or input_str == "البروفايل التلقائي" or input_str == "الصوره الوقتيه" or input_str == "الصورة الوقتية":
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف البروفـايل الوقتـي .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎البروفـايل الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "الاسم تلقائي" or input_str == "الاسم" or input_str == "الاسم التلقائي" or input_str == "الاسم الوقتي" or input_str == "اسم الوقتي":
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            DEFAULTUSER = gvarstatus("ALIVE_NAME") if gvarstatus("ALIVE_NAME") else Config.ALIVE_NAME
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER, last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي .. بنجـاح ✓**")
        if gvarstatus("auto2name") is not None and gvarstatus("auto2name") == "true": #Code by T.me/zzzzl1l
            delgvar("auto2name")
            await event.client(
                functions.account.UpdateProfileRequest(last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي² .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎الاسـم الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "البايو تلقائي" or input_str == "البايو" or input_str == "البايو التلقائي" or input_str == "البايو الوقتي" or input_str == "النبذه الوقتيه" or input_str == "النبذة الوقتية" or input_str == "بايو الوقتي" or input_str == "نبذه الوقتي":
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            DEFAULTUSERBIO = gvarstatus("DEFAULT_BIO") or "الحمد الله على كل شئ - @ZedThon"
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف النبـذه الوقتيـه .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎النبـذه الوقتيـه .. غيـر مفعـله اصـلاً ؟!**")



zq_lo.loop.create_task(digitalpicloop())
zq_lo.loop.create_task(autoname_loop())
zq_lo.loop.create_task(auto2name_loop())
zq_lo.loop.create_task(autobio_loop())


# ================================================================================================ #
# =========================================الوقتيه================================================= #
# ================================================================================================ #


BaqirVP_cmd = (
    "𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲 𝗥𝗲𝗽𝘁𝗵𝗼𝗻 - اوامـر الفـارات](t.me/Repthon) 𓆪\n\n"
    "**✾╎قائـمه اوامـر تغييـر زخـارف البروفايـل + الاسـم الوقـتي بأمـر واحـد فقـط 🦾 :** \n\n"
    "⪼ `.وقتيه 1` / `.الوقتي 1`\n\n"
    "⪼ `.وقتيه 2` / `.الوقتي 2`\n\n"
    "⪼ `.وقتيه 3` / `.الوقتي 3`\n\n"
    "⪼ `.وقتيه 4` / `.الوقتي 4`\n\n"
    "⪼ `.وقتيه 5` / `.الوقتي 5`\n\n"
    "⪼ `.وقتيه 6` / `.الوقتي 6`\n\n"
    "⪼ `.وقتيه 7` / `.الوقتي 7`\n\n"
    "⪼ `.وقتيه 8` / `.الوقتي 8`\n\n"
    "⪼ `.وقتيه 9` / `.الوقتي 9`\n\n"
    "⪼ `.وقتيه 10` / `.الوقتي 10`\n\n"
    "⪼ `.وقتيه 11` / `.الوقتي 11`\n\n"
    "⪼ `.وقتيه 12` / `.الوقتي 12`\n\n"
    "⪼ `.وقتيه 13` / `.الوقتي 13`\n\n"
    "⪼ `.وقتيه 14` / `.الوقتي 14`\n\n"
    "⪼ `.وقتيه 15`\n\n"
    "⪼ `.وقتيه 16`\n\n"
    "⪼ `.وقتيه 17`\n\n\n"
    "**✾╎لـ رؤيـة زغـارف الصورة الوقتـية ↶**  [⦇  اضـغـط هنــا  ⦈](t.me/Repthon_vars/20) \n\n"
    "**✾╎لـ رؤيـة زغـارف الاســم الوقتـي ↶**  [⦇  اضـغـط هنــا  ⦈](t.me/Repthon_vars/24) \n\n\n"
    "🛃 سيتـم اضـافة المزيـد من الزغـارف بالتحديثـات الجـايـه\n\n"
    "\n𓆩 [℡✗ ¦ ↱𝐺𝑜𝑙 𝐷. 𝑅𝑜𝑔𝑒𝑟↲ ¦ ✗𖠚卐](t.me/RR0RT) 𓆪"
)


# Copyright (C) 2022 Repthon . All Rights Reserved
@zq_lo.rep_cmd(pattern="وقتيه(?: |$)(.*)")
async def variable(event):
    input_str = event.pattern_match.group(1)
    rep = await edit_or_reply(event, "**✾╎جـاري اضـافة زخـرفـة الوقتيـه لـ بوتـك 💞🦾 . . .**")
    # All Rights Reserved for "@Repthon" "باقر"
    if input_str == "1":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/Repthon.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "2":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/Starjedi.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "3":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/Papernotes.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "4":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/Terserah.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "5":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/Photography Signature.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "6":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/Austein.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "7":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/Dream MMA.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "8":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/EASPORTS15.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "9":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/KGMissKindergarten.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "10":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/212 Orion Sans PERSONAL USE.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "11":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/PEPSI_pl.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "12":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/Paskowy.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "13":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/Cream Cake.otf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "14":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/Hello Valentina.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "15":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/Alien-Encounters-Regular.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "16":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/Linebeam.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "17":
        variable = "DEFAULT_PIC"
        rinfo = "repthon/helpers/styles/EASPORTS15.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, rinfo)


# Copyright (C) 2022 @Repthon . All Rights Reserved
@zq_lo.rep_cmd(pattern="الوقتي(?: |$)(.*)")
async def baqir(event):
    input_str = event.pattern_match.group(1)
    rep = await edit_or_reply(event, "**✾╎جـاري اضـافة زخـرفـة الوقتيـه لـ بوتـك 💞🦾 . . .**")
    # All Rights Reserved for "@Repthon" "باقر"
    if input_str == "1":
        rinfo = "𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(rinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(rinfo))
        addgvar("BA_FN", "𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬")
    elif input_str == "2":
        rinfo = "𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(rinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(rinfo))
        addgvar("BA_FN", "𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎")
    elif input_str == "3":
        rinfo = "١٢٣٤٥٦٧٨٩٠"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(rinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(rinfo))
        addgvar("BA_FN", "١٢٣٤٥٦٧٨٩٠")
    elif input_str == "4":
        rinfo = "₁₂₃₄₅₆₇₈₉₀"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(rinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(rinfo))
        addgvar("BA_FN", "₁₂₃₄₅₆₇₈₉₀")
    elif input_str == "5":
        rinfo = "¹²³⁴⁵⁶⁷⁸⁹⁰"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(rinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(rinfo))
        addgvar("BA_FN", "¹²³⁴⁵⁶⁷⁸⁹⁰")
    elif input_str == "6":
        rinfo = "➊➋➌➍➎➏➐➑➒✪"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(rinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(rinfo))
        addgvar("BA_FN", "➊➋➌➍➎➏➐➑➒✪")
    elif input_str == "7":
        rinfo = "❶❷❸❹❺❻❼❽❾⓿"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(rinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(rinfo))
        addgvar("BA_FN", "❶❷❸❹❺❻❼❽❾⓿")
    elif input_str == "8":
        rinfo = "➀➁➂➃➄➅➆➇➈⊙"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(rinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(rinfo))
        addgvar("BA_FN", "➀➁➂➃➄➅➆➇➈⊙")
    elif input_str == "9":
        rinfo = "⓵⓶⓷⓸⓹⓺⓻⓼⓽⓪"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("BA_FN", "⓵⓶⓷⓸⓹⓺⓻⓼⓽⓪")
    elif input_str == "10":
        rinfo = "①②③④⑤⑥⑦⑧⑨⓪"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("BA_FN", "①②③④⑤⑥⑦⑧⑨⓪")
    elif input_str == "11":
        rinfo = "𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(rinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(rinfo))
        addgvar("BA_FN", "𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢")
    elif input_str == "12":
        rinfo = "𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝟶"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(rinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(rinfo))
        addgvar("BA_FN", "𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝟶")
    elif input_str == "13":
        rinfo = "𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(rinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(rinfo))
        addgvar("BA_FN", "𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘")
    elif input_str == "14":
        zinfo = "１２３４５６７８９０"
        await asyncio.sleep(1.5)
        if gvarstatus("BA_FN") is not None:
            await rep.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(rinfo))
        else:
            await rep.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(rinfo))
        addgvar("BA_FN", "１２３４５６７８９０")



# Copyright (C) 2022 @Repthon . All Rights Reserved
@zq_lo.rep_cmd(pattern="اوامر الوقتي")
async def cmd(baqir):
    await edit_or_reply(baqir, BaqirVP_cmd)



# Copyright (C) 2022 @Repthon . All Rights Reserved
@zq_lo.rep_cmd(pattern="الخط(?: |$)(.*)")
async def variable(event):
    input_str = event.pattern_match.group(1)
    rep = await edit_or_reply(event, "**✾╎جـاري اضـافة زخـرفـة خـط الحقـوق لـ بوتـك 💞🦾 . . .**")
    # All Rights Reserved for "@Repthon" "باقر"
    if input_str == "1":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/Repthon.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "2":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/Starjedi.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "3":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/Papernotes.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "4":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/Terserah.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "5":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/Photography Signature.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "6":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/Austein.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "7":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/Dream MMA.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "8":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/EASPORTS15.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "9":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/KGMissKindergarten.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "10":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/212 Orion Sans PERSONAL USE.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "11":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/PEPSI_pl.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "12":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/Paskowy.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "13":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/Cream Cake.otf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "14":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/Hello Valentina.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "15":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/Alien-Encounters-Regular.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "16":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/Linebeam.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
    elif input_str == "17":
        variable = "REP_FONTS"
        rinfo = "repthon/helpers/styles/EASPORTS15.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("REP_FONTS") is None:
            await rep.edit("**✾╎تم اضـافـة زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        else:
            await rep.edit("**✾╎تم تغييـر زغـرفـة خـط الحقـوق {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.حقوق` **+ كلمـه بالـرد ع (صوره-ملصق-متحركه-فيديو) . .**".format(input_str))
        addgvar(variable, rinfo)
