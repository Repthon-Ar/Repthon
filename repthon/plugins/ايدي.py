import asyncio
import contextlib
import re
import aiohttp
import time
import html
import shutil
import os
import random
import base64
import requests
from requests import get
from datetime import datetime

from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import MessageEntityMentionName, EmojiStatusEmpty, MessageActionChannelMigrateFrom
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors import ChannelInvalidError, ChannelPrivateError, ChannelPublicGroupNaError, BadRequestError
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest, ExportChatInviteRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.utils import pack_bot_file_id
from telethon.errors.rpcerrorlist import YouBlockedUserError, ChatSendMediaForbiddenError
from telethon import events, types
from telethon.extensions import markdown, html
#from .xtelethonimport CustomParseMode  # TODO: Call the class from custom module
from . import zq_lo
from ..Config import Config
from ..utils import Rep_Vip, Rep_Dev
from ..helpers import reply_id
from ..helpers.utils import _format
from ..core.logger import logging
from ..core.managers import edit_or_reply, edit_delete
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.echo_sql import addecho, get_all_echos, get_echos, is_echo, remove_all_echos, remove_echo, remove_echos
from . import BOTLOG, BOTLOG_CHATID, spamwatch

plugin_category = "العروض"
LOGS = logging.getLogger(__name__)
RID = gvarstatus("R_RRID") or "ايديه"
Rep_Uid = zq_lo.uid
#zq_lo.parse_mode = CustomParseMode('markdown')  # TODO: Choose parsemode
dev_baqir = (1260465030, 7984777405)
REP_BLACKLIST = []


def parse_registration_time(reg_time: int):
    return datetime.fromtimestamp(reg_time).strftime('%Y-%m-%d')

