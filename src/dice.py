import logging
from random import randint
from logs import log
import re

logger = logging.getLogger("Dice")

class Dice:
    def split_roll_text(roll: str):
        num = re.sub("[d][0-9]+", "", roll)
        logger.debug(f"{log.DEBUG} Number of Dice: {num}")

        die = re.sub("[0-9]+[d]", "", roll)
        logger.debug(f"{log.DEBUG} Die Used: {die}")

        return int(num), int(die)
    
    def roll_dice(attributes: list[str]) -> str:
        logger.debug(f"{log.DEBUG} Attributes to work with: {attributes}")
        for attribute in attributes:
            if re.search("[0-9]+[d][0-9]+", attribute):
                num, die = Dice.split_roll_text(attribute)
                total = 0
                for instance in range(num):
                    logger.debug(f"{log.DEBUG} Roll #{instance+1}")
                    total += randint(1, die)
                    logger.debug(f"{log.DEBUG} Current Total: {total}")
                return f"You rolled [{num}d{die}]: {total}"
        return "Not sure what you mean there buddy."
    
