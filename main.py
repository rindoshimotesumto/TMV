import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from database.migrations import migrations

from handlers.start import sign_in, start
from handlers.tasks import tasks

from middlewares.middlewares import setup_middlewares

from logger.logger import write_logs

load_dotenv(dotenv_path=".env")
TOKEN: str | None = os.getenv("BOT_TOKEN")


# Run the bot
async def main():
    try:
        if not TOKEN:
            raise RuntimeError("TOKEN is not set!")

        bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

        dp = Dispatcher()
        
        
        dp.include_routers(
            start.router,
            sign_in.router,
            tasks.router,
        )

        await setup_middlewares(dp)
        await migrations.create_all_tables()

        write_logs("Bot started, link: https://t.me/tasksys_bot ✅")

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    except Exception as e:
        write_logs(str(e))


if __name__ == "__main__":
    asyncio.run(main())