entries = [
    (1000000, 1380326400),  # 2013
    (2768409, 1383264000),
    (7679610, 1388448000),
    (11538514, 1391212000),  # 2014
    (15835244, 1392940000),
    (23646077, 1393459000),
    (38015510, 1393632000),
    (44634663, 1399334000),
    (46145305, 1400198000),
    (54845238, 1411257000),
    (63263518, 1414454000),
    (101260938, 1425600000),  # 2015
    (101323197, 1426204000),
    (103151531, 1433376000),
    (103258382, 1432771000),
    (109393468, 1439078000),
    (111220210, 1429574000),
    (112594714, 1439683000),
    (116812045, 1437696000),
    (122600695, 1437782000),
    (124872445, 1439856000),
    (125828524, 1444003000),
    (130029930, 1441324000),
    (133909606, 1444176000),
    (143445125, 1448928000),
    (148670295, 1452211000),  # 2016
    (152079341, 1453420000),
    (157242073, 1446768000),
    (171295414, 1457481000),
    (181783990, 1460246000),
    (222021233, 1465344000),
    (225034354, 1466208000),
    (278941742, 1473465000),
    (285253072, 1476835000),
    (294851037, 1479600000),
    (297621225, 1481846000),
    (328594461, 1482969000),
    (337808429, 1487707000),  # 2017
    (341546272, 1487782000),
    (352940995, 1487894000),
    (369669043, 1490918000),
    (400169472, 1501459000),
    (616816630, 1529625600),  # 2018
    (681896077, 1532821500),
    (727572658, 1543708800),
    (796147074, 1541371800),
    (925078064, 1563290000),  # 2019
    (928636984, 1581513420),  # 2020
    (1054883348, 1585674420),
    (1057704545, 1580393640),
    (1145856008, 1586342040),
    (1227964864, 1596127860),
    (1382531194, 1600188120),
    (1658586909, 1613148540),  # 2021
    (1660971491, 1613329440),
    (1692464211, 1615402500),
    (1719536397, 1619293500),
    (1721844091, 1620224820),
    (1772991138, 1617540360),
    (1807942741, 1625520300),
    (1893429550, 1622040000),
    (1972424006, 1631669400),
    (1974255900, 1634000000),
    (2030606431, 1631992680),
    (2041327411, 1631989620),
    (2078711279, 1634321820),
    (2104178931, 1638353220),
    (2120496865, 1636714020),
    (2123596685, 1636503180),
    (2138472342, 1637590800),
    (3318845111, 1618028800),
    (4317845111, 1620028800),
    (5162494923, 1652449800),  # 2022
    (5186883095, 1648764360),
    (5304951856, 1656718440),
    (5317829834, 1653152820),
    (5318092331, 1652024220),
    (5336336790, 1646368100),
    (5362593868, 1652024520),
    (5387234031, 1662137700),
    (5396587273, 1648014800),
    (5409444610, 1659025020),
    (5416026704, 1660925460),
    (5465223076, 1661710860),
    (5480654757, 1660926300),
    (5499934702, 1662130740),
    (5513192189, 1659626400),
    (5522237606, 1654167240),
    (5537251684, 1664269800),
    (5559167331, 1656718560),
    (5568348673, 1654642200),
    (5591759222, 1659025500),
    (5608562550, 1664012820),
    (5614111200, 1661780160),
    (5666819340, 1664112240),
    (5684254605, 1662134040),
    (5684689868, 1661304720),
    (5707112959, 1663803300),
    (5756095415, 1660925940),
    (5772670706, 1661539140),
    (5778063231, 1667477640),
    (5802242180, 1671821040),
    (5853442730, 1674866100),  # 2023
    (5859878513, 1673117760),
    (5885964106, 1671081840),
    (5982648124, 1686941700),
    (6020888206, 1675534800),
    (6032606998, 1686998640),
    (6057123350, 1676198350),
    (6058560984, 1686907980),
    (6101607245, 1686830760),
    (6108011341, 1681032060),
    (6132325730, 1692033840),
    (6182056052, 1687870740),
    (6279839148, 1688399160),
    (6306077724, 1692442920),
    (6321562426, 1688486760),
    (6364973680, 1696349340),
    (6386727079, 1691696880),
    (6429580803, 1692082680),
    (6527226055, 1690289160),
    (6813121418, 1698489600),
    (6865576492, 1699052400),
    (6925870357, 1701192327),  
    (6986164222, 1701291564),
    (6908583918, 1704190978),  # 1  2024
    (6789142671, 1704548133),  # 1  2024 6
    (6819617432, 1704634533),  # 1  2024 7
    (6841678917, 1705066619),  # 1  2024 12
    (6740190197, 1706621819),  # 1  2024 30
    (6987617407, 1706828693),  # 2  2024
    (6901991004, 1706881019),  # 2  2024 2
    (6481292195, 1707313019),  # 2  2024 7
    (6298589281, 1708090619),  # 2  2024 16
    (6859218547, 1708349819),  # 2  2024 19
    (7071421922, 1708781819),  # 2  2024 24
    (7076644280, 1709334293),  # 3  2024
    (7111834877, 1709386619),  # 3  2024 2
    (6426532367, 1709818619),  # 3  2024 7
    (7095981585, 1710077819),  # 3  2024 10
    (6765158346, 1710337019),  # 3  2024 13
    (7030253025, 1710509819),  # 3  2024 15
    (7120688902, 1710682619),  # 3  2024 17
    (7199647175, 1710769019),  # 3  2024 18
    (6735293160, 1711633019),  # 3  2024 28
    (7035507513, 1711892219),  # 3  2024 31
    (7190655769, 1712012693),  # 4  2024
    (7092147884, 1712583419),  # 4  2024 8
    (6736662943, 1713101819),  # 4  2024 14
    (6709197876, 1713706619),  # 4  2024 21
    (7139496906, 1713793019),  # 4  2024 22
    (6839520908, 1714052219),  # 4  2024 25
    (6406354568, 1714138619),  # 4  2024 26
    (6314662459, 1714604693),  # 5  2024
    (6851341949, 1715089019),  # 5  2024 7
    (6617469844, 1715175419),  # 5  2024 8
    (6509264787, 1715434619),  # 5  2024 11
    (6998788527, 1715866619),  # 5  2024 16
    (7070171652, 1716125819),  # 5  2024 19
    (6634798413, 1716212219),  # 5  2024 20
    (7063353380, 1716385019),  # 5  2024 22
    (7048338448, 1716730619),  # 5  2024 26
    (6962490360, 1717162619),  # 5  2024 31
    (7061363744, 1717369493),  # 6  2024 2
    (6483413861, 1717421819),  # 6  2024 3 
    (7217061391, 1717508219),  # 6  2024 4
    (7184774821, 1717767419),  # 6  2024 7
    (7228987219, 1717853819),  # 6  2024 8
    (6517920416, 1718026619),  # 6  2024 10
    (7220580468, 1718113019),  # 6  2024 11
    (6407804362, 1718199419),  # 6  2024 12
    (7309229792, 1718285819),  # 6  2024 13
    (7335965415, 1718372219),  # 6  2024 14
    (7403480414, 1718545019),  # 6  2024 16
    (7355675121, 1718717819),  # 6  2024 18
    (7215394296, 1718977019),  # 6  2024 21
    (7482526044, 1719063419),  # 6  2024 22
    (7389140318, 1719149819),  # 6  2024 23
    (7329204618, 1719322619),  # 6  2024 25
    (6674196655, 1719409019),  # 6  2024 26
    (7355766296, 1719495419),  # 6  2024 27 
    (6726237511, 1719581819),  # 6  2024 28
    (7031946341, 1719875458),  # 7  2024
    (7356277790, 1719927419),  # 7  2024 2
    (7062534228, 1720186619),  # 7  2024 5
    (7069338083, 1720273019),  # 7  2024 6
    (6925327475, 1720305025),  # 7  2024 6 10.30
    (7376713041, 1720603825),  # 7  2024 10
    (6635521856, 1720690225),  # 7  2024 11
    (6680796824, 1720776625),  # 7  2024 12
    (7356141572, 1721122225),  # 7  2024 16
    (7310717903, 1721208625),  # 7  2024 17
    (7225544354, 1721295025),  # 7  2024 18
    (7436784240, 1721381425),  # 7  2024 19
    (7179266128, 1721467825),  # 7  2024 20
    (7438316067, 1721554225),  # 7  2024 21
    (7425293482, 1721640625),  # 7  2024 22
    (7237902404, 1721727025),  # 7  2024 23
    (7241222269, 1721813425),  # 7  2024 24
    (7372474328, 1721899825),  # 7  2024 25
    (7326309434, 1722072625),  # 7  2024 27
    (7424762420, 1722245425),  # 7  2024 29
    (7263151717, 1722331825),  # 7  2024 30
    (7127630690, 1722418225),  # 7  2024 31
    (7072147121, 1722553927),  # 8  2024
    (7194447636, 1722591025),  # 8  2024 2
    (7472043188, 1722763825),  # 8  2024 4
    (7349822507, 1723023025),  # 8  2024 7
    (7478876280, 1723368625),  # 8  2024 11
    (7474146579, 1723714225),  # 8  2024 15
    (7315147059, 1723973425),  # 8  2024 18
    (7512836127, 1724059825),  # 8  2024 19
    (6608978740, 1724146225),  # 8  2024 20
    (7444261673, 1724232625),  # 8  2024 21
    (7411478331, 1724405425),  # 8  2024 23
    (7402508588, 1724491825),  # 8  2024 24
    (7414499762, 1724578225),  # 8  2024 25
    (7231775745, 1724664625),  # 8  2024 26
    (7229301933, 1724837425),  # 8  2024 28
    (6794448699, 1725010225),  # 8  2024 30
    (7203459553, 1725232381),  # 9  2024
    (6545617682, 1725269425),  # 9  2024 2
    (7511370964, 1725316225),  # 9  2024 2 10.30
    (6940209565, 1725355825),  # 9  2024 3
    (7541738425, 1725402625),  # 9  2024 3 10.30
    (7493020995, 1725442225),  # 9  2024 4
    (7485102747, 1725528625),  # 9  2024 5
    (7348142395, 1725615025),  # 9  2024 6
    (7178009771, 1726133425),  # 9  2024 12
    (6653854045, 1726306225),  # 9  2024 14
    (6703727009, 1726392625),  # 9  2024 15
    (6576065294, 1726479025),  # 9  2024 16
    (7478453904, 1726525825),  # 9  2024 16 10.30 
    (7586525467, 1726651825),  # 9  2024 18
    (7510138690, 1726824625),  # 9  2024 20
    (7853061461, 1726911025),  # 9  2024 21
    (7287359358, 1726997425),  # 9  2024 22
    (8183576458, 1727083825),  # 9  2024 23
    (7701496013, 1727170225),  # 9  2024 24
    (7557898908, 1727688625),  # 9  2024 30
    (7255764154, 1727824381),  # 10 2024
    (7924226527, 1728034225),  # 10 2024 4
    (7966808949, 1728120625),  # 10 2024 5
    (8132423567, 1728293425),  # 10 2024 7
    (7915398097, 1728466225),  # 10 2024 9
    (7780534407, 1728552625),  # 10 2024 10
    (7921621269, 1728639025),  # 10 2024 11
    (7668356723, 1728811825),  # 10 2024 13
    (7820874598, 1728898225),  # 10 2024 14
    (7983427001, 1728984625),  # 10 2024 15
    (7720177224, 1729071025),  # 10 2024 16
    (7635774948, 1729157425),  # 10 2024 17
    (7771495833, 1729243825),  # 10 2024 18
    (7693806755, 1729330225),  # 10 2024 19
    (7813422471, 1729377025),  # 10 2024 19 10.30
    (7791771117, 1729416625),  # 10 2024 20
    (7900704280, 1729935025),  # 10 2024 26
    (7528958050, 1730107825),  # 10 2024 28
    (7817865983, 1730194225),  # 10 2024 29
    (7895564585, 1730367025),  # 10 2024 31
    (7782117193, 1730502781),  # 11 2024
    (7565970320, 1730539825),  # 11 2024 2
    (7981934264, 1730712625),  # 11 2024 4
    (8017342447, 1730799025),  # 11 2024 5
    (8126813714, 1730971825),  # 11 2024 7
    (7576051897, 1731058225),  # 11 2024 8
    (8196220219, 1731144625),  # 11 2024 9
    (7867322996, 1731231025),  # 11 2024 10
    (7994807689, 1731490225),  # 11 2024 13
    (7569498646, 1731576625),  # 11 2024 14
    (8051030718, 1731922225),  # 11 2024 18
    (7609944593, 1732095025),  # 11 2024 20
    (8060458027, 1732181425),  # 11 2024 21
    (7590457186, 1732354225),  # 11 2024 23
    (7785013699, 1732440625),  # 11 2024 24
    (7237053111, 1732527025),  # 11 2024 25
    (8191970479, 1732573825),  # 11 2024 25 10.30
    (7897827485, 1732699825),  # 11 2024 27
    (7995150295, 1732786225),  # 11 2024 28
    (7908652201, 1732872625),  # 11 2024 29
    (7707720342, 1733094781),  # 12 2024 2
    (7506650524, 1733218225),  # 12 2024 3
    (7821648301, 1733265025),  # 12 2024 3 10.30
    (7648567986, 1733563825),  # 12 2024 7
    (7862573238, 1733610625),  # 12 2024 7 10.30
    (7884539906, 1733736625),  # 12 2024 9
    (7940228571, 1733909425),  # 12 2024 11
    (7662198972, 1734082225),  # 12 2024 13
    (8124574038, 1734255025),  # 12 2024 15
    (7901287916, 1734600625),  # 12 2024 19
    (7848788808, 1734687025),  # 12 2024 20
    (8154656493, 1734773425),  # 12 2024 21
    (7273322210, 1734946225),  # 12 2024 23
    (7771578373, 1735291825),  # 12 2024 27
    (7832835741, 1735378225),  # 12 2024 28
    (7851697095, 1735551025),  # 12 2024 30
    (7831357206, 1735637425),  # 12 2024 31
    (7995455522, 1735765164),  # 1  2025
    (7287093425, 1736069425),  # 1  2025 5
    (7803070045, 1736155825),  # 1  2025 6
    (8099528362, 1736760625),  # 1  2025 13
    (7091404087, 1737106225),  # 1  2025 17
    (7799438607, 1737192625),  # 1  2025 18
    (8118041971, 1737279025),  # 1  2025 19
    (8051743665, 1737325825),  # 1  2025 19 10.30
    (7294739924, 1737365425),  # 1  2025 20
    (7616688371, 1737451825),  # 1  2025 21
    (7806616092, 1737624625),  # 1  2025 23
    (7655790974, 1737883825),  # 1  2025 26
    (8171233804, 1737912625),  # 1  2025 26 5.30
    (7948632604, 1737970225),  # 1  2025 27
    (7918805287, 1738056625),  # 1  2025 28
    (7680194561, 1738143025),  # 1  2025 29
    (7964370951, 1738229425),  # 1  2025 30
    (7581001954, 1738472065),  # 2  2025 2
]

