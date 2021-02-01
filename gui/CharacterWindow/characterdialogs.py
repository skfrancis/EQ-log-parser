from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QLabel, QDial, QFormLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon
from pathlib import Path
from util.tts import TTS
# Remove when done testing
from PyQt5.QtWidgets import QApplication
import sys


class CharacterDialog(QDialog):
    def __init__(self, parent, character_data):
        super().__init__(parent)
        self.character_data = character_data
        self.tts = TTS()
        voice_data = self.tts.get_voices()
        voice_names = [item['name'] for item in voice_data]
        # self.path = self.parent().path / 'img'
        self.log_file = QLineEdit(self.character_data.get('LogFile', ''))
        self.profile = QLineEdit(self.character_data.get('Profile', ''))
        self.character = QLineEdit(self.character_data.get('Character', ''))
        self.voices = QComboBox()
        self.voices.addItems(voice_names)
        self.volume = QDial()
        self.volume.setRange(0, 100)
        self.volume.setValue(self.character_data.get('Volume', 100))
        self.volume_value = QLabel(str(self.volume.value()))
        self.rate = QDial()
        self.rate.setRange(1, 400)
        self.rate.setValue(self.character_data.get('Rate', 200))
        self.rate_value = QLabel(str(self.rate.value()))
        self.phonetic = QLineEdit(self.character_data.get('Phonetic', ''))
        self.create_gui()

    def create_gui(self):
        self.setWindowTitle('Character Profile')
        # icon_path = self.path / 'profile.png'
        # icon = QIcon(str(icon_path.resolve()))
        # self.setWindowIcon(icon)
        form_layout = QFormLayout()
        form_layout.addRow('Log File:', self.log_file)
        form_layout.addRow('Profile Name:', self.profile)
        form_layout.addRow('Character Name:', self.character)
        form_layout.addRow('Phonetic Name:', self.phonetic)
        form_layout.addRow('Voice', self.voices)
        dial_labels = QHBoxLayout()
        volume_label = QLabel('Voice Volume')
        volume_label.setAlignment(Qt.AlignCenter)
        rate_label = QLabel('Voice Speed')
        rate_label.setAlignment(Qt.AlignCenter)
        dial_labels.addWidget(volume_label)
        dial_labels.addWidget(rate_label)
        dial_layout = QHBoxLayout()
        dial_layout.addWidget(self.volume)
        dial_layout.addWidget(self.rate)

        self.volume_value.setAlignment(Qt.AlignCenter)
        self.volume.valueChanged.connect(self.update_volume_label)

        self.rate_value.setAlignment(Qt.AlignCenter)
        self.rate.valueChanged.connect(self.update_rate_label)

        value_layout = QHBoxLayout()
        value_layout.addWidget(self.volume_value)
        value_layout.addWidget(self.rate_value)
        form_layout.addRow(dial_labels)
        form_layout.addRow(dial_layout)
        form_layout.addRow(value_layout)
        self.setLayout(form_layout)
        self.show()

    @pyqtSlot()
    def save(self):
        self.character_data = {
            'LogFile': self.log_file.text(),
            'Profile': self.profile.text(),
            'Character': self.character.text(),
            'Phonetic': self.phonetic.text(),
            'Voice': self.voices.currentText(),
            'Volume': self.volume.value(),
            'Rate': self.rate.value()
        }
        self.accept()

    @pyqtSlot()
    def update_volume_label(self):
        self.volume_value.setText(str(self.volume.value()))

    @pyqtSlot()
    def update_rate_label(self):
        self.rate_value.setText(str(self.rate.value()))


App = QApplication(sys.argv)
window = CharacterDialog(None, {})
sys.exit(App.exec())
