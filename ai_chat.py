import requests
from telethon import Button

API_KEY = "API_KEY"

async def ai_chat(event , prompt):
    req = requests.get(f"https://api.fast-creat.ir/gpt/chat?apikey={API_KEY}&text={prompt}")
    data = req.json()
    text = data.get("result", {}).get("text", "نامشخص")

    buttons = [
        Button.url("♻️ sɪʟᴋ ʀᴏᴀᴅ", "https://t.me/phonixhouse")
    ]

    if req.status_code == 200 and text:
        await event.reply(f"{text}" , buttons=buttons)
    else:
        await event.reply("هر 3 ثانیه یکبار میتوانید سوال بپرسید" , buttons=buttons)