import discord

class BotUtil:
    def embedded_message(embedded_title: str, embedded_description: str) -> discord.Embed:
        embed = discord.Embed(
            title=embedded_title,
            description=embedded_description,
            color=discord.Color.blue())
        embed.set_author(name="Ron Burgundy", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", icon_url="https://www.usatoday.com/gcdn/-mm-/9f6d022224eda40a294b4f8bd6a4e57117124c82/c=0-24-3000-2318&r=3000x2294/local/-/media/USATODAY/test/2013/08/13/1376422049000-Will-Ferrell.jpg")
        embed.set_footer(text="Written by San Diego's Finest")
        embed.set_thumbnail(url="https://ichef.bbci.co.uk/news/464/mcs/media/images/69276000/jpg/_69276020_ronburgundy_ap.jpg")
        return embed