import discord
from gnews import GNews
import json
import logging
from logs import log
from newsplease import NewsPlease, NewsArticle
from openai_api import AI

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("News")

class News:
    def get_articles_from_google(GoogleNews: GNews, news_articles: list[dict[str, any]] | list) -> tuple[list, list]:
        article_title_list = []
        article_text_list = []
        for index, article in enumerate(news_articles):
            logger.debug(f"{log.DEBUG} Article #{index}\n {article}")
            article_details = GoogleNews.get_full_article(article["url"])

            logger.debug(f"{log.DEBUG} Article Title:{article_details.title}")
            article_title_list.append(article_details.title)
            article_text_list.append(article_details.text)
        return article_title_list, article_text_list

    def get_article_details(url: str) -> tuple[str, str]:
        article = NewsPlease.from_url(url)
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

    def get_specific_articles(message: discord.Message, attributes: list[str]) -> tuple[list, list]:
        GoogleNews = GNews(max_results=5, period='1d', exclude_websites=["ft.com", "wsj.com"])
        try:
            match attributes[0]:
                case "business":
                    news_articles = GoogleNews.get_news_by_topic("BUSINESS")
                    articles_titles, articles_texts = News.get_articles_from_google(GoogleNews, news_articles)
                    return articles_titles, articles_texts
                case "stock", "stocks", "stock market":
                    business_articles = GoogleNews.get_news("stock market money trade")
                    articles_titles, articles_texts = News.get_articles_from_google(GoogleNews, business_articles)
                    return articles_titles, articles_texts
                case _:
                    # TODO: try to do a query using what they typed in as attributes
                    return [], []              
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for news call for specific articles call")
            return "Seems like you're missing some information. What type of article are you looking for?"
        
    def get_random_article() -> tuple[str, str]:
        article_link = "https://www.cnn.com/2024/06/05/investing/nvidia-stock-apple-microsoft-market-value/index.html"
        article_title, article_text = News.get_article_details(article_link)
        return article_title, article_text

    async def get_news(message: discord.Message, attributes: list[str]) -> str:
        logger.info(f"{log.INFO} Attempting to retreive news...")
        logger.debug(f"{log.DEBUG} Attributes received: {attributes}")
        try:
            match attributes[1]:
                case "please":
                    article_title, article_text = News.get_random_article()
                    return await AI.send_article(message, article_title, article_text)
                case "from":
                    article_titles, article_texts = News.get_specific_articles(message, attributes[2:])
                    return await AI.process_articles(message, "What's New in Business", article_titles, article_texts)
                case "get":
                    logger.debug(f"{log.DEBUG} sending {attributes[2:]} to details")
                    article_title, article_text = News.get_article_details(attributes[2])
                    return await AI.send_article(message, article_title, article_text)
                case _:
                    return ""
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for news call. Perhaps it wasn't on purpose?")
            return ""