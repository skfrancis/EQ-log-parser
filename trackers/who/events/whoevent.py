from filters.filters import WhoFilter
from sqlalchemy import column


class WhoEvent:
    def __init__(self, database):
        self.database = database
        self.table = 'friends'
        self.filter = WhoFilter()

    def parse_event(self, data):
        event_data = self.filter.parse(data)
        if event_data:
            data = {
                'name': event_data.get('Name'),
                'class': event_data.get('Class'),
                'level':  int(event_data.get('Level')) if event_data.get('Level') is not None else None
            }
            where_clause = (column('name').__eq__(event_data.get('Name')))
            result = self.database.select(self.table, where_clause).first()
            if result:
                current_data = dict(result)
                data['pet'] = current_data.get('pet')
                if current_data == data:
                    return result
                else:
                    # TODO: Update data if different
                    pass
            else:
                self.database.insert(self.table, data)
                print('Added Friend: {}'.format(event_data.get('Name')))
