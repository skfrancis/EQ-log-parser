import unittest
import datetime
from trackers.fights.filters.spellfilter import SpellFilter


class SpellFilterTest(unittest.TestCase):
    def test_no_match(self):
        spell_filter = SpellFilter()
        data = {
            'timestamp': datetime.datetime(2020, 11, 1, 0, 13, 53),
            'text': 'Welcome to EverQuest!'
        }
        result = spell_filter.parse(data)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
