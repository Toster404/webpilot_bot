import json
import time
import aiohttp

from telebot.async_telebot import AsyncTeleBot
from loguru                import logger

logger.add('logs/debug.log', format="{time:HH:mm:ss.SS} | {level} | {name}:{function}:{line}\n{message}", level="DEBUG", rotation="1 week", compression="zip", enqueue=True)
logger.add('logs/errors.log', format="{time:HH:mm:ss.SS} | {level} | {name}:{function}:{line}\n{message}", level="ERROR", rotation="1 week", compression="zip", enqueue=True)
logger.add('logs/warnings.log', format="{time:HH:mm:ss.SS} | {level} | {name}:{function}:{line}\n{message}", level="WARNING", rotation="1 week", compression="zip", enqueue=True)
logger.add('logs/info.log', format="{time:HH:mm:ss.SS} | {level} | {name}:{function}:{line}\n{message}", level="INFO", rotation="1 week", compression="zip", enqueue=True)

WEBPILOT_API_ENDPOINT = 'https://beta.webpilotai.com/api/v1'

class WebPilot():

  def __init__(self, api_key: str):
    self.api_key = api_key

  @logger.catch
  async def get_response(self, content: str, chat_id: int, message_id: int, bot: AsyncTeleBot) -> str:
    data = {'model': 'wp-watt-3.52-16k', 'content': content}
    headers = {'Authorization': f'Bearer {self.api_key}'}
    async with aiohttp.ClientSession(headers=headers) as session:
      async with session.post(f"{WEBPILOT_API_ENDPOINT}/watt/stream", json=data) as resp:
        start_time = time.time()
        i_time = time.time()
        text = ''
        async for chunk in resp.content:
          line = chunk.decode('utf-8')
          if 'data:' in line:
            line = line.replace('data:', '')
            line = line.strip()
            try:
              text += json.loads(line)['content']
            except:
              pass
            finally:
              if (time.time() - i_time) >= 1:
                await bot.edit_message_text(f'{text}\n\n<blockquote>Прошло секунд: {round(time.time() - start_time, 2)}</blockquote>', chat_id, message_id)
                i_time = time.time()


        return text
