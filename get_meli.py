import requests
from telethon import TelegramClient, events, Button
import asyncio

API_KEY = "API_KEY"

def get_meli(code_meli):

    response = requests.get(f"https://api.fast-creat.ir/codemeli?apikey={API_KEY}&code={code_meli}")
    data = response.json()  

    status = data.get("status")
    province = data.get("result", {}).get("province", "نامشخص")
    city = data.get("result", {}).get("city", "نامشخص")



    if status and status.lower().strip() == "successfully":
        print(f"♻️ ᴅᴀᴛᴀ ʀᴇᴄɪᴠᴇᴅ\n\n✅ sᴛᴀᴛᴜs: sᴜᴄᴄᴇssғᴜʟʟʏ\n🌏 ᴘʀᴏᴠɪɴᴄᴇ: {province}\n🗺 ᴄɪᴛʏ: {city}")
    else:
        print(response.text)

