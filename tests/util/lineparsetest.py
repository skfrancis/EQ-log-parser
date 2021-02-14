import unittest
import datetime
from util.lineparse import line_parse


class LineParseTest(unittest.TestCase):
    def test_official_format(self):
        text = '[Sat Sep 19 00:08:48 2020] Welcome to EverQuest!'
        result = line_parse(text)
        self.assertIsInstance(result.get('timestamp'), datetime.datetime)
        self.assertEqual(result.get('text'), 'Welcome to EverQuest!')

    def test_empty_line(self):
        text = ''
        result = line_parse(text)
        self.assertDictEqual(result, {})
        text = None
        result = line_parse(text)
        self.assertDictEqual(result, {})

    def test_blank_text(self):
        text = '[Sat Sep 19 00:08:48 2020] '
        result = line_parse(text)
        self.assertIsInstance(result.get('timestamp'), datetime.datetime)
        self.assertEqual(result.get('text'), '')

    def test_blank_date(self):
        text = '[] Welcome to EverQuest!'
        result = line_parse(text)
        self.assertDictEqual(result, {})

    def test_invalid_line(self):
        text = '[ Welcome to EverQuest!'
        result = line_parse(text)
        self.assertDictEqual(result, {})
        text = '] Welcome to EverQuest!'
        result = line_parse(text)
        self.assertDictEqual(result, {})
        text = '[]Welcome to EverQuest!'
        result = line_parse(text)
        self.assertDictEqual(result, {})
        text = '[Welcome to EverQuest!'
        result = line_parse(text)
        self.assertDictEqual(result, {})
        text = ']Welcome to EverQuest!'
        result = line_parse(text)
        self.assertDictEqual(result, {})
        text = 'Welcome to EverQuest!'
        result = line_parse(text)
        self.assertDictEqual(result, {})


if __name__ == '__main__':
    unittest.main()
