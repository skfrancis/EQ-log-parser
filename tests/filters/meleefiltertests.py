import unittest
import datetime
from trackers.fights.filters.meleefilter import MeleeFilter


class MeleeFilterTest(unittest.TestCase):
    def test_no_match(self):
        melee_filter = MeleeFilter()
        data = {
            'timestamp': datetime.datetime(2020, 11, 1, 0, 13, 53),
            'text': 'Welcome to EverQuest!'
        }
        result = melee_filter.parse(data)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
