# -*- coding: utf-8 -*-
import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import AsyncOpenAI

logging.basicConfig(level=logging.INFO)

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Привет! Я AI-бот на базе Qwen 3.6 Plus.")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("📝 Команды: /start, /help")

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    
    try:
        response = await client.chat.completions.create(
            model="qwen/qwen3.6-plus",  # БЕЗ :free - платная версия
            messages=[{"role": "user", "content": message.text}],
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        for chunk in [answer[i:i+4096] for i in range(0, len(answer), 4096)]:
            if chunk.strip():
                await message.answer(chunk)
            
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer(f"⚠️ Ошибка: {type(e).__name__}")

async def main():
    logging.info("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
