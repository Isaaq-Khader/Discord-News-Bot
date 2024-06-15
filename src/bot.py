import logging
from logs import log
import discord

logger = logging.getLogger("BotUtil")

class BotUtil:
    async def acknowledge_message(message: discord.Message):
        emoji = BotUtil.find_emoji(message, "standing_kitten")
        if emoji:
            await message.add_reaction(emoji)
        else:
            await message.add_reaction("🫡")

    def capitalize_words(words: list) -> list:
        new_words = []
        for word in words:
            logger.info(f"{log.DEBUG} Current word: {word}")
            new_word = word[0].upper() + word[1:]
            logger.info(f"{log.DEBUG} New word: {new_word}")
            new_words.append(new_word)
        return new_words
    
    def embedded_message(embedded_title: str, embedded_description: str) -> discord.Embed:
        embed = discord.Embed(
            title=embedded_title,
            description=embedded_description,
            color=discord.Color.blue())
        embed.set_author(name="Ron Burgundy", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", icon_url="https://www.usatoday.com/gcdn/-mm-/9f6d022224eda40a294b4f8bd6a4e57117124c82/c=0-24-3000-2318&r=3000x2294/local/-/media/USATODAY/test/2013/08/13/1376422049000-Will-Ferrell.jpg")
        embed.set_footer(text="Written by San Diego's Finest")
        embed.set_thumbnail(url="https://ichef.bbci.co.uk/news/464/mcs/media/images/69276000/jpg/_69276020_ronburgundy_ap.jpg")
        return embed
    
    def find_emoji(message: discord.Message, emoji_name: str) -> discord.Emoji:
        emojis = message.guild.emojis
        for emoji in emojis:
            if emoji.name == emoji_name:
                return emoji
        return None