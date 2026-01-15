import asyncio, os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers.user import user

load_dotenv(dotenv_path=".env")
TOKEN = os.getenv("BOT_TOKEN")

# Run the bot
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        user.router,
    )

    print("Bot started ✅\nLink: https://t.me/tasksys_bot")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())