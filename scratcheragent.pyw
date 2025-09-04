import requests
import json
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMessageBox
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
        self.button.clicked.connect(self.find)

    def find(self):
        scratcher = self.scratcher.text()

        if not scratcher:
            QMessageBox.critical(self, "Ошибка!", "Поле ввода не может быть пустым.")
        else:

            r1 = requests.get(f"https://api.scratch.mit.edu/users/{scratcher}/projects")
            if r1.status_code == 200:
                if r1.text == "[]":
                    QMessageBox.critical(self, "Ошибка!", "У скретчера нету проектов.")
                else:
                    j1 = r1.json()
                    r2 = requests.get(f"https://api.scratch.mit.edu/projects/{j1[0].get('id')}")
                    if r2.status_code == 200:
                        j2 = r2.json()
                        r3 = requests.get(f"https://projects.scratch.mit.edu/{j1[0].get('id')}?token={j2.get('project_token')}")
                        if r3.status_code == 200:
                            m = json.loads(r3.text)

                            msg_box = MessageBox(m.get("meta").get("agent"), self)
                            msg_box.exec()
                            
                            self.scratcher.clear()
                        else:
                            QMessageBox.critical(self, "Ошибка!", "Почему - не знаю!")
                    else:
                        QMessageBox.critical(self, "Ошибка!", "Почему - не знаю!")
                


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show() # Показываем окно
    sys.exit(app.exec())