from random import randint
import discord
from gnews import GNews
import logging
from src.bot import BotUtil
from src.database import DatabaseNews
from src.logs import log
from newsplease import NewsPlease, NewsArticle
from src.openai_api import AI

logger = logging.getLogger("News")

class News:
    # Description: Attains articles from Google News API using urls provided by API.
    # Parameters:
    #   - GoogleNews: Custom GoogleNews object
    #   - news_articles: Collection of base level news articles
    # Returns: List of article titles and list of article texts
    def get_articles_from_google(GoogleNews: GNews, news_articles: list[dict[str, any]] | list) -> tuple[list, list]:
        article_title_list = []
        article_text_list = []
        if not news_articles:
            logger.warning(f"{log.WARN} No Articles Found!")
            return [], [] 
        for index, article in enumerate(news_articles):
            logger.debug(f"{log.DEBUG} Article #{index}\n {article}")
            article_details = GoogleNews.get_full_article(article["url"])
            if not article_details:
                logger.warning(f"{log.WARN} Error retreiving article! Skipping...")
                continue
            logger.debug(f"{log.DEBUG} Article Title:{article_details.title}")
            article_title_list.append(article_details.title)
            article_text_list.append(article_details.text)
        return article_title_list, article_text_list

    # Description: Gets details of an article through its URL using NewsPlease API.
    # Parameters:
    #   - url: URL of the article
    # Returns: Article's title and text
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

    # Description: Gets the news based on attributes given by user. Some keywords have special topics that can be searched.
    # Parameters:
    #   - attributes: List of strings containing parameters from the user
    # Returns: List of article titles, list of article texts, and search term used
    @staticmethod
    def get_specific_articles(attributes: list[str]) -> tuple[list, list, str]:
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

    # Description: Selects a random article from the news using GoogleNews API.
    # Parameters:
    #   - GoogleNews: Custom GoogleNews object
    # Returns: URL of the randomly selected article
    def select_random_article(GoogleNews: GNews) -> str:
        articles = GoogleNews.get_top_news()
        random = randint(0, GoogleNews.max_results - 1)
        logger.debug(f"{log.DEBUG} Chose random article #{random}")
        return articles[random]["url"]

    # Description: Randomly selects an article from the internet.
    # Parameters: None
    # Returns: Article's title and text
    def get_random_article() -> tuple[str, str]:
        GoogleNews = GNews(max_results=20, period='1d', exclude_websites=["ft.com", "wsj.com"])
        article_link = News.select_random_article(GoogleNews)
        logger.debug(f"{log.DEBUG} Attained {article_link}")
        article = GoogleNews.get_full_article(article_link)
        return article.title, article.text
        
    # Description: Processes user's command to get the news.
    # Parameters:
    #   - message: Discord message
    #   - attributes: List of strings containing parameters from the user
    # Returns: Response based on command given
    async def get_news(message: discord.Message, attributes: list[str]) -> str:
        logger.info(f"{log.INFO} Potential news call received")
        logger.debug(f"{log.DEBUG} Attributes received: {attributes}")
        try:
            match attributes[0].lower():
                case "please":
                    await BotUtil.acknowledge_message(message)
                    logger.debug(f"{log.DEBUG} User wants a random news article")
                    article_title, article_text = News.get_random_article()
                    logger.debug(f"{log.DEBUG} Random article's title: {article_title}")
                    return AI.send_article(article_title, article_text)
                case "from":
                    await BotUtil.acknowledge_message(message)
                    article_titles, article_texts, title = News.get_specific_articles(attributes[1:])
                    return AI.process_articles(title, article_titles, article_texts)
                case "get":
                    await BotUtil.acknowledge_message(message)
                    logger.debug(f"{log.DEBUG} sending {attributes[1:]} to details")
                    article_title, article_text = News.get_article_details(attributes[1])
                    return AI.send_article(article_title, article_text)
                case "add":
                    await BotUtil.acknowledge_message(message)
                    logger.info(f"{log.DEBUG} Current attributes: {attributes[1:]}")
                    return DatabaseNews.handle_set(DatabaseNews(), attributes[1:])
                case "remove":
                    await BotUtil.acknowledge_message(message)
                    channel = attributes[1]
                    logger.debug(f"{log.DEBUG} Channel ID: {channel}")
                    if BotUtil.verify_channel(channel):
                        search_term = " ".join(attributes[2:])
                        return DatabaseNews.delete_key_term(DatabaseNews(), channel, search_term)
                    else:
                        return "Invalid/No channel ID given."
                case "list":
                    await BotUtil.acknowledge_message(message)
                    data = DatabaseNews.read_channel_terms(DatabaseNews(), message.channel.id)
                    logger.debug(f"{log.DEBUG} Current read data: {data}")
                    if not data:
                        return "There is currently no news being posted to this channel."
                    embedded_message = BotUtil.embedded_message(f"Current search terms for #{message.channel.name}")
                    for _, key in data:
                        name_list = BotUtil.capitalize_words(list(key.split()))
                        embedded_message.add_field(name="", value=f"* {" ".join(name_list)}", inline=False)
                    return embedded_message
                case _:
                    logger.warning(f"{log.WARN} Unknown command {attributes[0]}!")
                    return BotUtil.similar_command_word("news", "news", attributes[0], BotUtil.supported_news_commands)
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for news call. Perhaps it wasn't on purpose?")
            return "I'm not able to do anything with an incomplete command!"
        except TypeError as e:
            logger.critical(f"{log.ERROR} Required one or more arguments to proceed... Error: {e}")
            return ""
        except Exception as e:
            logger.critical(f"{log.ERROR} {e}")
            return "I seem to have ran into an issue processing that command. Apologies."