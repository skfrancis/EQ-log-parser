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
            Column('text', String(1000))
        )
        Table(
            'triggers', self._metadata,
            Column('name', String(500), primary_key=True),
            Column('search_text', String(500)),
            Column('alert_text', String(500)),
            Column('use_audio', Boolean)
        )



