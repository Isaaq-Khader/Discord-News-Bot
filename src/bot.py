import datetime
import difflib
import logging
from src.logs import log
import discord
import re

logger = logging.getLogger("BotUtil")

class BotUtil:
    author = "Ron Burgundy"
    footer = "Written by San Diego's Finest"
    icon = "https://www.usatoday.com/gcdn/-mm-/9f6d022224eda40a294b4f8bd6a4e57117124c82/c=0-24-3000-2318&r=3000x2294/local/-/media/USATODAY/test/2013/08/13/1376422049000-Will-Ferrell.jpg"
    thumbnail = "https://ichef.bbci.co.uk/news/464/mcs/media/images/69276000/jpg/_69276020_ronburgundy_ap.jpg"

    bot_prefix = "$"
    supported_commands = ["help", "news", "roll"]
    supported_news_commands = ["add", "from", "get", "list", "please", "remove"]

    # Description: Acknowledges a given message with a reaction emoji.
    # Parameters:
    #   - message: Discord message
    # Returns: None
    async def acknowledge_message(message: discord.Message) -> None:
        emoji = BotUtil.find_emoji(message, "standing_kitten")
        if emoji:
            await message.add_reaction(emoji)
        else:
            await message.add_reaction("🫡")

    # Description: Capitalizes a given string
    # Parameters:
    #   - word: Single word
    # Returns: Capitalized word
    def capitalize_word(word: str) -> str:
        return word[0].upper() + word[1:]

    # Description: Capitalizes the first letter in a set of strings
    # Parameters:
    #   - words: List of words
    # Returns: List of capitalized words
    def capitalize_words(words: list) -> list:
        new_words = []
        for word in words:
            logger.debug(f"{log.DEBUG} Current word: {word}")
            new_word = BotUtil.capitalize_word(word)
            logger.debug(f"{log.DEBUG} New word: {new_word}")
            new_words.append(new_word)
        return new_words
    
    # Description: Turns a list into a bullet point form for a Discord embed
    # Parameters:
    #   - words: List of words
    # Returns: Bullet pointed list of words
    def embedded_list(words: list[str]) -> str:
        embed_list = "\n".join(f"* {BotUtil.capitalize_word(word)}" for word in words)
        return embed_list

    # Description: Creates a template for a Discord embedded message
    # Parameters:
    #   - title: Title of the Discord embed
    #   - description: Description of the Discord embed
    #   - author: Author of the Discord embed
    #   - footer: Footer of the Discord embed
    #   - icon: URL of image to be used as an icon
    #   - thumbnail: URL of image to be used as a thumbnail
    # Returns: Discord embed
    def embedded_message(title: str, description: str = "", author = "", footer = "", icon = "", thumbnail = "") -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now())
        embed.set_author(name=author, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", icon_url=icon)
        embed.set_footer(text=footer)
        embed.set_thumbnail(url=thumbnail)
        return embed
    
    # Description: Finds whether an emoji exists in the server the message was sent.
    # Parameters:
    #   - message: Discord message
    #   - emoji_name: Name of the emoji to be cross referenced
    # Returns: If the emoji exists
    def find_emoji(message: discord.Message, emoji_name: str) -> discord.Emoji:
        emojis = message.guild.emojis
        for emoji in emojis:
            if emoji.name == emoji_name:
                return emoji
        return None
    
    # Description: Checks whether the misinput is similar to an existing command.
    # Parameters:
    #   - key_command: The specific command attempting to be run
    #   - full_command: The full command being ran
    #   - term: The misinput given by the user
    #   - term_list: Potential matches for the misinput by the user
    # Returns: Response prompting user for correct use of command or response saying unknown command (no similarities found)
    def similar_command_word(key_command: str, full_command: str, term: str, term_list: list[str]) -> str:
        similarity = difflib.get_close_matches(term, term_list)
        if similarity:
            logger.debug(f"{log.DEBUG} Closest match: {similarity}")
            return f"I don't know that {key_command} command. Did you mean `{full_command} {similarity[0]}`?"
        return f"I don't know that {key_command} command."
    
    # Description: Verifies whether a proper channel ID was provided.
    # Parameters:
    #   - channel: Potential channel ID
    # Returns: Whether a proper channel ID was given (true/false)
    def verify_channel(channel: str):
        logger.debug(f"{log.DEBUG} Verifying channel...")
        regex = "[0-9]{17,18}"
        result = re.search(regex, channel)
        is_channel = result is not None
        logger.debug(f"{log.DEBUG} is channel: {is_channel}")
        return is_channel