import datetime
import difflib
import logging
from logs import log
import discord
import re

logger = logging.getLogger("BotUtil")

class BotUtil:
    author = "Ron Burgundy"
    footer = "Written by San Diego's Finest"
    icon = "https://www.usatoday.com/gcdn/-mm-/9f6d022224eda40a294b4f8bd6a4e57117124c82/c=0-24-3000-2318&r=3000x2294/local/-/media/USATODAY/test/2013/08/13/1376422049000-Will-Ferrell.jpg"
    thumbnail = "https://ichef.bbci.co.uk/news/464/mcs/media/images/69276000/jpg/_69276020_ronburgundy_ap.jpg"

    supported_commands = ["help", "news", "roll"]
    supported_news_commands = ["add", "from", "get", "list", "please", "remove"]

    async def acknowledge_message(message: discord.Message):
        emoji = BotUtil.find_emoji(message, "standing_kitten")
        if emoji:
            await message.add_reaction(emoji)
        else:
            await message.add_reaction("🫡")

    def capitalize_word(word: str) -> str:
        return word[0].upper() + word[1:]

    def capitalize_words(words: list) -> list:
        new_words = []
        for word in words:
            logger.debug(f"{log.DEBUG} Current word: {word}")
            new_word = BotUtil.capitalize_word(word)
            logger.debug(f"{log.DEBUG} New word: {new_word}")
            new_words.append(new_word)
        return new_words
    
    def embedded_list(words: list[str]) -> str:
        embed_list = "\n".join(f"* {BotUtil.capitalize_word(word)}" for word in words)
        return embed_list

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
    
    def find_emoji(message: discord.Message, emoji_name: str) -> discord.Emoji:
        emojis = message.guild.emojis
        for emoji in emojis:
            if emoji.name == emoji_name:
                return emoji
        return None
    
    def similar_command_word(key_command: str, full_command: str, term: str, term_list: list[str]) -> str:
        similarity = difflib.get_close_matches(term, term_list)
        if similarity:
            logger.debug(f"{log.DEBUG} Closest match: {similarity}")
            return f"I don't know that {key_command} command. Did you mean `{full_command} {similarity[0]}`?"
        return f"I don't know that {key_command} command."
    
    def verify_channel(channel: str):
        logger.debug(f"{log.DEBUG} Verifying channel...")
        regex = "^\d+$" # all digits
        result = re.search(regex, channel)
        return result is not None