def predict_creation_date(id: int):
    entries.sort(key=lambda x: x[0])
    for i in range(1, len(entries)):
        if entries[i - 1][0] <= id <= entries[i][0]:
            t = (id - entries[i - 1][0]) / (entries[i][0] - entries[i - 1][0])
            reg_time = int(entries[i - 1][1] + t * (entries[i][1] - entries[i - 1][1]))
            return parse_registration_time(reg_time)            
    if id <= 1000000:
        return parse_registration_time(1380326400)
    else:
        return parse_registration_time(1738472065)



class InvalidFormatException(Exception):
    pass


class CustomParseMode:
    """
    Example using Markdown:

    - client.send_message('me', 'hello this is a [Text](spoiler), with custom emoji [❤️](emoji/10002345) !')

    Example using HTML:

    - client.send_message('me', 'hello this is a <a href="spoiler">Text</a>, with custom emoji <a href="emoji/10002345">❤️</a> !')

    `Sending spoilers and custom emoji <https://github.com/LonamiWebs/Telethon/wiki/Sending-more-than-just-messages#sending-spoilers-and-custom-emoji>`_
    :param parse_mode: The format to use for parsing text.
                       Can be either 'markdown' for Markdown formatting
                       or 'html' for HTML formatting.
    """
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'markdown':
            text, entities = markdown.parse(text)
        elif self.parse_mode == 'html':
            text, entities = html.parse(text)
        else:
            raise InvalidFormatException("Invalid parse mode. Choose either Markdown or HTML.")

        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, int(e.url.split('/')[1]))
        return text, entities

    @staticmethod
    def unparse(text, entities):
        for i, e in enumerate(entities or []):
            if isinstance(e, types.MessageEntityCustomEmoji):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, f'emoji/{e.document_id}')
            if isinstance(e, types.MessageEntitySpoiler):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, 'spoiler')
        return html.unparse(text, entities)


async def get_chatinfo(event, revent):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await revent.edit("**⎉ لـم يتـمّ العثـور على القنـاة/المجموعـة ✕**")
            return None
        except ChannelPrivateError:
            await revent.edit(
                "**⎉ هـذه مجموعـة أو قنـاة خاصـة أو لقد تمّ حظـري منه ⛞**"
            )
            return None
        except ChannelPublicGroupNaError:
            await revent.edit("**⎉ القنـاة أو المجموعـة الخارقـة غيـر موجـودة ✕**")
            return None
        except (TypeError, ValueError) as err:
            LOGS.info(err)
            await edit_delete(revent, "**⎉ لم يتم العثور على المجموعة او القناة**")
            return None
    return chat_info


