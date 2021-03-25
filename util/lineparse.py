from datetime import datetime


# Parse assumes log file line format of: [Sat Sep 19 00:08:48 2020] Welcome to EverQuest!
def line_parse(line):
    data = {}
    if line:
        if line.startswith('[') and line.find(']') != -1:
            line = line.rstrip('\n')
            index = line.find(']') + 1
            try:
                data['timestamp'] = datetime.strptime(line[:index], '[%a %b %d %H:%M:%S %Y]')
            except ValueError:
                return data
            try:
                data['text'] = line.split('] ', 1)[1]
            except IndexError:
                return {}
    return data
