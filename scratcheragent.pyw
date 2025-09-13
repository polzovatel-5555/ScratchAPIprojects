import requests
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMessageBox
from requests.exceptions import JSONDecodeError

class MessageBox(QMessageBox):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.text_to_copy = message
        
        self.setWindowTitle('Уведомление')
        self.setText(message)
        self.setIcon(QMessageBox.Icon.Information)

        self.copy_button = QPushButton('Скопировать')
        self.addButton(self.copy_button, QMessageBox.ButtonRole.ActionRole)
        self.addButton(QMessageBox.StandardButton.Ok)

        self.copy_button.clicked.connect(self.copy_text)

    def copy_text(self):
        clipboard = QApplication.clipboard()
        if clipboard is None:
            QMessageBox.critical(self, "Ошибка!", "Невозможно скопировать текст на данной платформе.")
            return

        clipboard.setText(self.text_to_copy) # Копируем переданный текст

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Useragent')
        self.setGeometry(100, 100, 400, 100) # (x, y, ширина, высота)

        self.scratcher = QLineEdit()
        self.scratcher.setPlaceholderText('Имя скретчера...')
        self.button = QPushButton('Узнать')

        layout = QVBoxLayout()
        layout.addWidget(self.scratcher)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.find_user)

    def find_user(self):
        scratcher = self.scratcher.text()

        if not scratcher:
            QMessageBox.critical(self, "Ошибка!", "Поле ввода не может быть пустым.")
            return

        r = requests.get(f"https://api.scratch.mit.edu/users/{scratcher}/projects")
        if r.status_code != 200:
            QMessageBox.critical(self, "Ошибка!", "Такого скретчера не существует.")
            return

        j = r.json()
        if type(j) is not list or len(j) == 0:
            QMessageBox.critical(self, "Ошибка!", "У скретчера нету проектов.")
            return

        if 'id' not in j[0]:
            QMessageBox.critical(self, "Ошибка!", "Почему - не знаю!")
            return

        project_id = j[0]['id']

        r = requests.get(f"https://api.scratch.mit.edu/projects/{project_id}")

        if r.status_code != 200:
            QMessageBox.critical(self, "Ошибка!", "Почему - не знаю!")
            return

        j = r.json()
        if 'project_token' not in j:
            QMessageBox.critical(self, "Ошибка!", "Почему - не знаю!")
            return

        r = requests.get(f"https://projects.scratch.mit.edu/{project_id}?token={j['project_token']}")
        if r.status_code != 200:
            QMessageBox.critical(self, "Ошибка!", "Почему - не знаю!")
            return

        try:
            project = r.json()
        except JSONDecodeError:
            QMessageBox.critical(self, "Ошибка!", "Почему - не знаю!")
            return

        if 'meta' not in project or 'agent' not in project['meta']:
            QMessageBox.critical(self, "Ошибка!", "Проект сохранён в доисторической эре Scratch 2.0 или ниже. Невозможно получить User Agent")
            return

        msg_box = MessageBox(project["meta"]["agent"], self)
        msg_box.exec()
        
        self.scratcher.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