async def fetched_info(chat, event):  # sourcery no-metrics
    # chat.chats is a list so we use get_entity() to avoid IndexError
    chat_obj_info = await event.client.get_entity(chat.full_chat.id)
    broadcast = (
        chat_obj_info.broadcast if hasattr(chat_obj_info, "broadcast") else False
    )
    chat_type = "القنـاة" if broadcast else "المجمـوعـة"
    chat_typp = "قنـاة" if broadcast else "مجمـوعـة"
    chat_title = chat_obj_info.title
    try:
        msg_info = await event.client(
            GetHistoryRequest(
                peer=chat_obj_info.id,
                offset_id=0,
                offset_date=datetime(2010, 1, 1),
                add_offset=-1,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as e:
        msg_info = None
        LOGS.error(f"Exception: {e}")
    # No chance for IndexError as it checks for msg_info.messages first
    first_msg_valid = bool(
        msg_info and msg_info.messages and msg_info.messages[0].id == 1
    )
    # Same for msg_info.users
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and isinstance(msg_info.messages[0].action, MessageActionChannelMigrateFrom)
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    supergroup = (
        "<b>خارقـه</b>"
        if hasattr(chat_obj_info, "megagroup") and chat_obj_info.megagroup
        else "ليست خارقـه"
    )
    username = "@{}".format(username) if username else None

    caption = f'<a href="t.me/Repthon">ᯓ 𝗥𝗲𝗽𝘁𝗵𝗼𝗻 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗗𝗮𝘁𝗮 📟</a>'
    caption += f"\n<b>⋆─┄─┄─┄─┄─┄┄─┄┄─┄─⋆</b>\n"
    caption += f"<b>● معلومـات إنشـاء {chat_type} 📑:</b>\n"
    if chat_title is not None:
        caption += f"<b>• الاسـم   ⤎</b> {chat_title}\n"
    if former_title is not None:  # Meant is the very first title
        caption += f"<b>• الإسم السابـق ⤎</b>  {former_title}\n"
    caption += f"<b>• الآيـدي  ⤎</b> <code>{chat_obj_info.id}</code>\n"
    if username is not None:
        caption += f"<b>• اليـوزر  ⤎</b>  \n {username}\n"
        if not broadcast:
            caption += f"<b>• النـوع   ⤎</b> {chat_typp} عامّـة - {supergroup}\n"
        else:
            caption += f"<b>• النـوع   ⤎</b> {chat_typp} عامّـة\n"
    else:
        if not broadcast:
            caption += f"<b>• النـوع   ⤎</b> {chat_typp} خاصـه - {supergroup}\n"
        else:
            caption += f"<b>• النـوع   ⤎</b> {chat_typp} خاصـه\n"
    if created is not None:
        caption += f"<b>• تاريـخ الإنشـاء  ⤎</b> <code>{created.date().strftime('%b %d, %Y')}</code> 🗓"
    else:
        #caption += f"<b>• الإنتـاج ⤎</b> <code>{chat_obj_info.date.date().strftime('%b %d, %Y')}</code> {warn_emoji}"
        caption += f"<b>• تاريـخ الإنشـاء  ⤎</b> <code>غير معروف</code> ✖️"
    return caption


@zq_lo.rep_cmd(
    pattern="انشاء(?:\s|$)([\s\S]*)",
    command=("انشاء", plugin_category),
    info={
        "header": "To get Group information.",
        "description": "Shows you the total information of the required chat.",
        "usage": [
            "{tr}انشاء <username/userid>",
            "{tr}انشاء <in group where you need>",
        ],
        "examples": "{tr}انشاء + معرف او رابط المجموعه",
    },
)
async def ch_info(event):
    "To get group information"
    revent = await edit_or_reply(event, "**⎉ جـارِ جلـب معلومـات الدردشـة، إنتظـر ⅏**")
    chat = await get_chatinfo(event, revent)
    if chat is None:
        return
    caption = await fetched_info(chat, event)
    try:
        await revent.edit(caption, parse_mode="html")
    except Exception as e:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, f"**⎉ هنـاك خطـأ في معلومـات الدردشـة ✕ : **\n`{str(e)}`"
            )

        await revent.edit("**⎉ حـدث خـطأ مـا، يرجـى التحقق من الأمـر ⎌**")


async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object


async def get_creation_date(user_id):
    url = "https://restore-access.indream.app/regdate"
    headers = {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Nicegram/92 CFNetwork/1390 Darwin/22.0.0",
        "x-api-key": "e758fb28-79be-4d1c-af6b-066633ded128",
        "accept-language": "en-US,en;q=0.9",
    }
    data = {"telegramId": user_id}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                json_response = await response.json()
                return json_response["data"]["date"]
            else:
                return "unknown"


async def rrr_info(repthon_user, event):
    FullUser = (await event.client(GetFullUserRequest(zthon_user.id))).full_user
    first_name = repthon_user.first_name
    full_name = FullUser.private_forward_name
    user_id = repthon_user.id
    b_sinc = "error"
    try:
        b_sinc = predict_creation_date(user_id)
        #b_sinc = await get_creation_date(user_id)
    except Exception:
        b_sinc = "unknown"
    username = repthon_user.username
    verified = repthon_user.verified
    b = (await event.client.get_entity(user_id)).premium
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("هذا المستخدم ليس له اسم أول")
    )
    full_name = full_name or first_name
    username = "@{}".format(username) if username else ("لا يـوجـد")
    rrrsinc = b_sinc if b_sinc else ("غيـر معلـوم")
    mypremium = (await event.client.get_entity(Rep_Uid)).premium
    emoji_id = None
    if (b == True and mypremium == True):
        emoji_status = (await event.client.get_entity(user_id)).emoji_status
        if isinstance(emoji_status, EmojiStatusEmpty): 
            emoji_id = 5834880210268329130
        else:
            try:
                emoji_id = emoji_status.document_id
                if emoji_id is None:
                    emoji_id = 5834880210268329130
            except Exception:
                    emoji_id = 5834880210268329130
    if mypremium == True:
        ################# Dev Baqir #################
        Repthon = f'<a href="t.me/Repthon">ᯓ 𝗥𝗲𝗽𝘁𝗵𝗼𝗻 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗗𝗮𝘁𝗮</a>.'
        Repthon += f'<a href="emoji/5832391341144805776">❤️</a>\n'
        Repthon += f"<b>⋆─┄─┄─┄─┄─┄┄─┄┄─┄─⋆</b>\n"
        Repthon += f"<b>● معلومـات إنشـاء حسـاب تيليجـرام </b>"
        Repthon += f'<a href="emoji/5832334750655715478">❤️</a>:\n'
        Repthon += f"<b>- الاسـم    ⤎  </b> "
        Repthon += f'<a href="tg://user?id={user_id}">{full_name}</a> '
        if b == True:
            Repthon += f'<a href="t.me/Repthon">"emoji/{emoji_id}">❤️</a>'
        Repthon += f"\n<b>- الايــدي  ⤎ </b> <code>{user_id}</code>"
        Repthon += f"\n<b>- اليـوزر    ⤎  {username}</b>\n"
        if b == True:
            Repthon += f"<b>- الحساب ⤎  بـريميـوم</b>"
            Repthon += f'<a href="emoji/5832422209074762334">❤️</a>\n'
        Repthon += f"<b>- الإنشـاء  ⤎</b>  {rrrsinc}  " 
        Repthon += f'<a href="emoji/5472026645659401564">❤️</a>'
        return Repthon
    else:
        ################# Dev Baqir #################
        Repthon = f'<a href="t.me/Repthon">ᯓ 𝗥𝗲𝗽𝘁𝗵𝗼𝗻 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗗𝗮𝘁𝗮 📟</a>'
        Repthon += f"\n<b>⋆─┄─┄─┄─┄─┄┄─┄┄─┄─⋆</b>\n"
        Repthon += f"<b>● معلومـات إنشـاء حسـاب تيليجـرام 📑:</b>\n"
        Repthon += f"<b>- الاسـم    ⤎  </b> "
        Repthon += f'<a href="tg://user?id={user_id}">{full_name}</a>'
        Repthon += f"\n<b>- الايــدي  ⤎ </b> <code>{user_id}</code>"
        Repthon += f"\n<b>- اليـوزر    ⤎  {username}</b>\n"
        if b == True:
            Repthon += f"<b>- الحساب ⤎  بـريميـوم 🌟</b>\n"
        Repthon += f"<b>- الإنشـاء  ⤎</b>  {rrrsinc}  🗓" 
        return Repthon

