import pyttsx3


class TTS:
    def __init__(self):
        self._engine = pyttsx3.init()

    def play(self, text):
        self._engine.say(text)
        self._engine.runAndWait()

    def get_voices(self):
        voices_data = self._engine.getProperty('voices')
        voices = []
        # noinspection PyTypeChecker
        for voice_data in voices_data:
            voices.append({
                'id': voice_data.id,
                'name': voice_data.name
            })
        return voices

    def set_voice(self, voice_id):
        self._engine.setProperty('voice', voice_id)
