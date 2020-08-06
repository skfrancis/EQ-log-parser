from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QCheckBox, QDialogButtonBox
from PyQt5.QtWidgets import QApplication
import sys


class TriggerDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self._id = data.get('id')
        self._name = QLineEdit(data.get('name'))
        self._search_text = QLineEdit(data.get('search_text'))
        self._alert_text = QLineEdit(data.get('alert_text'))
        self._use_audio = QCheckBox()
        self._use_audio.setChecked(data.get('use_audio'))
        self._file_name = QLineEdit(data.get('file_name'))
        self._button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.create_gui()

    def create_gui(self):
        self.setWindowTitle('Trigger Editor')
        form_layout = QFormLayout()
        form_layout.addRow('Name:', self._name)
        form_layout.addRow('Search Text:', self._search_text)
        form_layout.addRow('Alert Text:', self._alert_text)
        form_layout.addRow('Use Audio:', self._use_audio)
        form_layout.addRow('Audio File:', self._file_name)
        form_layout.addRow(self._button_box)
        self.setLayout(form_layout)
        self.show()

    def _save(self):
        data = {
            'name': self._name.text(),
            'search_text': self._search_text.text(),
            'alert_text': self._alert_text.text(),
            'use_audio': self._use_audio.isChecked(),
            'file_name': self._file_name.text()
        }
        return data


# Remove when done testing
if __name__ == '__main__':
    app = QApplication(sys.argv)
    trigger = {
        'id': 123,
        'name': 'Feign Death',
        'search_text': '^You begin casting Feign Death',
        'alert_text': 'Casted Feign Death',
        'use_audio': True,
        'audio_file': 'testing'
    }
    window = TriggerDialog(None, trigger)
    sys.exit(app.exec_())
