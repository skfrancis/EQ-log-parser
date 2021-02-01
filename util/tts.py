import pyttsx3


class TTS:
    def __init__(self):
        self.engine = pyttsx3.init()

    def play(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def get_voices(self):
        voices_data = self.engine.getProperty('voices')
        voices = []
        # noinspection PyTypeChecker
        for voice_data in voices_data:
            voices.append({
                'id': voice_data.id,
                'name': voice_data.name
            })
        return voices

    def set_voice(self, voice_id):
        self.engine.setProperty('voice', voice_id)

    def set_volume(self, volume):
        self.engine.setProperty('volume', volume)

    def set_rate(self, rate):
        self.engine.setProperty('rate', rate)

    def get_voice(self):
        return self.engine.getProperty('voice')

    def get_volume(self):
        self.engine.getProperty('volume')

    def get_rate(self):
        self.engine.getProperty('rate')
