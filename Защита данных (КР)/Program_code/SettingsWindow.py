from PyQt5.QtWidgets import (QDialog, QLabel, QVBoxLayout, QPushButton,
                             QRadioButton, QHBoxLayout, QCheckBox,
                             QLineEdit, QMessageBox, QFileDialog, QButtonGroup)
from PyQt5.QtGui import QFont
from GlobalVariables import GlobalSettings
from PyQt5.QtCore import Qt


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint))
        self.setWindowTitle("Настройки")
        self.resize(400, 400)

        self.path_file_save = GlobalSettings.path_file_save

        layout = QVBoxLayout()

        label_mode = QLabel("Режим работы криптоалгоритма:")
        label_mode.setFont(QFont('Arial', 12))

        layout_radiobuttons_mods = QVBoxLayout()

        self.group_radiobutton_mods = QButtonGroup(exclusive=True)
        radiobutton_mods = QRadioButton('Режим электронной кодовой книги (ECB)')
        radiobutton_mods.setFont(QFont('Arial', 12))
        radiobutton_mods.setChecked(True if GlobalSettings.mode == 'ecb' else False)
        radiobutton_mods.mode = 'ecb'
        layout_radiobuttons_mods.addWidget(radiobutton_mods)
        self.group_radiobutton_mods.addButton(radiobutton_mods)

        radiobutton_mods = QRadioButton('Режим сцепления блоков шифротекста (CBC)')
        radiobutton_mods.setFont(QFont('Arial', 12))
        radiobutton_mods.setChecked(True if GlobalSettings.mode == 'cbc' else False)
        radiobutton_mods.mode = 'cbc'
        layout_radiobuttons_mods.addWidget(radiobutton_mods)
        self.group_radiobutton_mods.addButton(radiobutton_mods)

        radiobutton_mods = QRadioButton('Режим обратной связи по шифротексту (CFB)')
        radiobutton_mods.setFont(QFont('Arial', 12))
        radiobutton_mods.setChecked(True if GlobalSettings.mode == 'cfb' else False)
        radiobutton_mods.mode = 'cfb'
        layout_radiobuttons_mods.addWidget(radiobutton_mods)
        self.group_radiobutton_mods.addButton(radiobutton_mods)

        radiobutton_mods = QRadioButton('Режим обратной связи по выходу (OFB)')
        radiobutton_mods.setFont(QFont('Arial', 12))
        radiobutton_mods.setChecked(True if GlobalSettings.mode == 'ofb' else False)
        radiobutton_mods.mode = 'ofb'
        layout_radiobuttons_mods.addWidget(radiobutton_mods)
        self.group_radiobutton_mods.addButton(radiobutton_mods)
        self.group_radiobutton_mods.buttonClicked.connect(self.radiobutton_mods_clicked)

        label_settings_crypto = QLabel('Настройки криптоалгоритма')
        label_settings_crypto.setFont(QFont('Arial', 14))

        layout_radiobuttons_blocks = QHBoxLayout()

        label_blocks = QLabel('Длинна блока:')
        label_blocks.setFont(QFont('Arial', 12))
        layout_radiobuttons_blocks.addWidget(label_blocks)

        self.group_radiobutton_blocks = QButtonGroup(exclusive=True)
        radiobutton_blocks = QRadioButton('16')
        radiobutton_blocks.setFont(QFont('Arial', 12))
        radiobutton_blocks.setChecked(True if GlobalSettings.blocks == 16 else False)
        radiobutton_blocks.blocks = 16
        layout_radiobuttons_blocks.addWidget(radiobutton_blocks)
        self.group_radiobutton_blocks.addButton(radiobutton_blocks)

        radiobutton_blocks = QRadioButton('32')
        radiobutton_blocks.setFont(QFont('Arial', 12))
        radiobutton_blocks.setChecked(True if GlobalSettings.blocks == 32 else False)
        radiobutton_blocks.blocks = 32
        layout_radiobuttons_blocks.addWidget(radiobutton_blocks)
        self.group_radiobutton_blocks.addButton(radiobutton_blocks)

        radiobutton_blocks = QRadioButton('64')
        radiobutton_blocks.setFont(QFont('Arial', 12))
        radiobutton_blocks.setChecked(True if GlobalSettings.blocks == 64 else False)
        radiobutton_blocks.blocks = 64
        layout_radiobuttons_blocks.addWidget(radiobutton_blocks)
        self.group_radiobutton_blocks.addButton(radiobutton_blocks)
        self.group_radiobutton_blocks.buttonClicked.connect(self.radiobutton_blocks_clicked)

        layout_num_rounds = QHBoxLayout()
        label_num_rounds = QLabel('Число раундов:')
        label_num_rounds.setFont(QFont('Arial', 12))
        layout_num_rounds.addWidget(label_num_rounds)
        self.edit_num_rounds = QLineEdit(str(GlobalSettings.rounds))
        self.edit_num_rounds.setFont(QFont('Arial', 12))
        layout_num_rounds.addWidget(self.edit_num_rounds)

        layout_key_len = QHBoxLayout()
        label_key_len = QLabel('Длинна ключа:')
        label_key_len.setFont(QFont('Arial', 12))
        layout_key_len.addWidget(label_key_len)
        self.edit_key_len = QLineEdit(str(GlobalSettings.key_len))
        self.edit_key_len.setFont(QFont('Arial', 12))
        layout_key_len.addWidget(self.edit_key_len)

        label_restrictions = QLabel('Ограничения на парольную фразу')
        label_restrictions.setFont(QFont('Arial', 14))

        label_min_len = QLabel('Минимальная длинна:')
        label_min_len.setFont(QFont('Arial', 12))
        self.edit_min_len = QLineEdit(str(GlobalSettings.min_len))
        self.edit_min_len.setFont(QFont('Arial', 12))
        self.checkbox_lowercase = QCheckBox('Строчные буквы')
        self.checkbox_lowercase.setFont(QFont('Arial', 12))
        self.checkbox_lowercase.setCheckState(GlobalSettings.lowercase_letter)
        self.checkbox_uppercase = QCheckBox('Заглавные буквы')
        self.checkbox_uppercase.setFont(QFont('Arial', 12))
        self.checkbox_uppercase.setCheckState(GlobalSettings.uppercase_letter)
        self.checkbox_digits = QCheckBox('Цифры')
        self.checkbox_digits.setFont(QFont('Arial', 12))
        self.checkbox_digits.setCheckState(GlobalSettings.digits)
        self.checkbox_special_symbols = QCheckBox('Специальные символы')
        self.checkbox_special_symbols.setFont(QFont('Arial', 12))
        self.checkbox_special_symbols.setCheckState(GlobalSettings.special_symbols)
        self.checkbox_delete_after = QCheckBox('Удалить файл после операции')
        self.checkbox_delete_after.setFont(QFont('Arial', 12))
        self.checkbox_delete_after.setCheckState(GlobalSettings.delete_after)
        self.checkbox_save_result_in_file = QCheckBox('Сохранить результат в файл')
        self.checkbox_save_result_in_file.setFont(QFont('Arial', 12))
        self.checkbox_save_result_in_file.setCheckState(GlobalSettings.save_in_file)

        layout_path_file_save = QHBoxLayout()
        label_path_file_save = QLabel('Путь сохраниения файла:')
        label_path_file_save.setFont(QFont('Arial', 12))
        layout_path_file_save.addWidget(label_path_file_save)
        btn_path_file_save = QPushButton('Выбрать путь')
        btn_path_file_save.setFont(QFont('Arial', 12))
        btn_path_file_save.clicked.connect(self.btn_path_file_save_click)
        layout_path_file_save.addWidget(btn_path_file_save)
        self.label_path_file_save_global = QLabel(f'Выбран путь: {GlobalSettings.path_file_save}'
                                                  if GlobalSettings.path_file_save != '' else 'Путь не выбран')
        self.label_path_file_save_global.setFont(QFont('Arial', 12))

        layout_name_file_save = QHBoxLayout()
        label_name_file_save = QLabel('Имя файла для сохранения:')
        label_name_file_save.setFont(QFont('Arial', 12))
        layout_name_file_save.addWidget(label_name_file_save)
        self.edit_name_file_save = QLineEdit(GlobalSettings.name_file_save)
        self.edit_name_file_save.setFont(QFont('Arial', 12))
        layout_name_file_save.addWidget(self.edit_name_file_save)

        save_button = QPushButton("Сохранить")
        save_button.setFont(QFont('Arial', 12))
        save_button.clicked.connect(self.save_click)

        layout.addWidget(label_settings_crypto)
        layout.addWidget(label_mode)
        layout.addLayout(layout_radiobuttons_mods)
        layout.addLayout(layout_radiobuttons_blocks)
        layout.addLayout(layout_num_rounds)
        layout.addLayout(layout_key_len)
        layout.addWidget(label_restrictions)
        layout_min_len = QHBoxLayout()
        layout_min_len.addWidget(label_min_len)
        layout_min_len.addWidget(self.edit_min_len)
        layout.addLayout(layout_min_len)
        layout.addWidget(self.checkbox_lowercase)
        layout.addWidget(self.checkbox_uppercase)
        layout.addWidget(self.checkbox_digits)
        layout.addWidget(self.checkbox_special_symbols)
        layout.addWidget(self.checkbox_delete_after)
        layout.addWidget(self.checkbox_save_result_in_file)
        layout.addLayout(layout_path_file_save)
        layout.addWidget(self.label_path_file_save_global)
        layout.addLayout(layout_name_file_save)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_click(self):
        try:
            rounds = int(self.edit_num_rounds.text())
            if 0 <= rounds <= 255:
                GlobalSettings.rounds = rounds
            else:
                raise Exception('Неверное значение')
        except Exception:
            QMessageBox.about(self, 'Ошибка', 'Неправильное значение в поле количества раундов\n'
                                              'Количество раудов должно быть от 0 до 255')
            return
        try:
            GlobalSettings.min_len = int(self.edit_min_len.text())
        except Exception:
            QMessageBox.about(self, 'Ошибка', 'Неправильное значение в поле минимальной длинны')
            return
        try:
            key_len = int(self.edit_key_len.text())
            if 0 <= key_len <= 2040:
                GlobalSettings.key_len = key_len
            else:
                raise Exception('Неверное значение')
        except Exception:
            QMessageBox.about(self, 'Ошибка', 'Неправильное значение в поле длинны ключа\n'
                                              'Длинна ключа должна быть от 0 до 2040')
            return
        GlobalSettings.lowercase_letter = self.checkbox_lowercase.checkState()
        GlobalSettings.uppercase_letter = self.checkbox_uppercase.checkState()
        GlobalSettings.digits = self.checkbox_digits.checkState()
        GlobalSettings.special_symbols = self.checkbox_special_symbols.checkState()
        GlobalSettings.delete_after = self.checkbox_delete_after.checkState()
        GlobalSettings.save_in_file = self.checkbox_save_result_in_file.checkState()
        GlobalSettings.path_file_save = self.path_file_save
        GlobalSettings.name_file_save = self.edit_name_file_save.text()
        if GlobalSettings.save_in_file and (GlobalSettings.path_file_save == '' or GlobalSettings.name_file_save == ''):
            QMessageBox.about(self, 'Ошибка', 'Не выбран путь или имя сохранения файла')
            return
        if GlobalSettings.save_in_file and GlobalSettings.name_file_save.find('.') == -1:
            QMessageBox.about(self, 'Ошибка', 'Неправильно имя сохранения файла')
            return
        self.close()

    @staticmethod
    def radiobutton_blocks_clicked(btn):
        GlobalSettings.blocks = btn.blocks

    @staticmethod
    def radiobutton_mods_clicked(btn):
        GlobalSettings.mode = btn.mode

    def btn_path_file_save_click(self):
        self.path_file_save = QFileDialog.getExistingDirectory()
        self.label_path_file_save_global.setText(f'Выбран путь: {self.path_file_save}'
                                                 if self.path_file_save != '' else 'Путь не выбран')
