import logging
import sqlite3
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
    
    def handle_set(self, attributes: list[str]) -> str:
        try:
            channel = attributes[0]
            terms = " ".join(attributes[1:])
            self.write(channel, terms)
            return f"set channel {channel} with search terms: {terms}"
        except IndexError:
            logger.critical(f"{log.ERROR} User went out of bounds for setting up news.")
            return "Specify a channel to set the news up to, along with any key words to search for."
        except Exception as e:
            logger.critical(f"{log.ERROR} {e}")
            return ""