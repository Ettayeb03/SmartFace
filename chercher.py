from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView
import dashboard
import frome
from frome import presence
from database import search_employee, get_worked_hours_today, get_worked_hours_month


class EmployeeSearchUI(object):
    """Interface pour la recherche d'employés"""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("EmployeeSearchWindow")
        MainWindow.resize(1200, 600)
        MainWindow.setStyleSheet("background-color: #ffffff;")

        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        MainWindow.setCentralWidget(self.central_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self._setup_navbar()
        self._setup_search_area()
        self._setup_result_table()
        self._setup_menu_bar(MainWindow)
        self._setup_status_bar(MainWindow)

        self._connect_signals()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _setup_navbar(self):
        self.navbar_frame = QtWidgets.QFrame(self.central_widget)
        self.navbar_frame.setFixedWidth(160)
        self.navbar_frame.setStyleSheet("background-color: #2f89ff;")

        self.navbar_layout = QtWidgets.QVBoxLayout(self.navbar_frame)
        self.navbar_layout.setContentsMargins(10, 20, 10, 20)
        self.navbar_layout.setSpacing(15)

        button_style = """
            QPushButton {
                border: none;
                color: white;
                background-color: transparent;
                padding: 10px;
                text-align: left;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1a73e8;
            }
        """

        self.btn_list = QtWidgets.QPushButton("Liste des employés")
        self.btn_add = QtWidgets.QPushButton("Ajouter employé")
        self.btn_search = QtWidgets.QPushButton("Rechercher employé")
        self.btn_attendance = QtWidgets.QPushButton("Présences")

        for button in [self.btn_list, self.btn_add, self.btn_search, self.btn_attendance]:
            button.setStyleSheet(button_style)
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.navbar_layout.addWidget(button)

        self.main_layout.addWidget(self.navbar_frame, alignment=QtCore.Qt.AlignLeft)

    def _setup_search_area(self):
        self.search_frame = QtWidgets.QFrame(self.central_widget)
        self.search_frame.setStyleSheet("padding: 20px;")

        self.search_layout = QtWidgets.QHBoxLayout(self.search_frame)
        self.search_layout.setContentsMargins(0, 0, 0, 0)

        self.search_field = QtWidgets.QLineEdit()
        self.search_field.setPlaceholderText("Rechercher par nom, prénom ou ID...")
        self.search_field.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                min-width: 300px;
            }
        """)

        self.search_button = QtWidgets.QPushButton("Rechercher")
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.search_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.search_layout.addWidget(self.search_field)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addStretch()

        self.main_layout.addWidget(self.search_frame)

    def _setup_result_table(self):
        self.result_table = QtWidgets.QTableWidget()
        self.result_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 5px;
                border: none;
            }
        """)

        headers = [
            "ID", "Nom", "Prénom", "Email",
            "Poste", "Département",
            "Heures aujourd'hui", "Heures ce mois"
        ]
        self.result_table.setColumnCount(len(headers))
        self.result_table.setHorizontalHeaderLabels(headers)

        header = self.result_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        header.setDefaultAlignment(QtCore.Qt.AlignLeft)

        self.result_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.result_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setSortingEnabled(True)

        self.main_layout.addWidget(self.result_table)

    def _setup_menu_bar(self, MainWindow):
        self.menu_bar = QtWidgets.QMenuBar(MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        MainWindow.setMenuBar(self.menu_bar)

    def _setup_status_bar(self, MainWindow):
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.status_bar)

    def _connect_signals(self):
        self.search_button.clicked.connect(self.search_employee)
        self.btn_list.clicked.connect(self.open_dashboard)
        self.btn_add.clicked.connect(self.redirect_to_add_form)
        self.btn_attendance.clicked.connect(self.redirect_to_attendance)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Recherche d'Employés"))

    def search_employee(self):
        search_text = self.search_field.text().strip()
        if not search_text:
            QtWidgets.QMessageBox.warning(
                self.central_widget,
                "Champ vide",
                "Veuillez entrer un terme de recherche"
            )
            return

        try:
            search_results = search_employee(search_text)
            self.result_table.setRowCount(0)

            if not search_results:
                QtWidgets.QMessageBox.information(
                    self.central_widget,
                    "Aucun résultat",
                    "Aucun employé trouvé avec ce critère"
                )
                return

            for row, employee in enumerate(search_results):
                self.result_table.insertRow(row)

                for col in range(min(len(employee), 6)):
                    item = QTableWidgetItem(str(employee[col]))
                    self.result_table.setItem(row, col, item)

                employee_id = employee[0]
                try:
                    hours_today = get_worked_hours_today(employee_id) or "0"
                    hours_month = get_worked_hours_month(employee_id) or "0"

                    self.result_table.setItem(row, 6, QTableWidgetItem(str(hours_today)))
                    self.result_table.setItem(row, 7, QTableWidgetItem(str(hours_month)))
                except Exception as e:
                    print(f"Erreur heures: {e}")

            self.result_table.resizeColumnsToContents()

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.central_widget,
                "Erreur",
                f"Erreur lors de la recherche: {str(e)}"
            )

    def open_dashboard(self):
        if not hasattr(self, 'dashboard_window') or self.dashboard_window is None:
            self.dashboard_window = QMainWindow()
            ui = dashboard.Ui_MainWindow()
            ui.setupUi(self.dashboard_window)
        self.dashboard_window.show()


    def redirect_to_add_form(self):
        if not hasattr(self, 'add_form_window') or self.add_form_window is None:
            self.add_form_window = QMainWindow()
            ui = frome.Ui_MainWindow()
            ui.setupUi(self.add_form_window)
        self.add_form_window.show()

    def redirect_to_attendance(self):
        if not hasattr(self, 'attendance_window') or self.attendance_window is None:
            self.attendance_window = QMainWindow()
            ui = presence.Ui_MainWindow()
            ui.setupUi(self.attendance_window)
        self.attendance_window.show()


Ui_MainWindow = EmployeeSearchUI

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    font = QtGui.QFont()
    font.setFamily("Segoe UI")
    font.setPointSize(10)
    app.setFont(font)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
