from telebot.async_telebot import AsyncTeleBot
from telebot.types         import Message, CallbackQuery, BotCommand
from typing                import Union
from loguru                import logger
from dotenv                import load_dotenv
from modules.webpilot      import WebPilot

import os

load_dotenv()

logger.add('logs/debug.log', format="{time:HH:mm:ss.SS} | {level} | {name}:{function}:{line}\n{message}", level="DEBUG", rotation="1 week", compression="zip", enqueue=True)
logger.add('logs/errors.log', format="{time:HH:mm:ss.SS} | {level} | {name}:{function}:{line}\n{message}", level="ERROR", rotation="1 week", compression="zip", enqueue=True)
logger.add('logs/warnings.log', format="{time:HH:mm:ss.SS} | {level} | {name}:{function}:{line}\n{message}", level="WARNING", rotation="1 week", compression="zip", enqueue=True)
logger.add('logs/info.log', format="{time:HH:mm:ss.SS} | {level} | {name}:{function}:{line}\n{message}", level="INFO", rotation="1 week", compression="zip", enqueue=True)

@logger.catch
async def start_command(object: Union[Message, CallbackQuery]):
  if isinstance(object, Message):
    await bot.reply_to(object, 'Привет!\n\nЯ бот Webpilot!\nСпроси что-нибудь')
  else:
    await bot.edit_message_text('Привет!\n\nЯ бот Webpilot!\nСпроси что-нибудь', object.message.chat.id, object.message.id)

@logger.catch
async def message_handler(message: Message):
  webpilot = WebPilot(os.getenv('WEBPILOT_API_KEY'))
  msg = await bot.reply_to(message, 'Загрузка...')
  text = await webpilot.get_response(message.text, msg.chat.id, msg.id, bot)
  await bot.edit_message_text(text, msg.chat.id, msg.id, parse_mode='Markdown')

async def start_bot(bot_local: AsyncTeleBot):
  global bot
  bot = bot_local
  await bot.set_my_commands([
    BotCommand('/start', 'Главное меню')
  ])
  bot.register_callback_query_handler(start_command, func=lambda call: call.data == '🏠')
  bot.register_message_handler(start_command, commands=['start'])
  bot.register_message_handler(message_handler, content_types=['text'])
  logger.success('Модули запущены')