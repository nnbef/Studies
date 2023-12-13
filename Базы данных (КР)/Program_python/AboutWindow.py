from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint))
        self.setWindowTitle("О программе")
        self.resize(400, 300)

        layout = QVBoxLayout()

        label1 = QLabel("База данных отдела техобслуживания")
        label1.setFont(QFont('Arial', 14))
        label1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label2 = QLabel('Курсовая работа по дисциплине "Базы данных"\n'
                       'Работу выполнил студент группы А-13б-20\n'
                       'Бегунов Никита Сергеевич\n'
                       'Тема №19')
        label2.setFont(QFont('Arial', 10))
        layout.addWidget(label1)
        layout.addWidget(label2)

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
