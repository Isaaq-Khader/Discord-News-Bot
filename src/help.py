import logging
from bot import BotUtil
from logs import log

logger = logging.getLogger("Help")

class Help:
    def __init__(self, attributes) -> None:
        self.attributes = attributes

    def dice_help(self):
        dice_icon = "https://cdn.pixabay.com/photo/2022/04/16/19/39/d20-7136921_640.png"
        message = BotUtil.embedded_message(title="Roll Help", thumbnail=dice_icon)
        message.add_field(name="**Description**", value="Allows you to roll a dice like in tabletop games.", inline=False)
        message.add_field(name="**Example Usages:**", value="`Roll 1d20`\n`Roll 8d6+4`\n`Roll 2d4-1`", inline=False)
        return message
    
    def general_help(self):
        question_mark = "https://static-00.iconduck.com/assets.00/white-question-mark-ornament-emoji-256x256-0ck2h3l5.png"
        message = BotUtil.embedded_message(title="General Help", thumbnail=question_mark)
        message.add_field(name="**Different commands:**", value=BotUtil.embedded_list(BotUtil.supported_commands), inline=False)
        message.add_field(name="", value="For more information on these commands, type `help [command]`", inline=False)
        message.add_field(name="", value="Example: `help news`", inline=False)
        return message

    def news_help(self, attributes):
        thumbnail = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMCXcZGvE7xr7oM7yqV0fcmC1TgLLU8uCrGJGFlQX1fUr8LcN5x5wE_rGYR1nU5F718Og&usqp=CAU"
        if len(attributes) == 1:
            message = BotUtil.embedded_message(title="News Help", thumbnail=thumbnail)
            message.add_field(name="**Description**", value="A set of commands to get news from within the past day in a summarized format. Daily news will be posted at 9AM CT.", inline=False)
            message.add_field(name="**Different commands:**", value=BotUtil.embedded_list(BotUtil.supported_news_commands), inline=False)
            message.add_field(name="", value="For more information on these commands, type `help news [command]`", inline=False)
            message.add_field(name="", value="Example: `help news please`", inline=False)
            return message
        try:
            match attributes[1]:
                case "add":
                    message = BotUtil.embedded_message(title="__News Add [Channel ID] [Search Term]__", thumbnail=thumbnail)
                    message.add_field(name="**Description**", value="Adds a search term for daily news to be published in the specified channel.", inline=False)
                    message.add_field(name="**Example Usage**", value="`news add 12345678901234567 stock market` -- adds the search term _stock market_ to daily news upload in channel _12345678901234567_.", inline=False)
                    logger.debug(f"{log.DEBUG} Sending help for news add")
                    return message
                case "from":
                    message = BotUtil.embedded_message(title="__News From [Search Term]__", thumbnail=thumbnail)
                    message.add_field(name="**Description**", value="Searches news from the search term given and provides summarized articles about the topic. Some topics such as _business_ and _sports_ will give more specific results as searches are based on Google News topics.", inline=False)
                    message.add_field(name="**Example Usage**", value="`news from technology` -- searches Google News under the topic of _technology_.\n`news from artificial intelligence` -- searches Google News using the search term of _artificial intelligence_.", inline=False)
                    logger.debug(f"{log.DEBUG} Sending help for news from")
                    return message
                case "get":
                    message = BotUtil.embedded_message(title="__News Get [Article Link]__", thumbnail=thumbnail)
                    message.add_field(name="**Description**", value="Summarizes the provided news article in 2-3 sentences.", inline=False)
                    message.add_field(name="**Example Usage**", value="`news get https://www.economist.com/business/2024/06/20/nvidia-is-now-the-worlds-most-valuable-company`", inline=False)
                    logger.debug(f"{log.DEBUG} Sending help for news get")
                    return message
                case "list":
                    message = BotUtil.embedded_message(title="__News List__", thumbnail=thumbnail)
                    message.add_field(name="**Description**", value="Lists the current search terms in the channel the command is typed in.", inline=False)
                    message.add_field(name="**Example Usage**", value="`news list`", inline=False)
                    logger.debug(f"{log.DEBUG} Sending help for news list")
                    return message
                case "please":
                    message = BotUtil.embedded_message(title="__News Please__", thumbnail=thumbnail)
                    message.add_field(name="**Description**", value="Provides a summary of a random article from the world wide web.", inline=False)
                    message.add_field(name="**Example Usage**", value="`news please`", inline=False)
                    logger.debug(f"{log.DEBUG} Sending help for news please")
                    return message
                case "remove":
                    message = BotUtil.embedded_message(title="__News Remove [Search Term]__", thumbnail=thumbnail)
                    message.add_field(name="**Description**", value="Removes a search term from being summarized in the daily news. If you're unsure of what topics already exist, use `news list`.", inline=False)
                    message.add_field(name="**Example Usage**", value="`news remove stock market` -- will no longer search news about the _stock market_ daily.", inline=False)
                    logger.debug(f"{log.DEBUG} Sending help for news remove")
                    return message
                case _:
                    logger.warning(f"{log.WARN} Unknown command {attributes[1]}!")
                    return BotUtil.similar_command_word("help", "help news", attributes[1], BotUtil.supported_news_commands)
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for help call. Did they miss an attribute?")
            return ""
        except Exception as e:
            logger.critical(f"{log.ERROR} {e}")
            return ""

    def help_processor(self) -> str:
        if len(self.attributes) == 1:
            logger.debug(f"{log.DEBUG} Sending general help commands...")
            return self.general_help()
        try:
            match self.attributes[1]:
                case "roll":
                    logger.debug(f"{log.DEBUG} Sending dice help commands...")
                    return self.dice_help()
                case "news":
                    logger.debug(f"{log.DEBUG} Sending news help commands...")
                    return self.news_help(self.attributes[1:])
                case _:
                    logger.warning(f"{log.WARN} Unknown command {self.attributes[1]}! Sending general help commands...")
                    return self.general_help()
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for help call. Perhaps it wasn't on purpose?")
            return ""
        except Exception as e:
            logger.critical(f"{log.ERROR} {e}")
            return ""