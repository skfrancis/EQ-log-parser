from gtts import gTTS
from pathlib import Path
from hashlib import md5
from time import localtime
from playsound import playsound

SUFFIX = '.mp3'
DIRECTORY = 'sounds'


class TTS:
    def __init__(self):
        self._path = Path.cwd() / DIRECTORY
        if not self._path.exists():
            self._path.mkdir(parents=False)

    def play(self, file_name):
        file_path = self._path / file_name
        file_path = str(file_path.resolve())
        playsound(file_path)

    def convert(self, text, file_name=None):
        tts = gTTS(text, lang='en')
        if not file_name:
            file_name = md5(str(localtime()).encode('utf-8')).hexdigest() + SUFFIX
        file_path = self._path / file_name
        file_path = str(file_path.resolve())
        tts.save(file_path)
        return file_name

