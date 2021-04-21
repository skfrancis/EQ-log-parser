import datetime

from util.lineparse import line_parse


class TestLineParse:
    def test_line_parse_working_line(self):
        parse_line = line_parse('[Sat Jan 31 23:59:59 2020] Welcome to EverQuest!')
        assert type(parse_line) == dict
        assert type(parse_line.get('timestamp')) == datetime.datetime
        assert type(parse_line.get('text')) == str

    def test_line_parse_empty_date(self):
        assert line_parse('[]') == {}

    def test_line_parse_empty_string(self):
        assert line_parse('') == {}

    def test_line_parse_no_str(self):
        assert line_parse(None) == {}

    def test_line_parse_just_date(self):
        assert (line_parse('[Sat Jan 1 00:00:00 2000]')) == {}
