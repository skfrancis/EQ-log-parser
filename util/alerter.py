import re
from util.tts import TTS


class Alerter:
    def __init__(self, triggers):
        self._triggers = triggers
        self._tts = TTS()

    def search(self, text):
        for trigger in self._triggers:
            if re.search(trigger.get('search_text'), text):
                self._alert(trigger)
                return trigger.get('alert_text')
            else:
                continue

    def _alert(self, trigger):
        if trigger.get('use_audio'):
            self._tts.play(trigger.get('audio_file'))
