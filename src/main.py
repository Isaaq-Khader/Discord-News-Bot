from random import randint
from dotenv import load_dotenv
import discord as d
import logging
from dice import Dice
from help import Help
from logs import log
import os
from news import News

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("RonBurgundy")

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
intents = d.Intents.default()
intents.message_content = True
client = d.Client(intents=intents)

class DiscordBot:
    async def handle_response(message: d.Message, user_input: str) -> str:
        cannonball = "Ladies and gentlemen, can I please have your attention. I've just been handed an urgent and horrifying news story. I need all of you to stop what you're doing and listen. CANNONBALL!!"
        help_text = "COMING SOON!"
        commands = ["roll",
                    "news",
                    "help"]
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
                            "hi": "Hi there!",}
        formatted_response = user_input.lower().split()
        logger.debug(f"{log.DEBUG} Formatted response: {formatted_response}")

        for index, word in enumerate(formatted_response):
            if word in single_responses:
                logger.debug(f"{log.DEBUG} Word Match for {word}")
                return single_responses[word]
            if word in commands:
                attributes = formatted_response[index:]
                match word:
                    case "roll":
                        return Dice.roll_dice(attributes)
                    case "news":
                        return await News.get_news(message, attributes)
                    case "help":
                        return Help.help_processor(attributes)
                    
        chance = randint(1, 10)
        logger.info(f"random number was {chance}")
        if chance == 3:
            return random_responses[randint(0, len(random_responses) - 1)]
        else:
            return

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
        News(client) # begins daily news


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