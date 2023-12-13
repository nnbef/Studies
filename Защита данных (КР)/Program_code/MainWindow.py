from PyQt5.QtWidgets import (QTextEdit, QWidget, QPushButton, QFileDialog,
                             QMainWindow, QAction, QVBoxLayout,
                             QHBoxLayout, QMessageBox, QLabel)
from SettingsWindow import SettingsDialog
from PassphraseEncWindow import PassphraseEncDialog
from PassphraseDecWindow import PassphraseDecDialog
from AboutWindow import AboutDialog
from PyQt5.QtGui import QFont
from GlobalVariables import GlobalSettings
from PyQt5.QtCore import Qt
from RC5 import RC5
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RC5')
        self.resize(800, 500)

        self.file_encrypt = 0
        self.file_decrypt = 0

        GlobalSettings.blocks = 32
        GlobalSettings.mode = 'ecb'
        GlobalSettings.passphrase = ''
        GlobalSettings.key_len = 128
        GlobalSettings.path_file_save = ''
        GlobalSettings.name_file_save = 'result.txt'
        GlobalSettings.enc_state = False
        GlobalSettings.dec_state = False

        label_text = QLabel('Шифрование текста')
        label_text.setFont(QFont('Arial', 14))
        label_text.setAlignment(Qt.AlignHCenter)
        label_file = QLabel('Шифрование файла')
        label_file.setFont(QFont('Arial', 14))
        label_file.setAlignment(Qt.AlignHCenter)

        self.edit_encrypt_text = QTextEdit('Текст для шифрования')
        self.edit_encrypt_text.setFont(QFont('Arial', 12))
        self.edit_decrypt_text = QTextEdit('Текст для расшифрования')
        self.edit_decrypt_text.setFont(QFont('Arial', 12))

        button_encrypt_text = QPushButton('Шифровать текст →')
        button_encrypt_text.setFont(QFont('Arial', 12))
        button_encrypt_text.clicked.connect(self.click_encrypt_text)
        button_decrypt_text = QPushButton('← Расшифровать текст')
        button_decrypt_text.setFont(QFont('Arial', 12))
        button_decrypt_text.clicked.connect(self.click_decrypt_text)

        button_select_encrypt_file = QPushButton('Выбрать файл для шифрования')
        button_select_encrypt_file.setFont(QFont('Arial', 12))
        button_select_encrypt_file.clicked.connect(self.click_select_enc_file)
        button_select_decrypt_file = QPushButton('Выбрать файл для расшифрования')
        button_select_decrypt_file.setFont(QFont('Arial', 12))
        button_select_decrypt_file.clicked.connect(self.click_select_dec_file)

        self.label_select_encrypt_file = QLabel('Файл не выбран')
        self.label_select_encrypt_file.setFont(QFont('Arial', 12))
        self.label_select_encrypt_file.setAlignment(Qt.AlignHCenter)
        self.label_select_decrypt_file = QLabel('Файл не выбран')
        self.label_select_decrypt_file.setFont(QFont('Arial', 12))
        self.label_select_decrypt_file.setAlignment(Qt.AlignHCenter)

        label_result_file = QLabel('Результат:')
        label_result_file.setFont(QFont('Arial', 12))
        self.edit_result_file = QTextEdit('Тут будет результат шифрования (расшифрования) файла')
        self.edit_result_file.setFont(QFont('Arial', 12))

        button_encrypt_file = QPushButton('Зашифровать файл')
        button_encrypt_file.setFont(QFont('Arial', 12))
        button_encrypt_file.clicked.connect(self.click_enc_file)
        button_decrypt_file = QPushButton('Расшифровать файл')
        button_decrypt_file.setFont(QFont('Arial', 12))
        button_decrypt_file.clicked.connect(self.click_dec_file)

        layout = QVBoxLayout()
        layout_text = QHBoxLayout()
        layout_text.addWidget(self.edit_encrypt_text)
        layout_text.addWidget(self.edit_decrypt_text)

        layout_buttons_text = QHBoxLayout()
        layout_buttons_text.addWidget(button_encrypt_text)
        layout_buttons_text.addWidget(button_decrypt_text)

        layout_encrypt_file = QVBoxLayout()
        layout_encrypt_file.addWidget(button_select_encrypt_file)
        layout_encrypt_file.addWidget(self.label_select_encrypt_file)
        layout_decrypt_file = QVBoxLayout()
        layout_decrypt_file.addWidget(button_select_decrypt_file)
        layout_decrypt_file.addWidget(self.label_select_decrypt_file)
        layout_file = QHBoxLayout()
        layout_file.addLayout(layout_encrypt_file)
        layout_file.addLayout(layout_decrypt_file)

        layout.addWidget(label_text)
        layout.addLayout(layout_text)

        layout.addLayout(layout_buttons_text)
        layout.addWidget(label_file)
        layout.addLayout(layout_file)
        layout_result_file = QHBoxLayout()
        layout_result_file.addWidget(label_result_file)
        layout_result_file.addWidget(self.edit_result_file)
        layout.addLayout(layout_result_file)
        layout_buttons_file = QHBoxLayout()
        layout_buttons_file.addWidget(button_encrypt_file)
        layout_buttons_file.addWidget(button_decrypt_file)
        layout.addLayout(layout_buttons_file)

        self.setLayout(layout)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.create_menu_bar()

    def click_enc_file(self):
        pew = PassphraseEncDialog()
        pew.exec_()
        rc5 = RC5(GlobalSettings.blocks, GlobalSettings.rounds, GlobalSettings.passphrase,
                  GlobalSettings.key_len, GlobalSettings.mode)
        if not GlobalSettings.enc_state:
            return
        try:
            if GlobalSettings.save_in_file:
                try:
                    with open(GlobalSettings.path_file_save + '/' + GlobalSettings.name_file_save, 'w') as file:
                        file.write(rc5.encrypt_file(self.file_encrypt).decode(encoding='cp1251'))
                    QMessageBox.about(self, 'Файл сохранен', 'Файл успешно сохранен')
                except FileNotFoundError:
                    QMessageBox.about(self, 'Ошибка', 'Ошибка при создании файла')
                    return
            else:
                self.edit_result_file.setText(rc5.encrypt_file(self.file_encrypt).decode(encoding='cp1251'))
            if GlobalSettings.delete_after \
                    and (GlobalSettings.path_file_save + '/' + GlobalSettings.name_file_save) != self.file_encrypt:
                os.remove(self.file_encrypt)
        except Exception:
            QMessageBox.about(self, 'Ошибка', 'Что-то пошло не так')

    def click_dec_file(self):
        pdw = PassphraseDecDialog()
        pdw.exec_()
        rc5 = RC5(GlobalSettings.blocks, GlobalSettings.rounds, GlobalSettings.passphrase,
                  GlobalSettings.key_len, GlobalSettings.mode)
        if not GlobalSettings.dec_state:
            return
        try:
            if GlobalSettings.save_in_file:
                try:
                    with open(GlobalSettings.path_file_save + '/' + GlobalSettings.name_file_save, 'w') as file:
                        file.write(rc5.decrypt_file(self.file_decrypt).decode(encoding='cp1251'))
                    QMessageBox.about(self, 'Файл сохранен', 'Файл успешно сохранен')
                except FileNotFoundError:
                    QMessageBox.about(self, 'Ошибка', 'Ошибка при создании файла')
                    return
            else:
                self.edit_result_file.setText(rc5.decrypt_file(self.file_decrypt).decode(encoding='cp1251'))
            if GlobalSettings.delete_after \
                    and (GlobalSettings.path_file_save + '/' + GlobalSettings.name_file_save) != self.file_decrypt:
                os.remove(self.file_decrypt)
        except Exception as exc:
            if exc.args[0] == '':
                QMessageBox.about(self, 'Ошибка', 'Что-то пошло не так')
            else:
                QMessageBox.about(self, 'Ошибка', exc.args[0])

    def click_encrypt_text(self):
        pew = PassphraseEncDialog()
        pew.exec_()
        rc5 = RC5(GlobalSettings.blocks, GlobalSettings.rounds, GlobalSettings.passphrase,
                  GlobalSettings.key_len, GlobalSettings.mode)
        if not GlobalSettings.enc_state:
            return
        try:
            if GlobalSettings.save_in_file:
                try:
                    with open(GlobalSettings.path_file_save + '/' + GlobalSettings.name_file_save, 'w') as file:
                        file.write(rc5.encrypt_bytes(self.edit_encrypt_text.toPlainText().encode(encoding='cp1251'))
                                   .decode(encoding='cp1251'))
                    QMessageBox.about(self, 'Файл сохранен', 'Файл успешно сохранен')
                except FileNotFoundError:
                    QMessageBox.about(self, 'Ошибка', 'Ошибка при создании файла')
                    return
            else:
                self.edit_decrypt_text.setText(rc5.encrypt_bytes(
                    self.edit_encrypt_text.toPlainText().encode(encoding='cp1251')).decode(encoding='cp1251'))
        except Exception:
            QMessageBox.about(self, 'Ошибка', 'Что-то пошло не так')

    def click_decrypt_text(self):
        pdw = PassphraseDecDialog()
        pdw.exec_()
        rc5 = RC5(GlobalSettings.blocks, GlobalSettings.rounds, GlobalSettings.passphrase,
                  GlobalSettings.key_len, GlobalSettings.mode)
        if not GlobalSettings.dec_state:
            return
        try:
            if GlobalSettings.save_in_file:
                try:
                    with open(GlobalSettings.path_file_save + '/' + GlobalSettings.name_file_save, 'w') as file:
                        file.write(rc5.decrypt_bytes(self.edit_decrypt_text.toPlainText().encode(encoding='cp1251'))
                                   .decode(encoding='cp1251'))
                    QMessageBox.about(self, 'Файл сохранен', 'Файл успешно сохранен')
                except FileNotFoundError:
                    QMessageBox.about(self, 'Ошибка', 'Ошибка при создании файла')
                    return
            else:
                self.edit_encrypt_text.setText(rc5.decrypt_bytes(
                    self.edit_decrypt_text.toPlainText().encode(encoding='cp1251')).decode(encoding='cp1251'))
        except Exception as exc:
            if exc.args[0] == '':
                QMessageBox.about(self, 'Ошибка', 'Что-то пошло не так')
            else:
                QMessageBox.about(self, 'Ошибка', exc.args[0])

    def click_select_enc_file(self):
        try:
            self.file_encrypt = QFileDialog.getOpenFileName()[0]
            self.label_select_encrypt_file.setText(self.file_encrypt)
        except Exception:
            return

    def click_select_dec_file(self):
        try:
            self.file_decrypt = QFileDialog.getOpenFileName()[0]
            self.label_select_decrypt_file.setText(self.file_decrypt)
        except Exception:
            return

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Программа")
        settings_action = QAction('Настройки', self)
        settings_action.triggered.connect(self.settings_action)
        close_action = QAction('Выход', self)
        close_action.triggered.connect(self.close_action)

        file_menu.addAction(settings_action)
        file_menu.addAction(close_action)

        help_menu = menu_bar.addMenu("Помощь")
        about = QAction('О программе', self)
        about.triggered.connect(self.about_action)
        help_menu.addAction(about)

    @staticmethod
    def close_action():
        exit()

    @staticmethod
    def about_action():
        about = AboutDialog()
        about.exec_()

    @staticmethod
    def settings_action():
        settings = SettingsDialog()
        settings.exec_()
