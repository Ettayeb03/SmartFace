from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from database import get_employee_list, search_employee, get_worked_hours_today, get_worked_hours_month

# Importer les autres interfaces
from frome import AddEmployeeWindow
from presence import AttendanceWindow
from affecterprojet import ProjectWindow


class UnifiedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartFace - Gestion RH")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: white;")
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)

        self.setup_sidebar()
        self.setup_content_area()

        self.load_employee_list()

        # Garde en mémoire les fenêtres secondaires
        self.add_window = None
        self.presence_window = None
        self.project_window = None

    def setup_sidebar(self):
        sidebar = QtWidgets.QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #2f89ff;")

        sidebar_layout = QtWidgets.QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(QtCore.Qt.AlignTop)

        buttons = [
            ("Liste Employee", self.load_employee_list),
            ("Ajouter Employee", self.show_add_employee),
            ("Rechercher Employé", self.setup_search_ui),
            ("Gestion Projects", self.show_projects),
            ("Présences", self.show_attendance)
        ]

        for text, callback in buttons:
            btn = QtWidgets.QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    background: transparent;
                    text-align: left;
                    padding: 10px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #1a73e8;
                }
            """)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            btn.clicked.connect(callback)
            sidebar_layout.addWidget(btn)

        self.main_layout.addWidget(sidebar)

    def setup_content_area(self):
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        self.main_layout.addWidget(self.content_widget)

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un employé...")
        self.search_input.setStyleSheet("padding: 5px; border: 1px solid #ddd; border-radius: 4px;")

        self.search_button = QtWidgets.QPushButton("Rechercher")
        self.search_button.setStyleSheet("background-color: #2f89ff; color: white; padding: 5px; border-radius: 4px;")
        self.search_button.clicked.connect(self.search_employees)

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        self.content_layout.addLayout(search_layout)

        self.employee_table = QtWidgets.QTableWidget()
        self.employee_table.setColumnCount(8)
        self.employee_table.setHorizontalHeaderLabels([
            "ID", "Nom", "Prénom", "Email", "Poste", "Département", "Heures Aujourd'hui", "Heures Mois"
        ])
        self.employee_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.employee_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.employee_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.content_layout.addWidget(self.employee_table)

    def clear_table(self):
        self.employee_table.setRowCount(0)

    def load_employee_list(self):
        self.clear_table()
        employees = get_employee_list() or []
        self.employee_table.setRowCount(len(employees))

        for row, emp in enumerate(employees):
            self.employee_table.setItem(row, 0, QTableWidgetItem(str(emp['employee_id'])))
            self.employee_table.setItem(row, 1, QTableWidgetItem(emp['nom']))
            self.employee_table.setItem(row, 2, QTableWidgetItem(emp['prenom']))
            self.employee_table.setItem(row, 3, QTableWidgetItem(emp['email']))
            self.employee_table.setItem(row, 4, QTableWidgetItem(emp['poste']))
            self.employee_table.setItem(row, 5, QTableWidgetItem(emp.get('department_name', '')))

            try:
                hours_today = get_worked_hours_today(emp['employee_id']) or "0"
                hours_month = get_worked_hours_month(emp['employee_id']) or "0"
            except Exception:
                hours_today = hours_month = "0"

            self.employee_table.setItem(row, 6, QTableWidgetItem(hours_today))
            self.employee_table.setItem(row, 7, QTableWidgetItem(hours_month))

    def search_employees(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            self.load_employee_list()
            return

        self.clear_table()
        results = search_employee(search_term) or []
        self.employee_table.setRowCount(len(results))

        for row, emp in enumerate(results):
            self.employee_table.setItem(row, 0, QTableWidgetItem(str(emp['employee_id'])))
            self.employee_table.setItem(row, 1, QTableWidgetItem(emp['nom']))
            self.employee_table.setItem(row, 2, QTableWidgetItem(emp['prenom']))
            self.employee_table.setItem(row, 3, QTableWidgetItem(emp['email']))
            self.employee_table.setItem(row, 4, QTableWidgetItem(emp['poste']))
            self.employee_table.setItem(row, 5, QTableWidgetItem(emp.get('department_name', '')))

            try:
                hours_today = get_worked_hours_today(emp['employee_id']) or "0"
                hours_month = get_worked_hours_month(emp['employee_id']) or "0"
            except Exception:
                hours_today = hours_month = "0"

            self.employee_table.setItem(row, 6, QTableWidgetItem(hours_today))
            self.employee_table.setItem(row, 7, QTableWidgetItem(hours_month))

    def setup_search_ui(self):
        self.search_input.clear()
        self.clear_table()

    def show_add_employee(self):
        if self.add_window is None:
            self.add_window = AddEmployeeWindow()
        self.add_window.show()

    def show_attendance(self):
        if self.presence_window is None:
            self.presence_window = AttendanceWindow()
        self.presence_window.show()

    def show_projects(self):
        if self.project_window is None:
            self.project_window = ProjectWindow()
        self.project_window.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = UnifiedApp()
    window.show()
    sys.exit(app.exec_())
