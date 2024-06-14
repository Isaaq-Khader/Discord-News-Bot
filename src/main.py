from dotenv import load_dotenv
import discord as d
import logging
from logs import log
import os
from responses import ResponseHandler

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("RonBurgundy")

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
intents = d.Intents.default()
intents.message_content = True
client = d.Client(intents=intents)

class DiscordBot:
    async def process_and_send_message(message: d.Message, user_message: str) -> None:
        if not user_message:
            logger.warning(f"{log.WARN} Empty user message received")
            return
        
        try:
            response = await ResponseHandler.handle_response(message, user_message)
            if response:
                await message.channel.send(response)
        except Exception as e:
            logger.critical(f"{log.ERROR} {e}")

    @client.event
    async def on_ready() -> None:
        logger.info(f"{log.INFO} {client.user} is now running!")
        await client.change_presence(activity=d.Activity(type=d.ActivityType.streaming, name="current news"))

    @client.event
    async def on_message(message: d.Message) -> None:
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = message.content
        channel = str(message.channel)

        logger.info(f"{log.INFO} [{channel}] {username}: '{user_message}'")
        await DiscordBot.process_and_send_message(message, user_message)
    
def main():
    client.run(token=token)

if __name__ == "__main__":
    main()