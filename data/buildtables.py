from sqlalchemy import Table, Column, Integer, Float, String, Boolean, DateTime


class BuildTables:
    def __init__(self, metadata):
        self.metadata = metadata
        self.build_tables()

    def build_tables(self):
        Table(
            'npcs', self.metadata,
            Column('name', String),
            Column('zone', String),
            Column('expansion', String),
            Column('body_type', String),
            Column('class', String),
            Column('level', Integer)
        )
        Table(
            'friends', self.metadata,
            Column('name', String),
            Column('class', String),
            Column('level', Integer),
            Column('pet', String)
        )
