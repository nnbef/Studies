from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt
import psycopg2


class RequestsByExecutorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/course_work_db')

        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint))
        self.setWindowTitle("Контроль выполнения заявок по исполнителям")
        self.resize(1300, 600)

        layout = QVBoxLayout()

        layout_enter_executor = QHBoxLayout()
        label_executor = QLabel('ФИО исполнителя: ')
        layout_enter_executor.addWidget(label_executor)
        self.executor_edit = QLineEdit()
        layout_enter_executor.addWidget(self.executor_edit)
        btn_enter_executor = QPushButton('Ввод')
        btn_enter_executor.clicked.connect(self.btn_enter_executor_action)
        layout_enter_executor.addWidget(btn_enter_executor)
        layout.addLayout(layout_enter_executor)

        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def btn_enter_executor_action(self):
        cursor = self.conn.cursor()
        cursor.execute(f"""SELECT * FROM get_requests_by_executor('{self.executor_edit.text()}')""")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        self.table.setRowCount(cursor.rowcount)
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        for i in range(len(rows)):
            for j in range(len(columns)):
                item = QTableWidgetItem(str(rows[i][j]))
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()
        cursor.close()
