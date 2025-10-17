from aiogram import Bot, Dispatcher
import asyncio
from handlers import register_handlers

# 🔑 Укажите токен вашего бота здесь
TOKEN = "8336802811:AAEodtJlk7nJGNN53oVCA-HAGAiVdK_nJ5U"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    print("🤖 Бот запущен...")
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())