import re

from telethon import Button
from telethon.events import CallbackQuery, InlineQuery

from jepthon import CMD_HELP, jepiq

# ๐ง๐ฒ๐น๐ฒ๐๐ฟ๐ฎ๐  : @Jepthon  ~ @lMl10l
from ..core.decorators import check_owner

CALC = {}

plugin_category = "utils"

m = [
    "AC",
    "C",
    "โซ",
    "%",
    "7",
    "8",
    "9",
    "+",
    "4",
    "5",
    "6",
    "-",
    "1",
    "2",
    "3",
    "x",
    "00",
    "0",
    ".",
    "รท",
]
tultd = [Button.inline(f"{x}", data=f"calc{x}") for x in m]
lst = list(zip(tultd[::4], tultd[1::4], tultd[2::4], tultd[3::4]))
lst.append([Button.inline("=", data="calc=")])


@jepiq.on(admin_cmd(pattern="ุญุงุณุจุฉ(?:\s|$)([\s\S]*)"))
async def icalc(e):
    if e.client._bot:
        return await e.reply(
            "**ุงูุญูุงุณุจุฉ ุงูุนููููุฉ ูุณููุฑุณ ุฃูุซูู\n @VV744**", buttons=lst
        )
    results = await e.client.inline_query(Config.TG_BOT_USERNAME, "calc")
    await results[0].click(e.chat_id, silent=True, hide_via=True)
    await e.delete()


@jepiq.tgbot.on(InlineQuery)
async def inlinecalc(event):
    query_user_id = event.query.user_id
    query = event.text
    string = query.lower()
    if (
        query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS
    ) and string == "calc":
        event.builder
        calc = event.builder.article(
            "Calc", text="**ุงูุญูุงุณุจุฉ ุงูุนููููุฉ ูุณููุฑุณ ุฃูุซูู\n @VV744**", buttons=lst
        )
        await event.answer([calc])


# ๐ง๐ฒ๐น๐ฒ๐๐ฟ๐ฎ๐  : @jepthon  ~ @lMl10l
@jepiq.tgbot.on(CallbackQuery(data=re.compile(b"calc(.*)")))
@check_owner
async def _(e):  # sourcery no-metrics
    x = (e.data_match.group(1)).decode()
    user = e.query.user_id
    get = None
    if x == "AC":
        if CALC.get(user):
            CALC.pop(user)
        await e.edit(
            "**ุงูุญูุงุณุจุฉ ุงูุนููููุฉ ูุณููุฑุณ ุงูุซูู\n @VV744**",
            buttons=[Button.inline("ุงูุชุญ ูุฑู ุงุฎุฑู", data="recalc")],
        )
    elif x == "C":
        if CALC.get(user):
            CALC.pop(user)
        await e.answer("ุชู ุงูุญุฐู")
    elif x == "โซ":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get[:-1]})
            await e.answer(str(get[:-1]))
    elif x == "%":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "/100"})
            await e.answer(str(get + "/100"))
    elif x == "รท":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "/"})
            await e.answer(str(get + "/"))
    elif x == "x":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + "*"})
            await e.answer(str(get + "*"))
    elif x == "=":
        if CALC.get(user):
            get = CALC[user]
        if get:
            if get.endswith(("*", ".", "/", "-", "+")):
                get = get[:-1]
            out = eval(get)
            try:
                num = float(out)
                await e.answer(f"โพโฎ ุงูุฌููุงุจ : {num}", cache_time=0, alert=True)
            except BaseException:
                CALC.pop(user)
                await e.answer("ุฎูุทุฃ", cache_time=0, alert=True)
        await e.answer("ุบูุฑ ูุนุฑูู")
    else:
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC.update({user: get + x})
            return await e.answer(str(get + x))
        CALC.update({user: x})
        await e.answer(str(x))


# ๐ง๐ฒ๐น๐ฒ๐๐ฟ๐ฎ๐  : @jepthon  ~ @lMl10l
@jepiq.tgbot.on(CallbackQuery(data=re.compile(b"recalc")))
@check_owner
async def _(e):
    m = [
        "AC",
        "C",
        "โซ",
        "%",
        "7",
        "8",
        "9",
        "+",
        "4",
        "5",
        "6",
        "-",
        "1",
        "2",
        "3",
        "x",
        "00",
        "0",
        ".",
        "รท",
    ]
    tultd = [Button.inline(f"{x}", data=f"calc{x}") for x in m]
    lst = list(zip(tultd[::4], tultd[1::4], tultd[2::4], tultd[3::4]))
    lst.append([Button.inline("=", data="calc=")])
    await e.edit("**ุงูุญูุงุณุจุฉ ุงูุนููููุฉ ูุณููุฑุณ ุฃูุซูู\n @VV744**", buttons=lst)

CMD_HELP.update(
    {"ุงูุญุณุงุจุฉ": ".ุญุงุณุจุฉ" "\n ููุท ุงูุชุจ ุงูุงูุฑ ูุนุฑุถ ุญุงุณุจุฉ ุนูููู ุชุญุชุงุฌ ุงูู ุชูุนูู ูุถุน ุงูุงููุงูู ุงููุง\n\n"}
)