async def fetch_info(replied_user, event):
    """Get details from the User object."""
    FullUser = (await event.client(GetFullUserRequest(replied_user.id))).full_user
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(user_id=replied_user.id, offset=42, max_id=0, limit=80)
    )
    replied_user_profile_photos_count = "لا يـوجـد بروفـايـل"
    dc_id = "Can't get dc id"
    with contextlib.suppress(AttributeError):
        replied_user_profile_photos_count = replied_user_profile_photos.count
        dc_id = replied_user.photo.dc_id
    user_id = replied_user.id
    b_sinc = "error"
    try:
        b_sinc = predict_creation_date(user_id)
        #b_sinc = await get_creation_date(user_id)
    except Exception:
        b_sinc = "unknown"
    first_name = replied_user.first_name
    last_name = replied_user.last_name
    full_name = f"{first_name} {last_name}" if last_name else first_name
    common_chat = FullUser.common_chats_count
    username = replied_user.username
    user_bio = FullUser.about
    is_bot = replied_user.bot
    restricted = replied_user.restricted
    verified = replied_user.verified
    b = (await event.client.get_entity(user_id)).premium
    mypremium = (await event.client.get_entity(Rep_Uid)).premium
    #r = int(gvarstatus("Repthon_Vip"))
    if b == True or user_id in dev_baqir:
        rpre = "ℙℝ𝔼𝕄𝕀𝕌𝕄 🌟"
    else:
        rpre = "𝕍𝕀ℝ𝕋𝕌𝔸𝕃 ✨"
    if (b == True and mypremium == True):
        emoji_status = (await event.client.get_entity(user_id)).emoji_status
        if isinstance(emoji_status, EmojiStatusEmpty): 
            emoji_id = 5834880210268329130
        else:
            try:
                emoji_id = emoji_status.document_id
                if emoji_id is None:
                    emoji_id = 5834880210268329130
            except Exception:
                    emoji_id = 5834880210268329130
    photo = await event.client.download_profile_photo(
        user_id,
        Config.TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg",
        download_big=True,
    )
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("هذا المستخدم ليس له اسم أول")
    )
    #full_name = full_name or first_name
    username = "@{}".format(username) if username else ("لا يـوجـد")
    user_bio = "لا يـوجـد" if not user_bio else user_bio
    rrrsinc = b_sinc if b_sinc else ("غيـر معلـوم")
    rmsg = await bot.get_messages(event.chat_id, 0, from_user=user_id) 
    rrr = rmsg.total
    if rrr < 100: 
        ba = "غير متفاعل  🗿"
    elif rrr > 200 and rrr < 500:
        ba = "ضعيف  🗿"
    elif rrr > 500 and rrr < 700:
        ba = "شد حيلك  🏇"
    elif rrr > 700 and rrr < 1000:
        ba = "ماشي الحال  🏄🏻‍♂"
    elif rrr > 1000 and rrr < 2000:
        ba = "ملك التفاعل  🎖"
    elif rrr > 2000 and rrr < 3000:
        ba = "امبراطور التفاعل  🥇"
    elif rrr > 3000 and rrr < 4000:
        ba = "غنبله  💣"
    else:
        ba = "نار وشرر  🏆"
################# Dev Baqir #################
    if user_id in dev_baqir:
        rotbat = "مطـور السـورس 𓄂" 
    elif user_id == (await event.client.get_me()).id:
        rotbat = "مـالك الحساب 𓀫" 
    else:
        rotbat = "العضـو 𓅫"
################# Dev Baqir #################
    #r = int(gvarstatus("Repthon_Vip"))
    REP_TEXT = gvarstatus("CUSTOM_ALIVE_TEXT") or "•⎚• مـعلومـات المسـتخـدم من سـورس ريبـثون"  
    REPM = gvarstatus("CUSTOM_ALIVE_EMOJI") or "✦ " 
    REPF = gvarstatus("CUSTOM_ALIVE_FONT") or "⋆─┄─┄─┄─ ᴿᴱᴾᵀᴴᴼᴺ ─┄─┄─┄─⋆" 
    if gvarstatus("RID_TEMPLATE") is None:
        if mypremium == True:
            caption = f"<b>✦ مـعلومـات المسـتخـدم من سـورس ريبـثون</b>"
            caption += f'<a href="emoji/5424605254614262924">❤️</a>\n'
            caption += f"ٴ<b>⋆┄─┄─┄─┄─</b>"
            caption += f'<a href="emoji/6309672657109393000">❤️</a>'
            caption += f"<b>─┄─┄─┄─┄⋆</b>\n"
            caption += f"<b>{REPM}الاســم    ⤎ </b> "
            caption += f'<a href="tg://user?id={user_id}">{full_name}</a> '
            if b == True:
                caption += f'<a href="emoji/{emoji_id}">❤️</a>'
            caption += f"\n<b>{REPM}اليـوزر    ⤎  {username}</b>"
            caption += f"\n<b>{REPM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
            caption += f"<b>{REPM}الرتبــه    ⤎  {rotbat} </b>\n"
            if b == True:
                caption += f"<b>{REPM}الحساب  ⤎  بـريميـوم</b>"
                caption += f'<a href="emoji/5832422209074762334">❤️</a>\n'
            caption += f"<b>{REPM}الصـور    ⤎</b>  {replied_user_profile_photos_count}\n"
            caption += f"<b>{REPM}الرسائل  ⤎</b>  {rrr} "
            caption += f'<a href="emoji/5253742260054409879">❤️</a>\n'
            caption += f"<b>{REPM}التفاعل  ⤎</b>  {ba}\n" 
            if user_id != (await event.client.get_me()).id: 
                caption += f"<b>{REPM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
            caption += f"<b>{REPM}الإنشـاء  ⤎</b>  {rrrsinc}  " 
            caption += f'<a href="emoji/5472026645659401564">❤️</a>\n'
            caption += f"<b>{REPM}البايـو     ⤎  {user_bio}</b>\n"
            caption += f"ٴ<b>⋆┄─┄─┄─┄─</b>"
            caption += f'<a href="emoji/6309672657109393000">❤️</a>'
            caption += f"<b>─┄─┄─┄─┄⋆</b>\n"
        else:
            caption = f"<b> {REP_TEXT} </b>\n"
            caption += f"ٴ<b>{REPF}</b>\n"
            caption += f"<b>{REPM}الاســم    ⤎ </b> "
            caption += f'<a href="tg://user?id={user_id}">{full_name}</a>'
            caption += f"\n<b>{REPM}اليـوزر    ⤎  {username}</b>"
            caption += f"\n<b>{REPM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
            caption += f"<b>{REPM}الرتبــه    ⤎  {rotbat} </b>\n"
            if b == True:
                caption += f"<b>{REPM}الحساب  ⤎  بـريميـوم 🌟</b>\n"
            caption += f"<b>{REPM}الصـور    ⤎</b>  {replied_user_profile_photos_count}\n"
            caption += f"<b>{REPM}الرسائل  ⤎</b>  {rrr}  💌\n"
            caption += f"<b>{REPM}التفاعل  ⤎</b>  {ba}\n" 
            if user_id != (await event.client.get_me()).id: 
                caption += f"<b>{REPM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
            caption += f"<b>{REPM}الإنشـاء  ⤎</b>  {rrrsinc}  🗓\n" 
            caption += f"<b>{REPM}البايـو     ⤎  {user_bio}</b>\n"
            caption += f"ٴ<b>{REPF}</b>"
    else:
        rrr_caption = gvarstatus("RID_TEMPLATE")
        caption = rrr_caption.format(
            rnam=full_name,
            rusr=username,
            ridd=user_id,
            rrtb=rotbat,
            rpre=rpre,
            rvip=rvip,
            rpic=replied_user_profile_photos_count,
            rmsg=rrr,
            rtmg=ba,
            rcom=common_chat,
            rsnc=rrrsinc,
            rbio=user_bio,
        )
    return photo, caption


