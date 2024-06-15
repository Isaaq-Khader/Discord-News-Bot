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
    def summarize_article(article_text: str) -> str:
        logger.info(f"{log.INFO} Making call to OpenAI for summary...")
        chat_object = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Ron Burgundy from the movie Anchorman who summarizes news."},
                {"role": "user", "content": f"Summarize this news article in three sentences or less. \nText: '''{article_text}'''"}
            ],
            max_tokens=3000,
            n=1
        )

        usage = chat_object.usage
        logger.info(f"{log.DEBUG} Prompt Tokens Used: {usage.prompt_tokens}")
        logger.info(f"{log.DEBUG} Completion Tokens Used: {usage.completion_tokens}")
        logger.info(f"{log.DEBUG} Total Tokens Used: {usage.total_tokens}")

        response = chat_object.choices[0].message.content
        logger.info(f"{log.INFO} OpenAI Response: {response}")
        return response
    
    def check_article(article_title: str):
        return "You are being redirected" in article_title

    def send_article(article_title: str, article_text: str) -> str:
        if not article_title or not article_text:
            return "There seems to be no information I can give you."
        if AI.check_article(article_title):
            return "Unable to summarize article."
        summary = AI.summarize_article(article_text)
        embedded_message = BotUtil.embedded_message(article_title, summary)
        return embedded_message

    def process_articles(title: str, article_titles: list, article_texts: list):
        if not article_titles or not article_texts:
            return "There seems to be no information I can give you."
        embedded_message = BotUtil.embedded_message(title, "")
        for title, text in zip(article_titles, article_texts):
            if AI.check_article(title):
                logger.warning(f"{log.WARN} Article was unable to be read... skipping...")
                continue
            logger.debug(f"{log.DEBUG} Article Title: {title}")
            logger.debug(f"{log.DEBUG} Article text len: {len(text)}")
            logger.info(f"{log.DEBUG} Embed len: {len(embedded_message)}")
            if len(embedded_message) >= 5500:
                return embedded_message
            summary = AI.summarize_article(text)
            embedded_message.add_field(name=f"**{title}**", value=summary, inline=False)
        return embedded_message