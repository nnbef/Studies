from PyQt5.QtWidgets import (QDialog, QLabel, QVBoxLayout, QPushButton,
                             QHBoxLayout, QLineEdit, QMessageBox)
from PyQt5.QtGui import QFont
from GlobalVariables import GlobalSettings
from PyQt5.QtCore import Qt


class PassphraseEncDialog(QDialog):
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

        label_comfirm = QLabel('Подтверждение:   ')
        label_comfirm.setFont(QFont('Arial', 12))
        self.edit_comfirm = QLineEdit('')
        self.edit_comfirm.setFont(QFont('Arial', 12))
        self.edit_comfirm.setEchoMode(QLineEdit.Password)
        layout_comfirm = QHBoxLayout()
        layout_comfirm.addWidget(label_comfirm)
        layout_comfirm.addWidget(self.edit_comfirm)

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
        layout.addLayout(layout_comfirm)
        layout.addLayout(layout_buttons)

        self.setLayout(layout)

    def save_click(self):
        if (pass_phrase := self.edit_passphrase.text()) != self.edit_comfirm.text():
            QMessageBox.about(self, 'Ошибка', 'Парольные фразы должны совпадать!')
            return
        if GlobalSettings.lowercase_letter and pass_phrase.upper() == pass_phrase:
            QMessageBox.about(self, 'Не выполнено ограничение на парольную фразу',
                              'В парольной фразе должны быть строчные символы!')
            return
        if GlobalSettings.uppercase_letter and pass_phrase.lower() == pass_phrase:
            QMessageBox.about(self, 'Не выполнено ограничение на парольную фразу',
                              'В парольной фразе должны быть заглавные символы!')
            return
        if GlobalSettings.digits and not any(ch.isdigit() for ch in pass_phrase):
            QMessageBox.about(self, 'Не выполнено ограничение на парольную фразу',
                              'В парольной фразе должны быть цифры!')
            return
        if GlobalSettings.special_symbols and not any(ch in pass_phrase for ch in '!@#$%№^&?./*\()-_=+[]{}"`~:;<>| '):
            QMessageBox.about(self, 'Не выполнено ограничение на парольную фразу',
                              'В парольной фразе должны быть специальные символы!')
            return
        if len(pass_phrase) < GlobalSettings.min_len:
            QMessageBox.about(self, 'Не выполнено ограничение на парольную фразу',
                              'Длинна парольной фразы меньше допустимой!')
            return
        GlobalSettings.passphrase = pass_phrase
        GlobalSettings.enc_state = True
        self.close()

    def cancel_click(self):
        GlobalSettings.enc_state = False
        self.close()
