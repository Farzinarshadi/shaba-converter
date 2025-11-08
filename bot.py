from telethon import TelegramClient, events, Button
from telethon.network import ConnectionTcpAbridged
import re
import requests
import base64
import json
import random
import os
import asyncio
from telethon.tl.custom import Conversation
from get_meli import get_meli
from ai_chat import ai_chat


# ---------------- info ----------------
api_id = "API_ID"
api_hash = "API_HASH"
bot_token = "BOT_TOKEN"

client = TelegramClient('estelam_session',
                        api_id,
                        api_hash,
                        connection=ConnectionTcpAbridged,
                        use_ipv6=False)


BLOCK_FILE = "blocked_users.json"
ADMIN_ID = 1878800785  


if not os.path.exists(BLOCK_FILE):
    with open(BLOCK_FILE, "w") as f:
        json.dump([], f)

def load_blocked_users():
    with open(BLOCK_FILE, "r") as f:
        return json.load(f)

def save_blocked_users(blocked):
    with open(BLOCK_FILE, "w") as f:
        json.dump(blocked, f)

def is_blocked(user_id):
    blocked = load_blocked_users()
    return user_id in blocked

# ---------------- start ----------------
@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    if is_blocked(event.sender_id):
        await event.reply("⛔ دلقکی ؟")
        return

    if event.is_channel or event.is_group:
        return
    
    first_name = event.sender.first_name or ""
    await event.reply(f"سلام {first_name}\nاز امکانات این ربات فقط در گروه ما میتوانید استفاده کنید:\n\nhttps://t.me/+a1Z9u5gxRzo2MGM0")

# ---------------- get sheba ----------------

def get_nonce():
    try:
        response = requests.get("https://shepa.com/sheba/")
        if response.status_code == 200:
            html = response.text
            match = re.search(r'data-nonce="([a-zA-Z0-9]+)"', html)
            if match:
                return match.group(1)
            else:
                print("🔴 نتوانستیم data-nonce را با regex پیدا کنیم.")
        else:
            print(f"❌ دریافت HTML ناموفق بود. کد: {response.status_code}")
    except Exception as e:
        print(f"❌ خطا در گرفتن nonce: {e}")
        

async def get_captcha(event, client):
    payload = {"action": "ira_iban_captcha"}
    try:
        response = requests.post("https://shepa.com/wp-admin/admin-ajax.php", data=payload)
        if response.status_code == 200:
            json_response = response.json()
            captcha_data = json_response.get("captcha")
            key = json_response.get("key")
            if json_response.get("success") and captcha_data and key:
                os.makedirs("captchas", exist_ok=True)
                filename = f"{random.randint(10000, 99999)}.png"
                filepath = os.path.join("captchas", filename)
                base64_string = captcha_data.split(",")[1]
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(base64_string))

                async with client.conversation(event.chat_id, timeout=30) as conv:
                    await conv.send_message(
                        "🔢 عدد داخل تصویر رو با اعداد لاتین بفرست تا اطلاعات رو بدمت:",
                        file=filepath,
                        reply_to=event.id
                    )
                    try:
                        while True:
                            response = await conv.get_response()
                            if response.sender_id == event.sender_id:  
                                user_input = response.raw_text.strip()
                                if not user_input.isdigit():
                                    await conv.send_message(
                                        "❌ فقط عدد مجاز است. عملیات لغو شد.",
                                        reply_to=event.id
                                    )
                                    return None
                                return int(user_input), key

                    except asyncio.TimeoutError:
                        await conv.send_message(
                            "⌛ زمان شما برای وارد کردن کد کپچا به پایان رسید.",
                            reply_to=event.id
                        )
                        return None
                    finally:
                        os.remove(filepath)  
            else:
                await event.reply("❌ CAPTCHA یا key یافت نشد.")
        else:
            await event.reply(f"❌ وضعیت پاسخ: {response.status_code}")
    except Exception as e:
        await event.reply(f"❌ خطا: {e}")
        return None
    

bank_logos = {
    "627412": "eghtesad.png",
    "627381": "ansar.png",
    "505785": "iranzamin.png",
    "636214": "ayandeh.png",
    "502229": "pasargad.png",
    "627488": "karafarin.png",
    "621986": "saman.png",
    "589210": "sepah.png",
    "603769": "saderat.png",
    "627961": "sanatmadan.png",
    "603770": "keshavarsi.png",
    "639217": "melal.png",
    "603799": "meli.png",
    "627353": "tejarat.png",
    "585983": "tejarat.png",  
    "622106": "parsian.png",
    "502908": "saderat.png",
    "627760": "postbank.png",
    "502938": "day.png",
    "627884": "parsian.png",  
    "610433": "maskan.png",
    "603793": "mehreqtesad.png",
    "505416": "gardeshgari.png",
    "504706": "shahr.png",
    "502806": "tosehe.png",
    "502910": "karafarin.png",
}

bank_names = {
    "627412": "بانک اقتصاد نوین",
    "627381": "بانک انصار",
    "505785": "بانک ایران‌زمین",
    "636214": "بانک آینده",
    "502229": "بانک پاسارگاد",
    "627488": "بانک کارآفرین",
    "621986": "بانک سامان",
    "589210": "بانک سپه",
    "603769": "بانک صادرات",
    "627961": "بانک صنعت و معدن",
    "603770": "بانک کشاورزی",
    "639217": "بانک ملل",
    "603799": "بانک ملی ایران",
    "627353": "بانک تجارت",
    "585983": "بانک تجارت",
    "622106": "بانک پارسیان",
    "502908": "بانک توسعه صادرات",
    "627760": "پست بانک ایران",
    "502938": "بانک دی",
    "636795": "بانک مرکزی",
    "627884": "بانک پارسیان",
    "610433": "بانک مسکن",
    "603793": "بانک مهر ایران",
    "606373": "بانک قرض‌الحسنه رسالت",
    "505416": "بانک گردشگری",
    "504706": "بانک شهر",
    "502806": "بانک توسعه تعاون",
    "502910": "بانک کارآفرین",
    "636949": "بانک حکمت ایرانیان",
    "627648": "بانک توسعه تعاون",
    "639346": "بانک سینا"
}



