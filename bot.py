from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
import json

# Loading configuration
from config import config

bot = Bot(token=config['TELEGRAM_BOT_TOKEN'])
dp = Dispatcher()

def load_chat_ids():
    try:
        with open('chat_ids.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_chat_ids(chat_ids):
    with open('chat_ids.json', 'w') as f:
        json.dump(chat_ids, f)

@dp.message(Command('start'))
async def start(message):
    chat_id = message.chat.id
    chat_ids = load_chat_ids()
    if chat_id not in chat_ids:
        chat_ids.append(chat_id)
        save_chat_ids(chat_ids)
    await message.reply("Теперь я буду присылать тебе уведомления об отключениях!")

@dp.message(Command('stop'))
async def stop(message):
    chat_id = message.chat.id
    chat_ids = load_chat_ids()
    if chat_id in chat_ids:
        chat_ids.remove(chat_id)
        save_chat_ids(chat_ids)
    await message.reply("Ты больше не будешь получать уведомления об отключениях.")

async def broadcast_message(message_text):
    chat_ids = load_chat_ids()
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=message_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")
