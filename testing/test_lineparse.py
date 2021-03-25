import datetime
from pathlib import Path

from util.lineparse import line_parse


def load_test_log():
    cwd = Path.cwd()
    log_file = cwd / 'eqlog_Testchar_testserver.txt'
    with log_file.open('r', encoding="utf8") as file:
        lines = file.readlines()
        return lines


def test_line_parse():
    data = load_test_log()
    for line in data:
        parse_line = line_parse(line)
        assert type(parse_line) == dict
        assert type(parse_line.get('timestamp')) == datetime.datetime
        assert type(parse_line.get('text')) == str
    assert line_parse('[]') == {}
    assert line_parse('') == {}
    assert line_parse(None) == {}
    assert (line_parse('[Sat Jan 1 00:00:00 2000]')) == {}
