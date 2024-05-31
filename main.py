from dotenv import load_dotenv
from discord import Intents, Client, Message
import logging
import os
from responses import ResponseHandler
from typing import Final

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("NewsBot")

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

class logc:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class log:
    DEBUG = f"{logc.OKGREEN}{logc.BOLD}DEBUG{logc.ENDC} -"
    INFO = f"{logc.OKBLUE}{logc.BOLD}INFO{logc.ENDC} -"
    WARN = f"{logc.WARNING}{logc.BOLD}WARN{logc.ENDC} -"
    ERROR = f"{logc.FAIL}{logc.BOLD}ERROR{logc.ENDC} -"
    CRIT = f"{logc.FAIL}{logc.BOLD}CRITICAL{logc.ENDC} -"
    SUM = f"{logc.OKCYAN}{logc.BOLD}SUMMARY{logc.ENDC} -"

class DiscordBot:
    async def send_message(message: Message, user_message: str) -> None:
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
        logger.warning(f"{log.INFO} {client.user} is now running!")

    @client.event
    async def on_message(message: Message) -> None:
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