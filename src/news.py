from gnews import GNews
import json
import logging
from logs import log
from newsplease import NewsPlease, NewsArticle

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

    def get_article_details(url: str) -> str:
        article = NewsPlease.from_url(url)
        logger.info(f"{log.DEBUG} Article return: {article}")
        article_props = NewsArticle.NewsArticle.get_dict(article)
        logger.info(f"{log.DEBUG} Dict return: {article_props}")
        article_text = article_props["maintext"]
        logger.info(f"{log.DEBUG} Article's text: {article_text}")
        text_length = len(article_text)
        logger.info(f"{log.DEBUG} Article's length': {text_length}")
        article_title = article_props["title"]
        logger.info(f"{log.DEBUG} Article Title: {article_title}")

        if text_length > 2000:
            article_text = article_text[:2000]
        return article_text

    def get_specific_articles(attributes: list[str]) -> str:
        GoogleNews = GNews(max_results=5, period='1d', exclude_websites=["ft.com"])
        try:
            match attributes[0]:
                case "business":
                    news_articles = GoogleNews.get_news_by_topic("BUSINESS")
                    articles_titles, articles_texts = News.get_articles_from_google(GoogleNews, news_articles)
                    for title, text in zip(articles_titles, articles_texts):
                        logger.info(f"{log.DEBUG} Article Title: {title}")
                        logger.info(f"{log.DEBUG} Article text len: {len(text)}")
                    return "TODO! Business articles"
                case "stock", "stocks", "stock market":
                    business_articles = GoogleNews.get_news("stock market money trade")
                    articles_titles, articles_texts = News.get_articles_from_google(GoogleNews, business_articles)
                    return "TODO! Stock articles"
                case _:
                    return "TODO! Other articles"              
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for news call for specific articles call")
            return "Seems like you're missing some information. What type of article are you looking for?"
        
    def get_random_article():
        article_link = "https://www.cnn.com/2024/06/05/investing/nvidia-stock-apple-microsoft-market-value/index.html"
        article_text = News.get_article_details(article_link)
        return article_text

    def get_news(attributes: list[str]) -> str:
        logger.debug(f"{log.INFO} Attempting to retreive news...")
        logger.debug(f"{log.DEBUG} Attributes received: {attributes}")
        try:
            match attributes[1]:
                case "please":
                    return News.get_random_article()
                case "from":
                    return News.get_specific_articles(attributes[2:])
                case "get":
                    logger.info(f"sending {attributes[2:]} to details")
                    return News.get_article_details(attributes[2])
                case _:
                    return ""
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for news call. Perhaps it wasn't on purpose?")
            return ""