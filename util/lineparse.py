from datetime import datetime
from pathlib import Path


# Parse assumes log file line format ofx: [Sat Sep 19 00:08:48 2020] Welcome to EverQuest!
def line_parse(line):
    data = {}
    if line.startswith('[') and line.find(']') != -1:
        line = line.rstrip('\n')
        index = line.find(']') + 1
        data['timestamp'] = datetime.strptime(line[:index], '[%a %b %d %H:%M:%S %Y]')
        data['text'] = line.split('] ', 1)[1]
    return data
