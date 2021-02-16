from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QLabel, QDial, QFormLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QFileDialog
from PyQt5.QtCore import Qt, QDir, pyqtSlot
from PyQt5.QtGui import QIcon
from pathlib import Path
from util.tts import TTS
import re
# TODO: Remove when done testing
from PyQt5.QtWidgets import QApplication
import sys


# TODO: Populate Values correctly on opening
class CharacterDialog(QDialog):
    def __init__(self, parent, character_data):
        super().__init__(parent)
        self.character_data = character_data
        self.tts = TTS()
        self.voice_data = self.tts.get_voices()
        voice_names = [item['name'] for item in self.voice_data]
        # self.path = self.parent().path / 'img'
        self.path = Path("D:\Projects\EQ-log-parser\img")
        self.game_directory = QLineEdit(self.character_data.get('game_directory', ''))
        self.directory_button = QPushButton()
        self.log_file = QComboBox()
        # self.log_file = QLineEdit(self.character_data.get('Log_file', ''))
        self.server_name = QLineEdit(self.character_data.get('server_name', ''))
        self.character = QLineEdit(self.character_data.get('character', ''))
        self.voices = QComboBox()
        self.voices.addItems(voice_names)
        self.volume = QDial()
        self.volume.setRange(0, 100)
        self.volume.setValue(self.character_data.get('volume', 100))
        self.volume_value = QLabel(str(self.volume.value()))
        self.rate = QDial()
        self.rate.setRange(1, 400)
        self.rate.setValue(self.character_data.get('rate', 200))
        self.rate_value = QLabel(str(self.rate.value()))
        self.phonetic = QLineEdit(self.character_data.get('phonetic', ''))
        self.phonetic_button = QPushButton()
        self.create_gui()

    def create_gui(self):
        self.setWindowTitle('Character Profile')
        icon_path = self.path / 'profile.png'
        icon = QIcon(str(icon_path.resolve()))
        self.setWindowIcon(icon)
        form_layout = QFormLayout()

        directory_layout = QHBoxLayout()
        directory_label = QLabel('Game Directory:')
        directory_icon_path = self.path / 'folder.png'
        directory_icon = QIcon(str(directory_icon_path.resolve()))
        self.directory_button.setIcon(directory_icon)
        self.directory_button.setFocusPolicy(Qt.NoFocus)
        self.directory_button.clicked.connect(self.get_game_directory)
        directory_layout.addWidget(directory_label)
        directory_layout.addWidget(self.game_directory)
        directory_layout.addWidget(self.directory_button)

        form_layout.addRow(directory_layout)
        self.log_file.currentIndexChanged.connect(self.update_log_file)
        form_layout.addRow('Log File:', self.log_file)
        self.server_name.setDisabled(True)
        form_layout.addRow('Server Name:', self.server_name)
        self.character.setDisabled(True)
        form_layout.addRow('Character Name:', self.character)

        phonetic_layout = QHBoxLayout()
        phonetic_label = QLabel('Phonetic Name:')
        phonetic_icon_path = self.path / 'speaker.png'
        phonetic_icon = QIcon(str(phonetic_icon_path.resolve()))

        self.phonetic_button.setIcon(phonetic_icon)
        self.phonetic_button.setFocusPolicy(Qt.NoFocus)
        self.phonetic_button.clicked.connect(self.play_phonetic_name)
        phonetic_layout.addWidget(phonetic_label)
        phonetic_layout.addWidget(self.phonetic)
        phonetic_layout.addWidget(self.phonetic_button)
        form_layout.addRow(phonetic_layout)

        self.voices.currentIndexChanged.connect(self.update_voice)
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
            'game_directory': self.game_directory.text(),
            'log_file': self.log_file.text(),
            'server_name': self.server_name.text(),
            'character': self.character.text(),
            'phonetic': self.phonetic.text(),
            'voice': self.voices.currentText(),
            'volume': self.volume.value(),
            'rate': self.rate.value()
        }
        self.accept()

    @pyqtSlot()
    def update_volume_label(self):
        self.volume_value.setText(str(self.volume.value()))
        self.tts.set_volume(self.volume.value())

    @pyqtSlot()
    def update_rate_label(self):
        self.rate_value.setText(str(self.rate.value()))
        self.tts.set_rate(self.rate.value())

    @pyqtSlot()
    def update_voice(self):
        name = self.voices.currentText()
        for voice in self.voice_data:
            if voice.get('name') == name:
                self.tts.set_voice(voice.get('id'))

    @pyqtSlot()
    def get_game_directory(self):
        directory_path = self.game_directory.text()
        dialog_icon_path = self.path / 'eq-icon.png'
        dialog_icon = QIcon(str(dialog_icon_path.resolve()))
        dialog = QFileDialog()
        dialog.setWindowIcon(dialog_icon)
        directory = QFileDialog.getExistingDirectory(self, 'Select Everquest Directory', directory_path)
        if directory:
            directory = QDir.toNativeSeparators(directory)
            self.game_directory.setText(directory)
            path = Path(directory) / 'Logs'
            files = []
            for file in path.glob('eqlog_*_*.txt'):
                files.append(file.name)
            self.log_file.addItems([file for file in files])

    def update_log_file(self):
        file_selected = self.log_file.currentText()
        expression = re.compile(r"^eqlog_(\w+)_(\w+).txt$")
        result = re.search(expression, file_selected)
        if result:
            self.server_name.setText(result.group(2).capitalize())
            self.character.setText(result.group(1).capitalize())
            self.phonetic.setText(result.group(1).capitalize())

    def play_phonetic_name(self):
        name = self.phonetic.text()
        self.tts.play(name)


# TODO: Remove when done testing
App = QApplication(sys.argv)
window = CharacterDialog(None, {})
sys.exit(App.exec())
