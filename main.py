import asyncio
import logging
import random
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message

# 1. TIZIM SOZLAMALARI
MAIN_BOT_TOKEN = "8845429132:AAGqNonq_hjENW0T9wEHOmmJddR9s4TE01s"

# 20 ta yordamchi botingiz tokenlari ro'yxati
REACTION_BOTS = [
    "8931402330:AAFBszfLXb41LovOOavwPOgPHmAWyyGq8ww",
    "8896768016:AAHuuKmIpmHr4FIbgfXyo4o74ozjCZw59DA",
    "8640809311:AAFwd1VgZc61BXbTHcWJFDpUDwsLmClSWuc",
    "8834224710:AAHeDPHAqhbmOna3pHcsPzBv-Czf5n-DCL0",
    "8921092985:AAFqi9ZzFOZaZx-NFEiYRh4yGIruevpUqzg",
    "8434763428:AAHNWUTvrDOdDtlhDuRbmVtGv5aqBwTHljY",
    "8856116601:AAHs-bUih54nv7Ydhmwgbxe7V4CkPd0X0x0",
    "8890604157:AAGbeVq0gTRsAtZQc37lpyk5xc7YlfCMETM",
    "8832192223:AAHNBICfLLoj5e70fT7nRmF84uim4eL85b0",
    "8720003617:AAGtey3-hy_J4ORC1Oh6ZF7OdfNvDXU4shc",
    "8731930908:AAF6BPiXb9ZDlrzEdVyUggkh-q4PN4juKIU",
    "8793178841:AAF-IzJjr5bOQG8zQOSbmERrSzVbeECw-oE",
    "8918144397:AAH_NjrZxl7630by36K2wknBqbVFyx7Xq1k",
    "8615011857:AAGXkSZjENzeERMwZUxReroAJseN386yCwU",
    "8377051100:AAEmkuVBrZLKZyBkd0Vxq1yHOSkP-ziU_mM",
    "8986357581:AAGNmEbFzvfJK5BSHn6AT0HC3CBY1WLxw6I",
    "8799218093:AAG8_AZ-GyLtErBP2DRrRyk7cJ0IJnQ-kGs",
    "8693075084:AAEi5IH39PPF9TBqMCemoNc-ZY-bTdRtijk",
    "8918449347:AAG9wdcK5kiVNzU4TB8MJpvLFBYpin25QOg",
    "8951843579:AAFblpLmmrJNaOjdpfNsQEXLk9mmjl-d7vg"
    # ... qolgan bot tokenlarini ham shu tartibda vergul bilan ajratib qo'shing
]

# Skrinshotdagi barcha 50 ta rasmiy Telegram emojilari ro'yxati
EMOJILAR_RO_YXATI = [
    "⭐", "❤️", "👍", "👎", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬",
    "😢", "🎉", "🤩", "🙏", "👌", "🕊️", "🤡", "🥱", "😍", "🐳", "❤️‍🔥", "🌚",
    "🌭", "💯", "🤣", "⚡", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "😈",
    "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😰", "🤝", "✍️",
    "🤗", "🫡"
]

# Tizim xatoliklarini kuzatish (Logging)
logging.basicConfig(level=logging.INFO)

# Obyektlarni yaratish
bot = Bot(token=MAIN_BOT_TOKEN)
dp = Dispatcher()

# 2. AVTOMATIK REAKSIYA BOSISH FUNKSIYASI
async def auto_react(chat_id: int, message_id: int):
    # Har safar post chiqqanda 20 ta botdan tasodifiy sonda bot tanlanadi (masalan, 10 tadan 20 tagacha)
    # Bu reaksiyalar soni doim har xil va tabiiy chiqishi uchun kerak
    faol_botlar_soni = random.randint(10, len(REACTION_BOTS)) if len(REACTION_BOTS) >= 10 else len(REACTION_BOTS)
    tanlangan_botlar = random.sample(REACTION_BOTS, faol_botlar_soni)
    
    logging.info(f"Yangi postga {faol_botlar_soni} ta bot orqali har xil reaksiyalar yuborilmoqda...")

    for token in tanlangan_botlar:
        # Ro'yxatdan tasodifiy bitta emoji tanlanadi
        tasodifiy_emoji = random.choice(EMOJILAR_RO_YXATI)
        
        url = f"https://api.telegram.org/bot{token}/setMessageReaction"
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "reaction": [{"type": "emoji", "emoji": tasodifiy_emoji}]
        }
        
        try:
            # Telegram API ga reaksiya bosish so'rovini yuborish
            response = requests.post(url, json=payload, timeout=25)
            res_data = response.json()
            if not res_data.get("ok"):
                logging.warning(f"Bot xatosi: {res_data.get('description')}")
        except Exception as e:
            logging.error(f"Ulanishda xatolik yuz berdi: {e}")
            
        # Telegram spam tizimiga tushib qolmaslik uchun har bir bot orasida 0.3 soniya kutish
        await asyncio.sleep(0.3)

# 3. KANALDA YANGI POST PAYDO BO'LISHINI USHLASH
@dp.channel_post()
async def handle_new_post(message: Message):
    # Yangi postning ID si va Kanal ID sini avtomatik aniqlaydi
    chat_id = message.chat.id
    message_id = message.message_id
    
    # Reaksiya bosish jarayonini orqa fonda (background task) ishga tushirish
    asyncio.create_task(auto_react(chat_id, message_id))

# 4. BOTNI ISHGA TUSHIRISH
async def main():
    print("🚀 Avtomatik aralash reaksiya tizimi ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())