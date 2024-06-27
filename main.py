from telebot.async_telebot import AsyncTeleBot
from dotenv                import load_dotenv
from loguru                import logger
from modules.telegram_bot  import start_bot

import os
import asyncio

load_dotenv()

logger.add('logs/debug.log', format="{time:HH:mm:ss.SS} | {level} | {name}:{function}:{line}\n{message}", level="DEBUG", rotation="1 week", compression="zip", enqueue=True)
logger.add('logs/errors.log', format="{time:HH:mm:ss.SS} | {level} | {name}:{function}:{line}\n{message}", level="ERROR", rotation="1 week", compression="zip", enqueue=True)
logger.add('logs/warnings.log', format="{time:HH:mm:ss.SS} | {level} | {name}:{function}:{line}\n{message}", level="WARNING", rotation="1 week", compression="zip", enqueue=True)
logger.add('logs/info.log', format="{time:HH:mm:ss.SS} | {level} | {name}:{function}:{line}\n{message}", level="INFO", rotation="1 week", compression="zip", enqueue=True)

bot = AsyncTeleBot(os.getenv('TELEGRAM_TOKEN'), parse_mode='html')

async def main(loop: asyncio.AbstractEventLoop):
  logger.success(f'Бот инициализирован как: @{(await bot.get_me()).username}')
  await start_bot(bot)
  await bot.polling(non_stop=True)

if __name__ == '__main__':
  loop = asyncio.new_event_loop()
  loop.create_task(main(loop=loop))
  loop.run_forever()