async def get_shaba(event, card_number):
    if is_blocked(event.sender_id):
        await event.reply("⛔ دلقکی ؟")
        return

    captcha_data = await get_captcha(event, client)
    if captcha_data is None:
        return

    captcha, key = captcha_data
    token = get_nonce()

    payload = {
        "action": "ira_iban_action",
        "cardnumber_or_accound": str(card_number),
        "bank_code": "",
        "key": key,
        "captcha": captcha,
        "_wpnonce": token
    }

    try:
        response = requests.post("https://shepa.com/wp-admin/admin-ajax.php", data=payload)
        result = response.json()

        if result.get("success") and "result" in result:
            data = result["result"]
            first_name = data.get("first_name", "ناموجود")
            last_name = data.get("last_name", "ناموجود")
            iban = data.get("iban_number", "ناموجود")
            deposits = data.get("deposits", "ناموجود")

            if first_name == "ناموجود":
                await event.reply("⛔️شماره کارت نامعتبره")
                return

            bin_code = str(card_number)[:6]
            bank_name = bank_names.get(bin_code, "نامشخص")
            logo_filename = bank_logos.get(bin_code)

            msg = (
                "✅ اطلاعات دریافت شد:\n\n"
                f"👤 نام کامل: {first_name} {last_name}\n"
                f"🏦 بانک: {bank_name}\n"
                f"🏦 شبا: `{iban}`\n"
                f"💳 شماره حساب: `{deposits}`\n"
            )

            buttons = [Button.url("♻️ sɪʟᴋ ʀᴏᴀᴅ", "https://t.me/phonixhouse")]

            if logo_filename:
                image_path = os.path.join("bank_images", logo_filename)
                if os.path.exists(image_path):
                    await event.reply(file=image_path, message=msg, buttons=buttons)
                    return

            await event.reply(msg, buttons=buttons)
        else:
            await event.reply("❌ عملیات موفق نبود یا نتیجه‌ای برنگشت.")
        return result
    except Exception as e:
        await event.reply("⚠️ خطا در ارتباط با سرور.")
        return None

# ---------------- delete group messages ----------------
@client.on(events.NewMessage(chats=2828795678))
async def handle_message(event):
    try:
        if event.raw_text == "استعلام" or event.raw_text == "اطلاعات" :
            if event.is_reply:
                reply_msg = await event.get_reply_message()
                card_pattern = r'\b\d{16}\b'
                if reply_msg and re.search(card_pattern, reply_msg.raw_text):
                    await reply_msg.delete()
                    card_number = re.search(card_pattern, reply_msg.raw_text).group()
                    await get_shaba(event, card_number)
                else:
                    await event.reply("احمق باید روی شماره کارت ریپلای بزنی")
            else:
                await event.reply("احمق باید روی شماره کارت ریپلای بزنی")
        elif event.raw_text == "ملی":
            if is_blocked(event.sender_id):
                await event.reply("⛔ دلقکی ؟")
                return
            if event.is_reply:
                reply_msg = await event.get_reply_message()
                code_meli_text = reply_msg.raw_text.strip()
                await get_meli(event, code_meli_text)
            else:
                await event.reply("احمق باید روی کد ملی ریپلای بزنی")
        elif event.raw_text.startswith("+"):
            if is_blocked(event.sender_id):
                await event.reply("⛔ دلقکی ؟")
                return
            await ai_chat(event , event.raw_text)

                
    except Exception as e:
        await event.reply(f"❌ خطا در پردازش پیام: {e}")


@client.on(events.NewMessage(pattern="^gg$"))
async def block_user(event):
    if event.sender_id != ADMIN_ID:
        return

    if not event.is_reply:
        await event.reply(" باید روی پیام کاربر ریپلای کنی.")
        return

    reply_msg = await event.get_reply_message()
    target_id = reply_msg.sender_id

    blocked = load_blocked_users()
    if target_id not in blocked:
        blocked.append(target_id)
        save_blocked_users(blocked)
        await event.reply("✅ کاربر با موفقیت کیر شد.")
    else:
        await event.reply("⚠️ این کاربر قبلاً بلاک کیر است.")

# ---------------- آنبلاک کردن کاربر با دستور bb ----------------
@client.on(events.NewMessage(pattern="^bb$"))
async def unblock_user(event):
    if event.sender_id != ADMIN_ID:
        return

    if not event.is_reply:
        await event.reply("باید روی پیام کاربر ریپلای کنی.")
        return

    reply_msg = await event.get_reply_message()
    target_id = reply_msg.sender_id

    blocked = load_blocked_users()
    if target_id in blocked:
        blocked.remove(target_id)
        save_blocked_users(blocked)
        await event.reply("✅ کاربر از بلاک کیر خارج شد.")
    else:
        await event.reply("⚠️ این کاربر در لیست کیر نبود.")

# ---------------- client ----------------
async def main():
    try:
        await client.start(bot_token=bot_token)
        print("Bot is running...")
        await client.run_until_disconnected()
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

