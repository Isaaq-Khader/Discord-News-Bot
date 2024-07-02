import logging
import os

import discord
from src.bot import BotUtil
from dotenv import load_dotenv
from openai import OpenAI
from src.logs import log

logger = logging.getLogger("OpenAI API")

load_dotenv()
token = os.getenv('OPENAI_TOKEN')
client = OpenAI(api_key=token)

class AI:
    # Description: Creates a summary of a given article's text
    # Parameters:
    #   - article_text: The full text from an article
    # Returns: Summary of the given article text
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
        logger.debug(f"{log.DEBUG} Prompt Tokens Used: {usage.prompt_tokens}")
        logger.debug(f"{log.DEBUG} Completion Tokens Used: {usage.completion_tokens}")
        logger.debug(f"{log.DEBUG} Total Tokens Used: {usage.total_tokens}")

        response = chat_object.choices[0].message.content
        logger.info(f"{log.INFO} OpenAI Response: {response}")
        return response
    
    # Description: Checks if this is a valid article. Sometimes an article has redirect text or unavailable text so this ensures this is a valid article.
    # Parameters:
    #   - article_title: The title of the article
    # Returns: Whether this is a valid article or not (true/false)
    def check_article(article_title: str) -> bool:
        return "You are being redirected" in article_title

    def send_article(article_title: str, article_text: str) -> str:
        if not article_title or not article_text:
            return "There seems to be no information I can give you."
        if AI.check_article(article_title):
            return "Unable to summarize article."
        summary = AI.summarize_article(article_text)
        embedded_message = BotUtil.embedded_message(article_title, summary, BotUtil.author, BotUtil.footer, BotUtil.icon, BotUtil.thumbnail)
        return embedded_message

    # Description: Processes each given article by summarizing the article's text and putting it into a Discord embed to be displayed to the user.
    # Parameters:
    #   - title: Title of the embedded message
    #   - article_titles: List containing titles of each article
    #   - article_texts: List containing texts of each article
    # Returns: Custom discord embed for displaying the summaries of each article
    @staticmethod
    def process_articles(title: str, article_titles: list, article_texts: list) -> discord.Embed:
        if not article_titles or not article_texts:
            return "There seems to be no information I can give you."
        embedded_message = BotUtil.embedded_message(title=title, author=BotUtil.author, footer=BotUtil.footer, icon=BotUtil.icon, thumbnail=BotUtil.thumbnail)
        for title, text in zip(article_titles, article_texts):
            if AI.check_article(title):
                logger.warning(f"{log.WARN} Article was unable to be read... skipping...")
                continue
            logger.debug(f"{log.DEBUG} Article Title: {title}")
            logger.debug(f"{log.DEBUG} Article text len: {len(text)}")
            logger.debug(f"{log.DEBUG} Embed len: {len(embedded_message)}")
            if len(embedded_message) >= 5500:
                return embedded_message
            summary = AI.summarize_article(text)
            embedded_message.add_field(name=f"**{title}**", value=summary, inline=False)
        return embedded_message