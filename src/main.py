from dotenv import load_dotenv
# from discord import Intents, Client, Message
import discord as d
import logging
from logs import log
import os
from responses import ResponseHandler
from typing import Final

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("NewsBot")

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
intents = d.Intents.default()
intents.message_content = True
client = d.Client(intents=intents)

class DiscordBot:
    async def send_message(message: d.Message, user_message: str) -> None:
        if not user_message:
            logger.warning(f"{log.WARN} Empty user message received")
            return
        
        try:
            response = ResponseHandler.handle_response(user_message)
            if response:
                await message.channel.send(response)
        except Exception as e:
            logger.critical(f"{log.ERROR} {e}")
    
    @client.event
    async def on_ready() -> None:
        logger.info(f"{log.INFO} {client.user} is now running!")
        await client.change_presence(activity=d.Activity(type=d.ActivityType.watching, name="current news"))

    @client.event
    async def on_message(message: d.Message) -> None:
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = message.content
        channel = str(message.channel)

        logger.info(f"{log.INFO} [{channel}] {username}: '{user_message}'")
        await DiscordBot.send_message(message, user_message)
    
def main():
    client.run(token=token)
    bot = DiscordBot()

if __name__ == "__main__":
    main()