from trackers.who.filters.whofilter import WhoFilter
from sqlalchemy import column


class WhoEvent:
    def __init__(self, database):
        self.database = database
        self.table = 'friends'
        self.filter = WhoFilter()

    def parse_event(self, data):
        event_data = self.filter.parse(data)
        if event_data:
            where_clause = (column('name').__eq__(event_data.get('name')))
            result = self.database.select(self.table, where_clause)

