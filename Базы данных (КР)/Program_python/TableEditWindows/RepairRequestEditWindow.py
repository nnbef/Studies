from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
import psycopg2


class RepairRequestEditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5432/course_work_db')
        self.index_column = 0

        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint))
        self.setWindowTitle("Просмотр и изменение заявок на ремонт")
        self.resize(800, 600)

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM repair_request ORDER BY id_request')
        self.rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()

        layout = QVBoxLayout()

        self.table = QTableWidget(cursor.rowcount, len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.itemChanged.connect(self.item_changed)
        layout.addWidget(self.table)

        layout_buttons = QHBoxLayout()
        add_line_button = QPushButton('Добавить строку')
        add_line_button.clicked.connect(self.add_line_btn_clicked)
        layout_buttons.addWidget(add_line_button)
        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.save_btn_clicked)
        layout_buttons.addWidget(save_button)
        layout.addLayout(layout_buttons)

        self.setLayout(layout)

        for i in range(len(self.rows)):
            for j in range(len(columns)):
                item = QTableWidgetItem(str(self.rows[i][j]))
                if j == self.index_column:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

    def add_line_btn_clicked(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        try:
            if row_position == 0:
                pred_index = 0
            else:
                pred_index = int(self.table.item(row_position-1, 0).text())
            item = QTableWidgetItem(str(pred_index + 1))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_position, 0, item)
        except:
            pass

    def item_changed(self):
        self.table.resizeColumnsToContents()

    def save_btn_clicked(self):
        try:
            data = []
            for r in range(self.table.rowCount()):
                row = []
                for c in range(self.table.columnCount()):
                    row.append(self.table.item(r, c).text())
                data.append(row)
            for r in range(len(self.rows)):
                the_same = True
                for c in range(len(self.rows[r])):
                    if str(data[r][c]) != str(self.rows[r][c]):
                        the_same = False
                if not the_same:
                    cur = self.conn.cursor()
                    cur.execute(f"""UPDATE repair_request SET status='{data[r][1]}',
                                    request_time='{data[r][2]}', id_technique={data[r][3]},
                                    id_rep_type={data[r][4]}, id_executor={data[r][5]}
                                    id_branch={data[r][6]} WHERE id_request={data[r][0]}""")
                    self.conn.commit()
                    cur.close()
            if len(self.rows) < len(data):
                for r in range(len(self.rows), len(data)):
                    cur = self.conn.cursor()
                    cur.execute(f"""INSERT INTO repair_request
                                (status, request_time, id_technique, id_rep_type, id_executor, id_branch)
                                VALUES ('{data[r][1]}', '{data[r][2]}', {data[r][3]},
                                {data[r][4]}, {data[r][5]}, {data[r][6]})""")
                    self.conn.commit()
                    cur.close()
            QMessageBox.about(self, 'Изменения сохранены', 'Изменения успешно сохранены')
        except:
            QMessageBox.about(self, 'Ошибка', 'Неверное значение в таблице')
