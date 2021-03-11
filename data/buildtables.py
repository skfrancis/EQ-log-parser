from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime


class BuildTables:
    def __init__(self, metadata):
        self._metadata = metadata
        self._build_tables()

    def _build_tables(self):
        Table(
            'logs', self._metadata,
            Column('id', Integer, primary_key=True),
            Column('timestamp', DateTime),
            Column('text', String(500))
        )




