from sqlalchemy import create_engine, MetaData, Table
from data.buildtables import BuildTables


class Database:
    def __init__(self, db_file):
        self._db_file = db_file
        self._db_engine = self._connect()
        self._metadata = MetaData()
        self._create_tables()

    def _connect(self):
        connect_string = 'sqlite:///' + self._db_file
        return create_engine(connect_string, echo=True)

    def _create_tables(self):
        BuildTables(self._metadata)
        self._metadata.create_all(self._db_engine, checkfirst=True)

    def select(self, table, where_clause=None):
        db_table = Table(table, self._metadata, autoload=True, autoload_with=self._db_engine)
        return self._db_engine.execute(db_table.select(whereclause=where_clause))

    def insert(self, table, data):
        db_table = Table(table, self._metadata, autoload=True, autoload_with=self._db_engine)
        return self._db_engine.execute(db_table.insert(), data)

    def update(self, table, values, where_clause=None):
        db_table = Table(table, self._metadata, autoload=True, autoload_with=self._db_engine)
        return self._db_engine.execute(db_table.update(whereclause=where_clause, values=values))

    def delete(self, table, where_clause=None):
        db_table = Table(table, self._metadata, autoload=True, autoload_with=self._db_engine)
        self._db_engine.execute(db_table.delete(whereclause=where_clause))

