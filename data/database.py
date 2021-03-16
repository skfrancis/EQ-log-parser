from sqlalchemy import create_engine, MetaData, Table
from data.buildtables import BuildTables


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.db_engine = self.connect()
        self.metadata = MetaData()
        self.create_tables()

    def connect(self):
        connect_string = 'sqlite:///' + self.db_file
        return create_engine(connect_string, echo=False)

    def create_tables(self):
        BuildTables(self.metadata)
        self.metadata.create_all(self.db_engine, checkfirst=True)

    def select(self, table, where_clause=None):
        db_table = Table(table, self.metadata, autoload=True, autoload_with=self.db_engine)
        return self.db_engine.execute(db_table.select(whereclause=where_clause))

    def insert(self, table, data):
        db_table = Table(table, self.metadata, autoload=True, autoload_with=self.db_engine)
        return self.db_engine.execute(db_table.insert(), data)

    def update(self, table, values, where_clause=None):
        db_table = Table(table, self.metadata, autoload=True, autoload_with=self.db_engine)
        return self.db_engine.execute(db_table.update(whereclause=where_clause, values=values))

    def delete(self, table, where_clause=None):
        db_table = Table(table, self.metadata, autoload=True, autoload_with=self.db_engine)
        self.db_engine.execute(db_table.delete(whereclause=where_clause))
