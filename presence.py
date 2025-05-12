from PyQt5 import QtCore, QtGui, QtWidgets
from database import get_employee_list, calculate_work_hours


class AttendanceWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.attendance_table = None
        self.date_edit = None
        self.main_layout = None
        self.central_widget = None
        self.setup_ui()
        self.load_attendance()

    def setup_ui(self):
        self.setWindowTitle("Gestion des Présences")
        self.resize(1000, 700)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.setup_date_controls()
        self.setup_attendance_table()

    def setup_date_controls(self):
        date_layout = QtWidgets.QHBoxLayout()

        self.date_edit = QtWidgets.QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QtCore.QDate.currentDate())
        date_layout.addWidget(QtWidgets.QLabel("Date :"))
        date_layout.addWidget(self.date_edit)

        search_btn = QtWidgets.QPushButton("Rechercher")
        search_btn.setStyleSheet("background-color: #2f89ff; color: white;")
        search_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        search_btn.clicked.connect(self.load_attendance)
        date_layout.addWidget(search_btn)

        self.main_layout.addLayout(date_layout)

    def setup_attendance_table(self):
        self.attendance_table = QtWidgets.QTableWidget()
        self.attendance_table.setColumnCount(6)
        self.attendance_table.setHorizontalHeaderLabels([
            "ID", "Nom", "Prénom", "Département", "Heures travaillées", "Statut"
        ])
        self.attendance_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.attendance_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.attendance_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.attendance_table.verticalHeader().setVisible(False)

        self.main_layout.addWidget(self.attendance_table)

    def load_attendance(self):
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")

        try:
            employees = get_employee_list()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement des employés : {e}")
            return

        if not employees:
            QtWidgets.QMessageBox.information(self, "Aucune donnée", "Aucun employé trouvé.")
            return

        self.attendance_table.setRowCount(len(employees))

        for row, emp in enumerate(employees):
            try:
                hours = calculate_work_hours(emp['employee_id'], selected_date) or "00:00"
            except Exception:
                hours = "00:00"

            status = "Présent" if hours != "00:00" else "Absent"

            self.attendance_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(emp['employee_id'])))
            self.attendance_table.setItem(row, 1, QtWidgets.QTableWidgetItem(emp['nom']))
            self.attendance_table.setItem(row, 2, QtWidgets.QTableWidgetItem(emp['prenom']))
            self.attendance_table.setItem(row, 3, QtWidgets.QTableWidgetItem(emp.get('department_name', '')))
            self.attendance_table.setItem(row, 4, QtWidgets.QTableWidgetItem(hours))

            status_item = QtWidgets.QTableWidgetItem(status)
            color = QtGui.QColor("#27ae60") if status == "Présent" else QtGui.QColor("#c0392b")
            status_item.setBackground(QtGui.QBrush(color))
            status_item.setForeground(QtGui.QBrush(QtCore.Qt.white))
            self.attendance_table.setItem(row, 5, status_item)


# Test rapide de la fenêtre si ce fichier est exécuté seul
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = AttendanceWindow()
    window.show()
    sys.exit(app.exec_())
