import asyncio
from aiogram import Bot, Dispatcher

from handlers import register_routes
from database.models import BaseModel
from database import engine

TOKEN = ""

# плохой подход тк изменения не мигригруются в бд
async def init_model():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    register_routes(dp)
    
    await init_model()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
