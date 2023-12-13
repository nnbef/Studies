from PyQt5.QtWidgets import (QDialog, QVBoxLayout,
                             QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt
import psycopg2


class RequestsDeadlineDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/course_work_db')

        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint))
        self.setWindowTitle("Заявки с превышением нормативного срока")
        self.resize(1300, 600)

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM get_requests_deadline()')
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()

        layout = QVBoxLayout()

        self.table = QTableWidget(cursor.rowcount, len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        layout.addWidget(self.table)

        self.setLayout(layout)

        for i in range(len(rows)):
            for j in range(len(columns)):
                item = QTableWidgetItem(str(rows[i][j]))
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
