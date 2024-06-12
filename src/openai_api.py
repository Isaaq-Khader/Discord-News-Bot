import logging
import os
import discord
from bot import BotUtil
from dotenv import load_dotenv
from openai import OpenAI

from logs import log

logger = logging.getLogger("OpenAI API")

load_dotenv()
token = os.getenv('OPENAI_TOKEN')
client = OpenAI(api_key=token)

class AI:
    async def summarize_article(article_text: str) -> str:
        # await message.channel.send(f"**{article_title}**")
        # await message.channel.send(">>> ARTICLE SUMMARY \nWILL GO HERE") # article_text
        # embedded_message = BotUtil.embedded_message(article_title, article_text)
        # await message.channel.send(embed=embedded_message)
        # TODO: Add in openAI call to create a summary
        return article_text[:500]
    
    async def send_article(message: discord.Message, article_title: str, article_text: str) -> str:
        summary = await AI.summarize_article(article_text)
        embedded_message = BotUtil.embedded_message(article_title, summary)
        await message.channel.send(embed=embedded_message)
        return ""

    async def process_articles(message: discord.Message, title: str, article_titles: list, article_texts: list):
        embedded_message = BotUtil.embedded_message(title, "")
        for title, text in zip(article_titles, article_texts):
            logger.debug(f"{log.DEBUG} Article Title: {title}")
            logger.debug(f"{log.DEBUG} Article text len: {len(text)}")
            logger.info(f"{log.DEBUG} Embed len: {len(embedded_message)}")
            if len(embedded_message) >= 5500:
                await message.channel.send(embed=embedded_message)
            summary = await AI.summarize_article(text)
            embedded_message.add_field(name=f"**{title}**", value=summary, inline=False)
        await message.channel.send(embed=embedded_message)
        return ""
    def create_message():
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
        )

        print(completion.choices[0].message)