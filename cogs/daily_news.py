import datetime
import logging
from src.database import DatabaseNews
from discord.ext import tasks, commands
from src.logs import log
from src.news import News
from src.openai_api import AI

logger = logging.getLogger("DailyNews")
SENDING_TIME = datetime.time(13, 00, 0, 0) # in UTC (-5 CST)

class DailyNews(commands.Cog):
    def __init__(self, client) -> None:
        self.send_news.start()
        self.client = client
        self.database = DatabaseNews()
        self.open_ai = AI()
        self.news = News()

    def news_unload(self):
        self.send_news.cancel()

    @tasks.loop(time=SENDING_TIME)
    async def send_news(self):
        try:
            logger.info(f"{log.INFO} Running daily news!")
            channel_ids = self.database.get_channel_ids()
            logger.debug(f"{log.DEBUG} Channel IDs: {channel_ids}")
            key_terms = self.database.get_key_terms()
            logger.debug(f"{log.DEBUG} Key terms: {key_terms}")
            key_terms_cache: dict = {}
            for curr_id, curr_key in zip(channel_ids, key_terms):
                id = curr_id[0]
                key = curr_key[0]
                logger.info(f"Current Channel ID: {id}")
                logger.info(f"Current search term: {key}")
                channel = self.client.get_channel(id)
                if key in list(key_terms_cache.keys()):
                    logger.debug(f"{log.DEBUG} Using cached embedded response for channel {id}!")
                    embedded_response = key_terms_cache.get(key)
                    await channel.send(embed=embedded_response)
                    continue
                article_titles, article_texts, title = self.news.get_specific_articles(list(key.split(" ")))
                embedded_response = self.open_ai.process_articles(title, article_titles, article_texts)
                key_terms_cache[key] = embedded_response
                await channel.send(embed=embedded_response)
        except Exception as e:
            logger.critical(f"{log.ERROR} {e}")

    @send_news.before_loop
    async def before_daily_news(self):
        logger.info(f"{log.INFO} Waiting to send the news!")
        await self.client.wait_until_ready()

async def setup(client):
    await client.add_cog(DailyNews(client))