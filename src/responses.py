import logging
from random import randint
import discord
from logs import log
from news import News
from dice import Dice

logger = logging.getLogger("ResponseHandler")

class ResponseHandler: 
    async def handle_response(message: discord.Message, user_input: str) -> str:
        cannonball = "Ladies and gentlemen, can I please have your attention. I've just been handed an urgent and horrifying news story. I need all of you to stop what you're doing and listen. CANNONBALL!!"
        help_text = "COMING SOON!"
        commands = ["roll",
                    "news"]
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
                            "help": help_text}
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
        chance = randint(1, 10)
        logger.info(f"random number was {chance}")
        if chance == 3:
            return random_responses[randint(0, len(random_responses) - 1)]
        else:
            return