from PyQt5.QtWidgets import (QDialog, QLabel, QVBoxLayout, QPushButton,
                             QHBoxLayout, QLineEdit)
from PyQt5.QtGui import QFont
from GlobalVariables import GlobalSettings
from PyQt5.QtCore import Qt


class PassphraseDecDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint))
        self.setWindowTitle("Парольная фраза")
        self.resize(400, 200)

        layout = QVBoxLayout()

        label_passphrase = QLabel('Парольная фраза:')
        label_passphrase.setFont(QFont('Arial', 12))
        self.edit_passphrase = QLineEdit('')
        self.edit_passphrase.setFont(QFont('Arial', 12))
        self.edit_passphrase.setEchoMode(QLineEdit.Password)
        layout_passphrase = QHBoxLayout()
        layout_passphrase.addWidget(label_passphrase)
        layout_passphrase.addWidget(self.edit_passphrase)

        save_button = QPushButton("Ввод")
        save_button.setFont(QFont('Arial', 12))
        save_button.clicked.connect(self.save_click)
        cancel_button = QPushButton('Отмена')
        cancel_button.setFont(QFont('Arial', 12))
        cancel_button.clicked.connect(self.cancel_click)
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(save_button)
        layout_buttons.addWidget(cancel_button)

        layout.addLayout(layout_passphrase)
        layout.addLayout(layout_buttons)

        self.setLayout(layout)

    def save_click(self):
        GlobalSettings.passphrase = self.edit_passphrase.text()
        GlobalSettings.dec_state = True
        self.close()

    def cancel_click(self):
        GlobalSettings.dec_state = False
        self.close()
