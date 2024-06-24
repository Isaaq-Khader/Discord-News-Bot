import logging
from random import randint
from src.logs import log
import re

logger = logging.getLogger("Dice")

class Dice:
    def split_roll_text(roll: str) -> tuple[int, int, int]:
        modifier = re.sub("[0-9]+[d][0-9]+", "", roll)
        logger.debug(f"{log.DEBUG} Modifier regex result: {modifier}")
        if modifier:
            modifier = int(modifier)
            logger.debug(f"{log.DEBUG} Modifier used: {modifier}")
            num = re.sub("[d][0-9]+[+, -][0-9]+", "", roll)
            die = re.sub("[0-9]+[d]|[+, -][0-9]+", "", roll)
        else:
            logger.debug(f"{log.DEBUG} No modifier used.")
            modifier = 0
            num = re.sub("[d][0-9]+", "", roll)
            die = re.sub("[0-9]+[d]", "", roll)

        logger.debug(f"{log.DEBUG} Number of Dice: {num}")
        logger.debug(f"{log.DEBUG} Die Used: {die}")
        return int(num), int(die), modifier
    
    def roll_dice(attributes: list[str]) -> str:
        logger.debug(f"{log.DEBUG} Attributes to work with: {attributes}")
        for attribute in attributes:
            if re.search("[0-9]+[d][0-9]+", attribute):
                num, die, mod = Dice.split_roll_text(attribute)
                if not num or not die:
                    logger.debug(f"{log.DEBUG} no number of dice or die side found...")
                    return "You hooligan, the statement is not correct... please try again"
                if num > 100 or die > 100:
                    return "What am I, a wizard? I can't do that."
                total = mod
                logger.debug(f"{log.DEBUG} Initial Total: {total}")
                for instance in range(num):
                    logger.debug(f"{log.DEBUG} Roll #{instance+1}")
                    roll = randint(1, die)
                    total += roll
                    logger.debug(f"{log.DEBUG} Rolled: {roll}")
                    logger.debug(f"{log.DEBUG} Current Total: {total}")
                if roll == 1 and num == 1:
                    return "You rolled a Nat 1!"
                if total < 1:
                    total = 1
                if roll == die and num == 1:
                    return f"You rolled [{attribute}]: CRITICAL {total}!"
                return f"You rolled [{attribute}]: {total}"
        return ""
    
