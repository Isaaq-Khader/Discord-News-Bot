import logging
import os
import discord
from dotenv import load_dotenv
from openai import OpenAI

from logs import log

logger = logging.getLogger("OpenAI API")

load_dotenv()
token = os.getenv('OPENAI_TOKEN')
client = OpenAI(api_key=token)

class AI:
    async def summarize_article(message: discord.Message, article_title: str, article_text: str) -> str:
        await message.channel.send(f"**{article_title}**")
        await message.channel.send(">>> ARTICLE SUMMARY \nWILL GO HERE") # article_text
        return ""

    async def process_articles(message: discord.Message, article_titles: list, article_texts: list):
        for title, text in zip(article_titles, article_texts):
            logger.debug(f"{log.DEBUG} Article Title: {title}")
            logger.debug(f"{log.DEBUG} Article text len: {len(text)}")
            await AI.summarize_article(message, title, text)
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