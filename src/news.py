import discord
from gnews import GNews
import json
import logging
from bot import BotUtil
from logs import log
from newsplease import NewsPlease, NewsArticle
from openai_api import AI

logger = logging.getLogger("News")

class News:
    def get_articles_from_google(GoogleNews: GNews, news_articles: list[dict[str, any]] | list) -> tuple[list, list]:
        article_title_list = []
        article_text_list = []
        if not news_articles:
            logger.warning(f"{log.WARN} No Articles Found!")
            return [], [] 
        for index, article in enumerate(news_articles):
            logger.info(f"{log.DEBUG} Article #{index}\n {article}")
            article_details = GoogleNews.get_full_article(article["url"])
            if not article_details:
                logger.warning(f"{log.WARN} Error retreiving article! Skipping...")
                continue
            logger.info(f"{log.DEBUG} Article Title:{article_details.title}")
            article_title_list.append(article_details.title)
            article_text_list.append(article_details.text)
        return article_title_list, article_text_list

    def get_article_details(url: str) -> tuple[str, str]:
        article = NewsPlease.from_url(url)
        if not article:
            logger.warning(f"{log.WARN} No article found!")
            return [], []
        logger.debug(f"{log.DEBUG} Article return: {article}")
        article_props = NewsArticle.NewsArticle.get_dict(article)
        logger.debug(f"{log.DEBUG} Dict return: {article_props}")
        article_text = article_props["maintext"]
        logger.debug(f"{log.DEBUG} Article's text: {article_text}")
        text_length = len(article_text)
        logger.debug(f"{log.DEBUG} Article's length': {text_length}")
        article_title = article_props["title"]
        logger.debug(f"{log.DEBUG} Article Title: {article_title}")

        return article_title, article_text

    def get_specific_articles(message: discord.Message, attributes: list[str]) -> tuple[list, list, str]:
        GoogleNews = GNews(max_results=5, period='1d', exclude_websites=["ft.com", "wsj.com"])
        try:
            match attributes[0].lower():
                case "business":
                    title = "What's New in Business"
                    news_articles = GoogleNews.get_news_by_topic("BUSINESS")
                case "sports":
                    title = "What's New in Sports"
                    news_articles = GoogleNews.get_news_by_topic("SPORTS")
                case "technology":
                    title = "What's New in Tech"
                    news_articles = GoogleNews.get_news_by_topic("TECHNOLOGY")
                case "stock" | "stocks" | "stock market":
                    title = "What's New in the Stock Market"
                    news_articles = GoogleNews.get_news("stock market")
                case _:
                    if len(attributes) > 8:
                        logger.warning(f"{log.WARN} Too many attributes given for article search!!!")
                        return [], [], ""
                    attributes_revised = BotUtil.capitalize_words(attributes)
                    search_term = " ".join(attributes_revised)
                    title = f"What's New with {search_term}"
                    news_articles = GoogleNews.get_news(search_term)
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for news call for specific articles call")
            return "Seems like you're missing some information. What type of article are you looking for?"
        
        articles_titles, articles_texts = News.get_articles_from_google(GoogleNews, news_articles)
        return articles_titles, articles_texts, title

    def get_random_article() -> tuple[str, str]:
        # TODO: Get a random article from the web and pass along the title and text
        return [], []
        article_link = "https://www.cnn.com/2024/06/05/investing/nvidia-stock-apple-microsoft-market-value/index.html"
        article_title, article_text = News.get_article_details(article_link)
        return article_title, article_text

    async def get_news(message: discord.Message, attributes: list[str]) -> str:
        logger.info(f"{log.INFO} Attempting to retreive news...")
        logger.debug(f"{log.DEBUG} Attributes received: {attributes}")
        try:
            match attributes[1].lower():
                case "please":
                    article_title, article_text = News.get_random_article()
                    return await AI.send_article(message, article_title, article_text)
                case "from":
                    emoji = BotUtil.find_emoji(message, "standing_kitten")
                    if emoji:
                        await message.add_reaction(emoji)
                    else:
                        await message.add_reaction("🫡")
                    article_titles, article_texts, title = News.get_specific_articles(message, attributes[2:])
                    return await AI.process_articles(message, title, article_titles, article_texts)
                case "get":
                    logger.debug(f"{log.DEBUG} sending {attributes[2:]} to details")
                    article_title, article_text = News.get_article_details(attributes[2])
                    return await AI.send_article(message, article_title, article_text)
                case _:
                    return ""
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for news call. Perhaps it wasn't on purpose?")
            return ""