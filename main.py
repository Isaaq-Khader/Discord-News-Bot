import asyncio
from random import randint
from dotenv import load_dotenv
import discord as d
from discord.ext import commands
import logging
from src.bot import BotUtil
from src.dice import Dice
from src.help import Help
from src.logs import log
import os
from src.news import News

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("RonBurgundy")

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
intents = d.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=BotUtil.bot_prefix, intents=intents, help_command=None)

class DiscordBot:
    # Description: Processes a Discord message and checks whether this is a command or special term
    # Parameters: 
    #   - message: Discord message
    #   - user_input: User's message text
    # Returns: String of response to command or special term
    async def handle_response(message: d.Message, user_input: str) -> str:
        cannonball = "Ladies and gentlemen, can I please have your attention. I've just been handed an urgent and horrifying news story. I need all of you to stop what you're doing and listen. CANNONBALL!!"
        random_responses = ["I'm in a glass case of emotion!", 
                            "I'm very important. I have many leather-bound books and my apartment smells of rich mahogany.",
                            "You're so wise. You're like a miniature Buddha, covered in hair.",
                            "Knights of Columbus, that hurt.",
                            "You stay classy, San Diego.",
                            "By the beard of Zeus!",
                            cannonball]
        single_responses = {"cannonball":  cannonball,
                            "hello": "Hello there!",
                            "hey": "Hey there!",
                            "hi": "Hi there!",
                            "ron": "What is it?",}
        formatted_response = user_input.lower().split()
        logger.info(f"{log.DEBUG} Formatted response: {formatted_response}")

        possible_command = formatted_response[0].replace(BotUtil.bot_prefix, "")
        is_command = possible_command in BotUtil.supported_commands
        logger.debug(f"{log.DEBUG} Is a command? -- {is_command}")
        has_prefix = formatted_response[0].startswith(BotUtil.bot_prefix)
        logger.debug(f"{log.DEBUG} Has prefix? -- {has_prefix}")
        if is_command and has_prefix:
            attributes = formatted_response[1:]
            match possible_command:
                case "roll":
                    return Dice.roll_dice(attributes)
                case "news":
                    return await News.get_news(message, attributes)
                case "help":
                    help_class = Help(formatted_response)
                    return help_class.help_processor()
                case _:
                    return "That is currently not implemented. Try again later. Now shoo."

        for index, word in enumerate(formatted_response, 1):
            if word in single_responses:
                logger.debug(f"{log.DEBUG} Word Match for {word} at {index}")
                return single_responses[word]
        
        chance = randint(1, 10)
        logger.info(f"random number was {chance}")
        if chance == 3:
            return random_responses[randint(0, len(random_responses) - 1)]
        else:
            return ""

    # Description: Prepares to send a message to a discord channel
    # Parameters:
    #   - message: Discord message
    #   - user_input: User's message text
    # Returns: None
    async def process_and_send_message(message: d.Message, user_message: str) -> None:
        if not user_message:
            logger.warning(f"{log.WARN} Empty user message received")
            return
        try:
            response = await DiscordBot.handle_response(message, user_message)
            if type(response) == d.Embed:
                await message.channel.send(embed=response)
            elif response:
                await message.channel.send(response)
            else:
                logger.debug(f"{log.DEBUG} No coded response for the given message...")
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
        await DiscordBot.process_and_send_message(message, user_message)
    
async def load():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"cogs.{file[:-3]}")

async def main():
    await load()
    await client.start(token=token)

asyncio.run(main())