@zq_lo.rep_cmd(
    pattern="ايدي(?: |$)(.*)",
    command=("ايدي", plugin_category),
    info={
        "header": "لـ عـرض معلومـات الشخـص",
        "الاستـخـدام": " {tr}ايدي بالـرد او {tr}ايدي + معـرف/ايـدي الشخص",
    },
)
async def who(event):
    "Gets info of an user"
    #if gvarstatus("Repthon_Vip") is not None or Rep_Uid in Rep_Dev:
        #input_str = event.pattern_match.group(1)
        #reply = event.reply_to_msg_id
        #if not input_str and not reply:
            #return
    if (event.chat_id in REP_BLACKLIST) and (Rep_Uid not in Rep_Dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫\n- فـي مجموعـة استفسـارات زدثــون ؟!**")
    rep = await edit_or_reply(event, "⇆")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    replied_user = await get_user_from_event(event)
    try:
        photo, caption = await fetch_info(replied_user, event)
    #except (AttributeError, TypeError):
        #return await edit_or_reply(rep, "**- لـم استطـع العثــور ع الشخــص ؟!**")
    except AttributeError as e:
        return await edit_or_reply(rep, str(e))
    except TypeError as e:
        return await edit_or_reply(rep, str(e))
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if gvarstatus("RID_TEMPLATE") is None:
        #event.client.parse_mode = CustomParseMode('html')  # TODO: Choose parsemode
        try:
            await event.client.send_file(
                event.chat_id,
                photo,
                caption=caption,
                link_preview=False,
                force_document=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("html"),
            )
            if not photo.startswith("http"):
                os.remove(photo)
            await rep.delete()
        except ChatSendMediaForbiddenError:
            #await rep.edit(caption, parse_mode=CustomParseMode("html"))
            await event.client.send_message(
                event.chat_id,
                caption,
                link_preview=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("html"),
            )
            await rep.delete()
        except Exception:
            await event.client.send_message(
                event.chat_id,
                caption,
                link_preview=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("html"),
            )
            return await rep.delete()
    else:
        #event.client.parse_mode = CustomParseMode('markdown')  # TODO: Choose parsemode
        try:
            await event.client.send_file(
                event.chat_id,
                photo,
                caption=caption,
                link_preview=False,
                force_document=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("markdown"),
            )
            if not photo.startswith("http"):
                os.remove(photo)
            await rep.delete()
        except ChatSendMediaForbiddenError:
            #await rep.edit(caption, parse_mode=CustomParseMode("markdown"))
            await event.client.send_message(
                event.chat_id,
                caption,
                link_preview=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("markdown"),
            )
            await rep.delete()
        except Exception:
            await event.client.send_message(
                event.chat_id,
                caption,
                link_preview=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("markdown"),
            )
            return await rep.delete()

""""
@zedub.zed_cmd(
    pattern="ا(?: |$)(.*)",
    command=("ا", plugin_category),
    info={
        "header": "امـر مختصـر لـ عـرض معلومـات الشخـص",
        "الاستـخـدام": " {tr}ا بالـرد او {tr}ا + معـرف/ايـدي الشخص",
    },
)
async def who(event):
    "Gets info of an user"
    #if gvarstatus("ZThon_Vip") is not None or Zel_Uid in Zed_Dev:
        #input_str = event.pattern_match.group(1)
        #reply = event.reply_to_msg_id
        #if not input_str and not reply:
            #return
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in Zed_Dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫\n- فـي مجموعـة استفسـارات زدثــون ؟!**")
    zed = await edit_or_reply(event, "⇆")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    replied_user = await get_user_from_event(event)
    try:
        photo, caption = await fetch_info(replied_user, event)
    except (AttributeError, TypeError):
        return await edit_or_reply(zed, "**- لـم استطـع العثــور ع الشخــص ؟!**")
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if gvarstatus("ZID_TEMPLATE") is None:
        #event.client.parse_mode = CustomParseMode('html')  # TODO: Choose parsemode
        try:
            await event.client.send_file(
                event.chat_id,
                photo,
                caption=caption,
                link_preview=False,
                force_document=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("html"),
            )
            if not photo.startswith("http"):
                os.remove(photo)
            await zed.delete()
        except ChatSendMediaForbiddenError:
            #await zed.edit(caption, parse_mode=CustomParseMode("html"))
            await event.client.send_message(
                event.chat_id,
                caption,
                link_preview=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("html"),
            )
            await zed.delete()
        except Exception:
            await event.client.send_message(
                event.chat_id,
                caption,
                link_preview=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("html"),
            )
            return await zed.delete()
    else:
        #event.client.parse_mode = CustomParseMode('markdown')  # TODO: Choose parsemode
        try:
            await event.client.send_file(
                event.chat_id,
                photo,
                caption=caption,
                link_preview=False,
                force_document=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("markdown"),
            )
            if not photo.startswith("http"):
                os.remove(photo)
            await zed.delete()
        except ChatSendMediaForbiddenError:
            #await zed.edit(caption, parse_mode=CustomParseMode("markdown"))
            await event.client.send_message(
                event.chat_id,
                caption,
                link_preview=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("markdown"),
            )
            await zed.delete()
        except Exception:
            await event.client.send_message(
                event.chat_id,
                caption,
                link_preview=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("markdown"),
            )
            return await zed.delete()


@zedub.zed_cmd(pattern="الانشاء(?: |$)(.*)")
async def zelzalll(event):
    zed = await edit_or_reply(event, "**- جـارِ جلب المعلومـات . . .**")
    zthon_user = await get_user_from_event(event)
    try:
        ZThon = await zzz_info(zthon_user, event)
    except (AttributeError, TypeError):
        return await edit_or_reply(zed, "**- لـم استطـع العثــور ع الشخــص ؟!**")
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    #zedub.parse_mode = CustomParseMode('html')  # TODO: Choose parsemode
    mypremium = (await event.client.get_entity(Zel_Uid)).premium
    if mypremium == True:
        try:
            await event.client.send_message(
                event.chat_id,
                ZThon,
                link_preview=False,
                reply_to=message_id_to_reply,
                parse_mode=CustomParseMode("html"),
            )
            await zed.delete()
        except Exception:
            await zed.edit("**- غيـر معلـوم او هنـاك خطـأ ؟!**", parse_mode="html")
    else:
        try:
            await event.client.send_message(
                event.chat_id,
                ZThon,
                link_preview=False,
                reply_to=message_id_to_reply,
                parse_mode="html",
            )
            await zed.delete()
        except Exception:
            await zed.edit("**- غيـر معلـوم او هنـاك خطـأ ؟!**", parse_mode="html")


@zedub.zed_cmd(pattern=f"{ZIDA}(?: |$)(.*)")
async def hwo(event):
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in Zed_Vip):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫\n- فـي مجموعـة استفسـارات زدثــون ؟!**")
    zed = await edit_or_reply(event, "⇆")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    replied_user = await get_user_from_event(event)
    try:
        photo, caption = await fetch_info(replied_user, event)
    except (AttributeError, TypeError):
        return await edit_or_reply(zed, "**- لـم استطـع العثــور ع الشخــص ؟!**")
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    try:
        await event.client.send_file(
            event.chat_id,
            photo,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )
        if not photo.startswith("http"):
            os.remove(photo)
        await zed.delete()
    except TypeError:
        await zed.edit(caption, parse_mode="html")


@zedub.zed_cmd(
    pattern="صورته(?:\\s|$)([\\s\\S]*)",
    command=("صورته", plugin_category),
    info={
        "header": "لـ جـلب بـروفـايـلات الشخـص",
        "الاستـخـدام": [
            "{tr}صورته + عدد",
            "{tr}صورته الكل",
            "{tr}صورته",
        ],
    },
)
async def potocmd(event):
    "To get user or group profile pic"
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in Zed_Vip):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫\n- فـي مجموعـة استفسـارات زدثــون ؟!**")
    uid = "".join(event.raw_text.split(maxsplit=1)[1:])
    user = await event.get_reply_message()
    chat = event.input_chat
    if user and user.sender:
        photos = await event.client.get_profile_photos(user.sender)
        u = True
    else:
        photos = await event.client.get_profile_photos(chat)
        u = False
    if uid.strip() == "":
        uid = 1
        if int(uid) > (len(photos)):
            return await edit_delete(
                event, "**- لا يـوجـد هنـاك صـور لهـذا الشخـص ؟! **"
            )
        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    elif uid.strip() == "الكل":
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
        else:
            try:
                if u:
                    photo = await event.client.download_profile_photo(user.sender)
                else:
                    photo = await event.client.download_profile_photo(event.input_chat)
                await event.client.send_file(event.chat_id, photo)
            except Exception:
                return await edit_delete(event, "**- لا يـوجـد هنـاك صـور لهـذا الشخـص ؟! **")
    else:
        try:
            uid = int(uid)
            if uid <= 0:
                await edit_or_reply(
                    event, "**- رقـم خـاطـئ . . .**"
                )
                return
        except BaseException:
            await edit_or_reply(event, "**- رقـم خـاطـئ . . .**")
            return
        if int(uid) > (len(photos)):
            return await edit_delete(
                event, "**- لا يـوجـد هنـاك صـور لهـذا الشخـص ؟! **"
            )

        send_photos = await event.client.download_media(photos[uid - 1])
        await event.client.send_file(event.chat_id, send_photos)
    await event.delete()


@zedub.zed_cmd(
    pattern="(الايدي|id)(?:\\s|$)([\\s\\S]*)",
    command=("id", plugin_category),
    info={
        "header": "To get id of the group or user.",
        "description": "if given input then shows id of that given chat/channel/user else if you reply to user then shows id of the replied user \
    along with current chat id and if not replied to user or given input then just show id of the chat where you used the command",
        "usage": "{tr}id <reply/username>",
    },
)
async def _(event):
    "To get id of the group or user."
    if input_str := event.pattern_match.group(2):
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{e}`", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"**⎉ ايـدي المستخـدم**  `{input_str}` **هـو** `{p.id}`"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"**⎉ ايـدي المستخـدم**  `{p.title}` **هـو** `{p.id}`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "**⎉ أدخل إما اسم مستخدم أو الرد على المستخدم**")
    elif event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                f"**⎉ ايـدي الدردشـه : **`{event.chat_id}`\n\n**⎉ ايـدي المستخـدم : **`{r_msg.sender_id}`\n\n**⎉ ايـدي الميديـا : **`{bot_api_file_id}`",
            )

        else:
            await edit_or_reply(
                event,
                f"**⎉ ايـدي الدردشـه : **`{event.chat_id}`\n\n**⎉ ايـدي المستخـدم : **`{r_msg.sender_id}`",
            )

    else:
        await edit_or_reply(event, f"**⎉ ايـدي الدردشـه : **`{event.chat_id}`")


@zedub.zed_cmd(
    pattern="رابطه(?:\\s|$)([\\s\\S]*)",
    command=("رابطه", plugin_category),
    info={
        "header": "لـ جـلب اسـم الشخـص بشكـل ماركـدون ⦇.رابطه بالـرد او + معـرف/ايـدي الشخص⦈ ",
        "الاسـتخـدام": "{tr}رابطه <username/userid/reply>",
    },
)
async def permalink(event):
    Generates a link to the user's PM with a custom text.
    user, custom = await get_user_from_event(event)
    if not user:
        return
    if custom:
        return await edit_or_reply(event, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(event, f"[{tag}](tg://user?id={user.id})")


@zedub.zed_cmd(pattern="اسمي$")
async def permalink(event):
    user = await event.client.get_me()
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(event, f"[{tag}](tg://user?id={user.id})")


@zedub.zed_cmd(
    pattern="اسمه(?:\\s|$)([\\s\\S]*)",
    command=("اسمه", plugin_category),
    info={
        "header": "لـ جـلب اسـم الشخـص بشكـل ماركـدون ⦇.اسمه بالـرد او + معـرف/ايـدي الشخص⦈ ",
        "الاسـتخـدام": "{tr}اسمه <username/userid/reply>",
    },
)
async def permalink(event):
    Generates a link to the user's PM with a custom text.
    user, custom = await get_user_from_event(event)
    if not user:
        return
    if custom:
        return await edit_or_reply(event, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(event, f"[{tag}](tg://user?id={user.id})")


@zedub.zed_cmd(pattern="الصور(?:\\s|$)([\\s\\S]*)")
async def potocmd(event):
    uid = "".join(event.raw_text.split(maxsplit=1)[1:])
    user = await get_user_from_event(event)
    rser = await event.get_reply_message()
    chat = event.input_chat
    if rser and ser.sender:
        photos = await event.client.get_profile_photos(rser.sender)
    else:
        photos = await event.client.get_profile_photos(user.id)
    if uid.strip() == "":
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
        else:
            try:
                if rser:
                    photo = await event.client.download_profile_photo(rser.sender)
                else:
                    photo = await event.client.download_profile_photo(event.input_chat)
                await event.client.send_file(event.chat_id, photo)
            except Exception:
                return await edit_delete(event, "**- لا يـوجـد هنـاك صـور لهـذا الشخـص ؟! **")
    else:
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
        else:
            try:
                photo = await event.client.download_profile_photo(user.id)
                await event.client.send_file(event.chat_id, photo)
            except Exception:
                return await edit_delete(event, "- لا يـوجـد هنـاك صـور لهـذا الشخـص ؟! ")
    await event.delete()


@zedub.zed_cmd(pattern="معنى(?: |$)(.*)")
async def get_name_meaning(event):
    nms = event.pattern_match.group(1)
    if not nms:
        return await edit_or_reply(event, "**- ارسـل (.معنى) + الاسـم**\n**- مثـال :**\n.معنى محمد")
    zzz = await edit_or_reply(event, "**⎉ جـارِ البحث عـن معنـى الاسـم ...**")
    url = "https://meaningnames.net/mean.php"
    headers = {
        'authority': 'meaningnames.net',
        'accept': '*/*',
        'referer': 'https://meaningnames.net/',
        'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
        'x-requested-with': 'XMLHttpRequest',
        'cookie': 'PHPSESSID=7uoau0rn3ud96s7nhc684aatf1',
    }
    if nms == "عائشه" or nms == "عائشة":
        caption=f"**- معنى اسم ( عائشة ) :**\nمعناه: الحياة، المأمولُ بطول عمرها، ذات الحياة، المرتاحة في حياتها...\nوهو اسم ام المؤمنين عائشة احب زوجات رسول الله (صلى الله عليه وسلم) اليه وابنة أبي بكر الصديق، وبها يتحبَّبون الناس تسمية بناتهم."
        return await edit_or_reply(event, caption)
    data = {'name': nms, 'ajax': 'TRUE'}
    response = requests.post(url, headers=headers, data=data).text
    try:
        ma = re.findall(r'<h3 style="line-height: 215%;">(.*?)<h3>', response)[0]
        photo = f"https://meaning-names.net/images-{nms}"
        caption=f"**- معنى اسم ( {nms} )** :\n{ma}"
        await edit_or_reply(event, caption)
    except:
        await zzz.edit("**- لم يتم العثـور على معنى الاسم ؟!\n- جرب الكتابة بدون اخطاء املائيـه**")


@zedub.zed_cmd(pattern="حساب(?: |$)(.*)")
async def openacc(event):
    acc = event.pattern_match.group(1)
    if not acc:
        return await edit_or_reply(event, "**- ارسـل الامـر والايـدي فقـط**")
    zzz = await edit_or_reply(event, "**⎉ جـارِ صنـع رابـط دخـول لـ الحسـاب ▬▭ ...**")
    caption=f"**- رابـط صاحب الايدي ( {acc} )** :\n**- الرابـط ينفتـح عبـر تطبيـق تيليكرام بلاس فقـط**\n\n[اضـغـط هـنـا](tg://openmessage?user_id={acc})"
    await edit_or_reply(event, caption)


@zedub.zed_cmd(pattern="اضف كليشة (الايدي|ايدي|الفحص|فحص|الحماية|الحمايه|الخاص) ?(.*)")
async def variable(event):
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    vinfo = reply.text
    zed = await edit_or_reply(event, "**⎉ جـاري اضـافة الكليشـة الـى بـوتك ...**")
    if input_str == "الايدي" or input_str == "ايدي":
        variable = "ZID_TEMPLATE"
        await asyncio.sleep(1.5)
        if gvarstatus("ZID_TEMPLATE") is None:
            await zed.edit("**⎉ تم تغييـر كليشـة {} بنجـاح ☑️**\n**⎉ الكليشـة الجـديده** \n {} \n\n**⎉ الان قـم بـ ارسـال الامـر ↶** `.ايدي` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**⎉ تم اضـافـة كليشـة {} بنجـاح ☑️**\n**⎉ الكليشـة المضـافه** \n {} \n\n**⎉ الان قـم بـ ارسـال الامـر ↶** `.ايدي` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("ZID_TEMPLATE", vinfo)
    elif input_str == "الفحص" or input_str == "فحص":
        variable = "ALIVE_TEMPLATE"
        await asyncio.sleep(1.5)
        if gvarstatus("ALIVE_TEMPLATE") is None:
            await zed.edit("**⎉ تم تغييـر كليشـة {} بنجـاح ☑️**\n**⎉ الكليشـة الجـديده** \n {} \n\n**⎉ الان قـم بـ ارسـال الامـر ↶** `.فحص` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**⎉ تم اضـافـة كليشـة {} بنجـاح ☑️**\n**⎉ الكليشـة المضـافه** \n {} \n\n**⎉ الان قـم بـ ارسـال الامـر ↶** `.فحص` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("ALIVE_TEMPLATE", vinfo)
    elif input_str == "الحماية" or input_str == "الحمايه" or input_str == "الخاص":
        variable = "pmpermit_txt"
        await asyncio.sleep(1.5)
        if gvarstatus("pmpermit_txt") is None:
            await zed.edit("**⎉ تم تغييـر كليشـة {} بنجـاح ☑️**\n**⎉ الكليشـة الجـديده** \n {} \n\n**⎉ الان قـم بـ ارسـال الامـر ↶** `.الحمايه تفعيل` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**⎉ تم اضـافـة كليشـة {} بنجـاح ☑️**\n**⎉ الكليشـة المضـافه** \n {} \n\n**⎉ الان قـم بـ ارسـال الامـر ↶** `.الحمايه تفعيل` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("pmpermit_txt", vinfo)
    else:
        if input_str:
            return await zed.edit("**⎉ عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))
        return await edit_or_reply(event, "**⎉ عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))


@zedub.zed_cmd(pattern="اضف كليشه (الايدي|ايدي|الفحص|فحص|الحماية|الحمايه|الخاص) ?(.*)")
async def variable(event):
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    vinfo = reply.text
    zed = await edit_or_reply(event, "**⎉ جـاري اضـافة الكليشـة الـى بـوتك ...**")
    if input_str == "الايدي" or input_str == "ايدي":
        variable = "ZID_TEMPLATE"
        await asyncio.sleep(1.5)
        if gvarstatus("ZID_TEMPLATE") is None:
            await zed.edit("**⎉ تم تغييـر كليشـة {} بنجـاح ☑️**\n**⎉ الكليشـة الجـديده** \n {} \n\n**⎉ الان قـم بـ ارسـال الامـر ↶** `.ايدي` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**⎉ تم اضـافـة كليشـة {} بنجـاح ☑️**\n**⎉ الكليشـة المضـافه** \n {} \n\n**⎉ الان قـم بـ ارسـال الامـر ↶** `.ايدي` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("ZID_TEMPLATE", vinfo)
    elif input_str == "الفحص" or input_str == "فحص":
        variable = "ALIVE_TEMPLATE"
        await asyncio.sleep(1.5)
        if gvarstatus("ALIVE_TEMPLATE") is None:
            await zed.edit("**⎉ تم تغييـر كليشـة {} بنجـاح ☑️**\n**⎉ الكليشـة الجـديده** \n {} \n\n**⎉ الان قـم بـ ارسـال الامـر ↶** `.فحص` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**⎉ تم اضـافـة كليشـة {} بنجـاح ☑️**\n**⎉ الكليشـة المضـافه** \n {} \n\n**⎉ الان قـم بـ ارسـال الامـر ↶** `.فحص` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("ALIVE_TEMPLATE", vinfo)
    elif input_str == "الحماية" or input_str == "الحمايه" or input_str == "الخاص":
        variable = "pmpermit_txt"
        await asyncio.sleep(1.5)
        if gvarstatus("pmpermit_txt") is None:
            await zed.edit("**⎉ تم تغييـر كليشـة {} بنجـاح ☑️**\n**⎉ الكليشـة الجـديده** \n {} \n\n**⎉ الان قـم بـ ارسـال الامـر ↶** `.الحمايه تفعيل` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**⎉ تم اضـافـة كليشـة {} بنجـاح ☑️**\n**⎉ الكليشـة المضـافه** \n {} \n\n**⎉ الان قـم بـ ارسـال الامـر ↶** `.الحمايه تفعيل` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("pmpermit_txt", vinfo)
    else:
        if input_str:
            return await zed.edit("**⎉ عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))
        return await edit_or_reply(event, "**⎉ عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))


@zedub.on(admin_cmd(pattern="(خط التشويش|خط تشويش|تفعيل تشويش|تفعيل التشويش)"))
async def _(event):
    is_cllear = gvarstatus("cllear")
    if not is_cllear:
        addgvar ("cllear", "on")
        await edit_delete(event, "**⎉ تم تفعيـل خـط التشـويش .. بنجـاح ✓**\n**⎉ لـ تعطيله اكتب (.تعطيل تشويش) **")
        return
    if is_cllear:
        await edit_delete(event, "**⎉ خـط التشـويش مغعـل .. مسبقـاً ✓**\n**⎉ لـ تعطيله اكتب (.تعطيل تشويش) **")
        return

@zedub.on(admin_cmd(pattern="(تعطيل تشويش|تعطيل التشويش)"))
async def _(event):
    is_cllear = gvarstatus("cllear")
    if is_cllear:
        delgvar("cllear")
        await edit_delete(event, "**⎉ تم تعطيـل خـط التشـويش .. بنجـاح ✓**\n**⎉ لـ تفعيله اكتب (.تفعيل تشويش) **")
        return
    if not is_cllear:
        await edit_delete(event, "**⎉ خـط التشـويش مغعـل .. مسبقـاً ✓**\n**⎉ لـ تفعيله اكتب (.تفعيل تشويش) **")
        return


@zedub.on(events.NewMessage(outgoing=True))
async def comming(event):
    if event.message.text and not event.message.media and "." not in event.message.text:
        is_cllear = gvarstatus("cllear")
        if is_cllear:
            try:
                await event.edit(f"[{event.message.text}](spoiler)", parse_mode=CustomParseMode("markdown"))
            except MessageIdInvalidError:
                pass"""
