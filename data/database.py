from sqlalchemy import create_engine, MetaData
from data.buildtables import BuildTables


class Database:
    def __init__(self, db_file):
        self._db_file = db_file
        self._db_engine = self._connect()
        self._metadata = MetaData()

    def _connect(self):
        connect_string = 'sqlite:///' + self._db_file
        return create_engine(connect_string, echo=True)

    def create_tables(self):
        BuildTables(self._metadata)
        self._metadata.create_all(self._db_engine, checkfirst=True)
