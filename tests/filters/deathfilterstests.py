import unittest
import datetime
from trackers.fights.filters.deathfilter import DeathFilter


class DeathFiltersTest(unittest.TestCase):
    def test_self_kill(self):
        death_filter = DeathFilter()
        data = {
            'timestamp': datetime.datetime(2020, 11, 1, 0, 13, 53),
            'text': 'You have slain Burynai Excavator!'
        }
        result = death_filter.parse(data)
        self.assertIsInstance(result.get('timestamp'), datetime.datetime)
        self.assertEqual(result.get('source'), 'You')
        self.assertEqual(result.get('target'), 'Burynai Excavator')
        self.assertEqual(result.get('amount'), 'death')
        self.assertIsNone(result.get('attack'))
        self.assertIsNone(result.get('damagemod'))
        self.assertEqual(result.get('debug'), data.get('text'))

    def test_self_died(self):
        death_filter = DeathFilter()
        data = {
            'timestamp': datetime.datetime(2020, 11, 1, 0, 13, 53),
            'text': 'You have been slain by Burynai Excavator!'
        }
        result = death_filter.parse(data)
        self.assertIsInstance(result.get('timestamp'), datetime.datetime)
        self.assertEqual(result.get('source'), 'Burynai Excavator')
        self.assertEqual(result.get('target'), 'You')
        self.assertEqual(result.get('amount'), 'death')
        self.assertIsNone(result.get('attack'))
        self.assertIsNone(result.get('damagemod'))
        self.assertEqual(result.get('debug'), data.get('text'))

    def test_other_kill(self):
        death_filter = DeathFilter()
        data = {
            'timestamp': datetime.datetime(2020, 11, 1, 0, 13, 53),
            'text': 'A moss snake has been slain by Rarshaak!'
        }
        result = death_filter.parse(data)
        self.assertIsInstance(result.get('timestamp'), datetime.datetime)
        self.assertEqual(result.get('source'), 'Rarshaak')
        self.assertEqual(result.get('target'), 'A moss snake')
        self.assertEqual(result.get('amount'), 'death')
        self.assertIsNone(result.get('attack'))
        self.assertIsNone(result.get('damagemod'))
        self.assertEqual(result.get('debug'), data.get('text'))

    def test_no_kill(self):
        death_filter = DeathFilter()
        data = {
            'timestamp': datetime.datetime(2020, 11, 1, 0, 13, 53),
            'text': 'Rarshaak died.'
        }
        result = death_filter.parse(data)
        self.assertIsInstance(result.get('timestamp'), datetime.datetime)
        self.assertEqual(result.get('source'), 'Rarshaak')
        self.assertEqual(result.get('target'), 'Rarshaak')
        self.assertEqual(result.get('amount'), 'death')
        self.assertIsNone(result.get('attack'))
        self.assertIsNone(result.get('damagemod'))
        self.assertEqual(result.get('debug'), data.get('text'))

    def test_no_match(self):
        death_filter = DeathFilter()
        data = {
            'timestamp': datetime.datetime(2020, 11, 1, 0, 13, 53),
            'text': 'Welcome to EverQuest!'
        }
        result = death_filter.parse(data)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
