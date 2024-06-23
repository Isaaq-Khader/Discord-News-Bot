import logging
import sqlite3
from bot import BotUtil
from logs import log

logger = logging.getLogger("News Database")

database = sqlite3.connect("dailynews.db")
cursor = database.cursor()
database.execute("CREATE TABLE IF NOT EXISTS dailynews(channel_id INT, key_terms STRING)")

class DatabaseNews:
    def __init__(self) -> None:
        pass

    def read(self):
        query = "SELECT * FROM dailynews"
        data = cursor.execute(query).fetchall()
        return data

    def read_channel_terms(self, channel_id: int):
        query = "SELECT * FROM dailynews WHERE channel_id = ?"
        data = cursor.execute(query, (channel_id,)).fetchall()
        return data
    
    def get_channel_ids(self):
        query = "SELECT channel_id FROM dailynews"
        data = cursor.execute(query).fetchall()
        return data
    
    def get_key_terms(self):
        query = "SELECT key_terms FROM dailynews"
        data = cursor.execute(query).fetchall()
        return data

    def write(self, channel_id: int, key_terms: str) -> str:
        query = "INSERT INTO dailynews VALUES(?, ?)"
        cursor.execute(query, (channel_id, key_terms,))
        database.commit()
        return "Another guaranteed viewer. Excellent."
        
    def delete(self, channel_id: int) -> str:
        query = "DELETE FROM dailynews WHERE channel_id = ?"
        cursor.execute(query, (channel_id,))
        database.commit()
        return "Very sad to see you go. Darn hooligans."
    
    def delete_key_term(self, channel_id: str, key: str) -> str:
        if not key:
            return "No search term was given. Provide a search term to remove."
        logger.debug(f"{log.DEBUG} Remove Channel ID: {channel_id}")
        logger.debug(f"{log.DEBUG} Remove Search Term: {key}")
        query = "DELETE FROM dailynews WHERE channel_id = ? AND key_terms = ?"
        cursor.execute(query, (channel_id, key.lower(),))
        database.commit()
        return "Very sad to see you go. Darn hooligans." # TODO: see if it can validate the removal
    
    def handle_set(self, attributes: list[str]) -> str:
        try:
            channel = attributes[0]
            logger.debug(f"{log.DEBUG} Channel ID: {channel}")
            if BotUtil.verify_channel(channel):
                logger.debug(f"{log.DEBUG} Valid channel, adding to database...")
                terms = " ".join(attributes[1:])
                self.write(channel, terms)
                return f"Set channel {channel} with search terms: {terms}"
            else:
                logger.critical(f"{log.ERROR} Invalid channel given!")
                return "Improper channel ID given."
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for setting up news.")
            return "Specify a channel to set the news up to, along with any key words to search for."
        except Exception as e:
            logger.critical(f"{log.ERROR} {e}")
            return ""