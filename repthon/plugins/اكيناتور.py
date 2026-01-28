import os
import re
import asyncio

try:
    from akinator import Akinator
except ModuleNotFoundError:
    os.system("pip3 install akinator.py")
    from akinator import Akinator

try:
    from deep_translator import GoogleTranslator
    translator = GoogleTranslator(source='auto', target='ar')
except ImportError:
    os.system("pip3 install deep-translator")
    from deep_translator import GoogleTranslator
    translator = GoogleTranslator(source='auto', target='ar')

from telethon import Button
from telethon.events import CallbackQuery, InlineQuery

from repthon import zq_lo
from ..Config import Config
from ..core.decorators import check_owner

games = {}
aki_photo = "https://graph.org/file/b0ff07069e8637783fdae.jpg"

@zq_lo.rep_cmd(pattern="اكينوتر(?:\\s|$)([\\s\\S]*)")
async def start_aki_cmd(e):
    aki = Akinator()
    games.update({e.chat_id: {e.id: aki}})
    
    try:
        results = await e.client.inline_query(
            Config.TG_BOT_USERNAME, f"aki_{e.chat_id}_{e.id}"
        )
        await results[0].click(e.chat_id)
    except Exception:
        return await e.reply("**⌔∮ يجب تفعيل وضع الانلاين للبوت من @BotFather أولاً**")
    
    if e.out:
        await e.delete()

@zq_lo.tgbot.on(CallbackQuery(data=re.compile(b"aki_?(.*)")))
@check_owner
async def handle_start(e):
    adt = e.pattern_match.group(1).strip().decode("utf-8")
    dt = adt.split("_")
    ch, mid = int(dt[0]), int(dt[1])
    
    await e.edit("**⌔∮ جاري استدعاء المارد...**")
    
    try:
        loop = asyncio.get_event_loop()
        try:
            q = await loop.run_in_executor(None, lambda: games[ch][mid].start_game(language="ar"))
        except TypeError:
            q = await loop.run_in_executor(None, lambda: games[ch][mid].start_game())
        
        buttons = [
            [Button.inline("✅ نعم", f"aka_{ch}_{mid}_0"), Button.inline("❌ لا", f"aka_{ch}_{mid}_1")],
            [Button.inline("❓ لا أعلم", f"aka_{ch}_{mid}_2"), Button.inline("🤔 ربما", f"aka_{ch}_{mid}_3")],
            [Button.inline("📉 ربما لا", f"aka_{ch}_{mid}_4")]
        ]
        await e.edit(f"**السؤال الأول:**\n\n`{q}`", buttons=buttons)
    except Exception as ex:
        await e.edit(f"**حدث خطأ أثناء التشغيل:**\n`{ex}`")

@zq_lo.tgbot.on(CallbackQuery(data=re.compile(b"aka_?(.*)")))
@check_owner
async def process_answer(e):
    mk = e.pattern_match.group(1).decode("utf-8").split("_")
    if len(mk) < 3: return
    
    ch, mid, ans = int(mk[0]), int(mk[1]), mk[2]
    
    try:
        gm = games[ch][mid]
    except KeyError:
        return await e.answer("⚠️ الجلسة منتهية.", alert=True)

    await e.answer("تفكير... 🤔")
    loop = asyncio.get_event_loop()
    
    try:
        q = await loop.run_in_executor(None, lambda: gm.answer(ans))
        
        if gm.progression >= 80:
            await loop.run_in_executor(None, gm.win)
            res = gm.first_guess
            
            try:
                name_ar = translator.translate(res['name'])
                desc_ar = translator.translate(res['description'])
            except:
                name_ar, desc_ar = res['name'], res['description']
            
            final_text = (
                f"**✨ لقد حزرت الشخصية! ✨**\n\n"
                f"**👤 الاسم:** `{name_ar}`\n"
                f"**📝 الوصف:** `{desc_ar}`\n\n"
                f"**نسبة التأكد:** `{gm.progression}%`"
            )
            return await e.edit(final_text, file=res['absolute_picture_path'], buttons=[Button.inline("🔄 لعب مجدداً", f"aki_{ch}_{mid}")])

        buttons = [
            [Button.inline("✅ نعم", f"aka_{ch}_{mid}_0"), Button.inline("❌ لا", f"aka_{ch}_{mid}_1")],
            [Button.inline("❓ لا أعلم", f"aka_{ch}_{mid}_2"), Button.inline("🤔 ربما", f"aka_{ch}_{mid}_3")],
            [Button.inline("📉 ربما لا", f"aka_{ch}_{mid}_4")]
        ]
        await e.edit(f"**السؤال التالي:**\n\n`{q}`", buttons=buttons)
    except Exception as ex:
        await e.edit(f"**خطأ:** `{ex}`")

@zq_lo.tgbot.on(InlineQuery)
async def handle_inline(e):
    query_user_id = e.query.user_id
    query = e.text
    if (query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS) and query.startswith("aki"):
        ans = [
            await e.builder.photo(
                aki_photo,
                text="**أهلاً بك في أكينوتر!**",
                buttons=[Button.inline("❃ ابدأ اللعب ❃", data=query)],
            )
        ]
        await e.answer(ans)
