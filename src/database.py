import logging
import sqlite3
from src.bot import BotUtil
from src.logs import log

logger = logging.getLogger("News Database")

database = sqlite3.connect("dailynews.db")
cursor = database.cursor()
database.execute("CREATE TABLE IF NOT EXISTS dailynews(channel_id INT, key_terms STRING)")

class DatabaseNews:
    def __init__(self) -> None:
        pass

    # Description: Reads data from dailynews database.
    # Parameters: None
    # Returns: List of data
    def read(self) -> list[any]:
        query = "SELECT * FROM dailynews"
        data = cursor.execute(query).fetchall()
        return data

    # Description: Reads the current search terms for a given channel ID.
    # Parameters:
    #   - channel_id: ID of channel to be searched
    # Returns: List of data
    def read_channel_terms(self, channel_id: int) -> list[any]:
        query = "SELECT * FROM dailynews WHERE channel_id = ?"
        data = cursor.execute(query, (channel_id,)).fetchall()
        return data
    
    # Description: Reads all channel IDs from dailynews database.
    # Parameters: None
    # Returns: List of channel IDs
    def get_channel_ids(self) -> list[any]:
        query = "SELECT channel_id FROM dailynews"
        data = cursor.execute(query).fetchall()
        return data
    
    # Description: Reads all key terms from dailynews database
    # Parameters: None
    # Returns: List of key terms
    def get_key_terms(self) -> list[any]:
        query = "SELECT key_terms FROM dailynews"
        data = cursor.execute(query).fetchall()
        return data

    # Description: Writes a new search query for a given channel ID.
    # Parameters:
    #   - channel_id: ID of channel
    #   - key_terms: Search term
    # Returns: Acknowledgement of addition.
    def write(self, channel_id: int, key_terms: str) -> str:
        query = "INSERT INTO dailynews VALUES(?, ?)"
        cursor.execute(query, (channel_id, key_terms,))
        database.commit()
        return "Another guaranteed viewer. Excellent."
        
    # Description: Deletes all search terms for a given channel ID.
    # Parameters:
    #   - channel_id: ID of channel
    # Returns: Acknowledgement of deletion.
    def delete(self, channel_id: int) -> str:
        query = "DELETE FROM dailynews WHERE channel_id = ?"
        cursor.execute(query, (channel_id,))
        database.commit()
        return "Very sad to see you go. Darn hooligans."
    
    # Description: Deletes a search term for a given channel ID.
    # Parameters:
    #   - channel_id: ID of channel
    #   - key: Search term
    # Returns: Acknowledgement of deletion.
    def delete_key_term(self, channel_id: str, key: str) -> str:
        if not key:
            return "No search term was given. Provide a search term to remove."
        logger.debug(f"{log.DEBUG} Remove Channel ID: {channel_id}")
        logger.debug(f"{log.DEBUG} Remove Search Term: {key}")
        query = "DELETE FROM dailynews WHERE channel_id = ? AND key_terms = ?"
        cursor.execute(query, (channel_id, key.lower(),))
        database.commit()
        return "Very sad to see you go. Darn hooligans." # TODO: see if it can validate the removal
    
    # Description: Attempts to set a channel ID with the specified search term
    # Parameters:
    #   - attributes: List of strings containing parameters from the user
    # Returns: Acknowledgement of setting new search term.
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