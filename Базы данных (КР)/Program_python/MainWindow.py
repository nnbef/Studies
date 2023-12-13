from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QVBoxLayout
from AboutWindow import AboutDialog
from TableEditWindows.BranchEditWindow import BranchEditDialog
from TableEditWindows.DepartmentEditWindow import DepartmentEditDialog
from TableEditWindows.ExecutorEditWindow import ExecutorEditDialog
from TableEditWindows.RepairRequestEditWindow import RepairRequestEditDialog
from TableEditWindows.RepairTypeEditWindow import RepairTypeEditDialog
from TableEditWindows.TechniqueEditWindow import TechniqueEditDialog
from TableEditWindows.TechniqueTypeEditWindow import TechniqueTypeEditDialog
from ReportWindows.RequestsWindow import RequestsDialog
from ReportWindows.RequestsByExecutorWindow import RequestsByExecutorDialog
from ReportWindows.RequestsByTypeWindow import RequestsByTypeDialog
from ReportWindows.RequestsDeadlineWindow import RequestsDeadlineDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('База данных отдела техобслуживания')
        self.resize(800, 500)

        layout = QVBoxLayout()

        self.setLayout(layout)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('Программа')
        close_action = QAction('Выход', self)
        close_action.triggered.connect(self.close_action)
        file_menu.addAction(close_action)

        tables_edit = menu_bar.addMenu('Таблицы')
        table_branch = QAction('Филиалы', self)
        table_branch.triggered.connect(self.table_branch_edit_action)
        tables_edit.addAction(table_branch)
        table_department = QAction('Отделы', self)
        table_department.triggered.connect(self.table_department_edit_action)
        tables_edit.addAction(table_department)
        table_technique_type = QAction('Типы техники', self)
        table_technique_type.triggered.connect(self.table_tec_type_edit_action)
        tables_edit.addAction(table_technique_type)
        table_technique = QAction('Техника', self)
        table_technique.triggered.connect(self.table_technique_edit_action)
        tables_edit.addAction(table_technique)
        table_executor = QAction('Исполнители', self)
        table_executor.triggered.connect(self.table_executor_edit_action)
        tables_edit.addAction(table_executor)
        table_repair_type = QAction('Типы ремонтов', self)
        table_repair_type.triggered.connect(self.table_repair_type_edit_action)
        tables_edit.addAction(table_repair_type)
        table_repair_request = QAction('Заявки на ремонт', self)
        table_repair_request.triggered.connect(self.table_repair_request_edit_action)
        tables_edit.addAction(table_repair_request)

        reports = menu_bar.addMenu('Отчеты')
        table_requests = QAction('Заявки на ремонтные работы', self)
        table_requests.triggered.connect(self.table_requests_action)
        reports.addAction(table_requests)
        table_requests_by_executor = QAction('Контроль выполнения заявок по исполнителям', self)
        table_requests_by_executor.triggered.connect(self.table_requests_by_executor_action)
        reports.addAction(table_requests_by_executor)
        table_requests_deadline = QAction('Заявки с превышением нормативного срока', self)
        table_requests_deadline.triggered.connect(self.table_requests_deadline_action)
        reports.addAction(table_requests_deadline)
        table_requests_by_type = QAction('Заявки заданного типа', self)
        table_requests_by_type.triggered.connect(self.table_requests_by_type_action)
        reports.addAction(table_requests_by_type)

        help_menu = menu_bar.addMenu('Помощь')
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
    def table_branch_edit_action():
        br = BranchEditDialog()
        br.exec_()

    @staticmethod
    def table_department_edit_action():
        dep = DepartmentEditDialog()
        dep.exec_()

    @staticmethod
    def table_tec_type_edit_action():
        tt = TechniqueTypeEditDialog()
        tt.exec_()

    @staticmethod
    def table_technique_edit_action():
        tec = TechniqueEditDialog()
        tec.exec_()

    @staticmethod
    def table_executor_edit_action():
        executor = ExecutorEditDialog()
        executor.exec_()

    @staticmethod
    def table_repair_type_edit_action():
        rep_type = RepairTypeEditDialog()
        rep_type.exec_()

    @staticmethod
    def table_repair_request_edit_action():
        rep_request = RepairRequestEditDialog()
        rep_request.exec_()

    @staticmethod
    def table_requests_action():
        rd = RequestsDialog()
        rd.exec_()

    @staticmethod
    def table_requests_by_executor_action():
        rbed = RequestsByExecutorDialog()
        rbed.exec_()

    @staticmethod
    def table_requests_deadline_action():
        rdd = RequestsDeadlineDialog()
        rdd.exec_()

    @staticmethod
    def table_requests_by_type_action():
        rbtd = RequestsByTypeDialog()
        rbtd.exec_()
