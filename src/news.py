import json
import logging
from logs import log
from newsplease import NewsPlease, NewsArticle

logger = logging.getLogger("News")

class News:
    def get_article_details(article_link: str) -> str:
        article = NewsPlease.from_url(f"{article_link}")
        article_props = NewsArticle.NewsArticle.get_dict(article)
        article_text = article_props["maintext"]
        text_length = len(article_text)
        logger.debug(f"{log.DEBUG} Article's length': {text_length}")
        article_title = article_props["title"]
        logger.debug(f"{log.DEBUG} Article Title: {article_title}")

        return f"Here's an article: COMING SOON!"

    def get_specific_articles(attributes: list[str]) -> str:
        try:
            match attributes[0]:
                case "business":
                    return "TODO! Business articles"
                case "finance":
                    return "TODO! Finance articles"
                case _:
                    return "TODO! Other articles"              
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for news call for specific articles call")
            return "Seems like you're missing some information. What type of article are you looking for?"
        
    def get_news(attributes: list[str]) -> str:
        logger.debug(f"{log.INFO} Attempting to retreive news...")
        logger.debug(f"{log.DEBUG} Attributes received: {attributes}")
        try:
            match attributes[1]:
                case "please":
                    # this will give a random article from the web
                    article_link = "https://www.cnn.com/2024/06/05/investing/nvidia-stock-apple-microsoft-market-value/index.html"
                    return News.get_article_details(article_link)
                case "from":
                    return News.get_specific_articles(attributes[2:])
                case "get":
                    return News.get_article_details(attributes[2:])
                case _:
                    return ""
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for news call. Perhaps it wasn't on purpose?")
            return ""