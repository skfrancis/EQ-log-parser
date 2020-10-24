from data.database import Database
from pathlib import Path


class TriggerData:
    def __init__(self):
        self._db_file = Path.cwd() / 'config.db'
        self._database = Database(str(self._db_file.resolve()))
        self._table = 'triggers'

    def import_data(self):
        result = self._database.select(self._table)
