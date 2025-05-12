import sys
import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QLineEdit,
    QComboBox, QPushButton, QFormLayout,
    QVBoxLayout, QCalendarWidget, QMessageBox
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(925, 600)
        MainWindow.setStyleSheet("background-color:#fff;")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.navbar = QtWidgets.QFrame(self.centralwidget)
        self.navbar.setGeometry(QtCore.QRect(0, 0, 161, 591))
        self.navbar.setStyleSheet("background-color: #2f89ff; border:none")

        self.create_nav_buttons()

        self.content_area = QtWidgets.QScrollArea(self.centralwidget)
        self.content_area.setGeometry(QtCore.QRect(170, 0, 755, 591))
        self.content_area.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 753, 589))

        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.title_text = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.title_text.setMaximumSize(QtCore.QSize(16777215, 70))
        self.title_text.setStyleSheet("border: none; background: transparent;")
        self.verticalLayout.addWidget(self.title_text)

        self.content_area.setWidget(self.scrollAreaWidgetContents)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.afficher_liste_employes()

    def create_nav_buttons(self):
        buttons = [
            {"text": "Liste Employés", "y": 100, "action": self.afficher_liste_employes},
            {"text": "Ajouter Employé", "y": 180, "action": self.ajouter_employe},
            {"text": "Chercher Employé", "y": 260, "action": self.chercher_employe},
            {"text": "Consulter Présence", "y": 340, "action": self.consulter_presence}
        ]
        for btn in buttons:
            button = QtWidgets.QPushButton(self.navbar)
            button.setGeometry(QtCore.QRect(10, btn["y"], 141, 41))
            button.setFont(QtGui.QFont("Arial", 10))
            button.setStyleSheet("border: none; color: white; background-color: transparent; text-align: left; padding-left: 15px; font-size: 14px; border-radius: 5px;")
            button.setText(btn["text"])
            button.clicked.connect(btn["action"])

    def clear_content(self):
        for i in reversed(range(self.verticalLayout.count())):
            widget = self.verticalLayout.itemAt(i).widget()
            if widget is not None and widget != self.title_text:
                widget.deleteLater()

    def afficher_liste_employes(self):
        self.clear_content()
        self.title_text.setHtml("<p align='center' style='font-size:16pt; font-weight:700;'>Liste des employés</p>")

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Poste", "Département"])
        table.horizontalHeader().setStretchLastSection(True)

        try:
            connection = mysql.connector.connect(
                host="localhost", user="root", password="", database="smartFace"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT employee_id, nom, prenom, poste, department_id FROM employees")
            employes = cursor.fetchall()
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Erreur de base de données", f"Erreur : {err}")
            return

        table.setRowCount(len(employes))
        for row, emp in enumerate(employes):
            for col, data in enumerate(emp):
                table.setItem(row, col, QTableWidgetItem(str(data)))

        self.verticalLayout.addWidget(table)

    def ajouter_employe(self):
        self.clear_content()
        self.title_text.setHtml("<p align='center' style='font-size:16pt; font-weight:700;'>Ajouter un employé</p>")

        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.poste_input = QLineEdit()
        self.department_input = QComboBox()

        try:
            connection = mysql.connector.connect(
                host="localhost", user="root", password="", database="smartFace"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT department_id, name FROM departments")
            departments = cursor.fetchall()
            for dept_id, dept_name in departments:
                self.department_input.addItem(dept_name, dept_id)
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Erreur", f"Erreur récupération départements: {err}")

        form_layout.addRow("Nom:", self.name_input)
        form_layout.addRow("Prénom:", self.prenom_input)
        form_layout.addRow("Poste:", self.poste_input)
        form_layout.addRow("Département:", self.department_input)

        submit_btn = QPushButton("Enregistrer")
        submit_btn.setStyleSheet("background-color: #2f89ff; color: white;")
        submit_btn.clicked.connect(self.enregistrer_employe)
        form_layout.addRow(submit_btn)

        form_widget = QtWidgets.QWidget()
        form_widget.setLayout(form_layout)
        self.verticalLayout.addWidget(form_widget)

    def enregistrer_employe(self):
        nom = self.name_input.text().strip()
        prenom = self.prenom_input.text().strip()
        poste = self.poste_input.text().strip()
        department_id = self.department_input.currentData()

        if not nom or not prenom or not poste:
            QMessageBox.warning(None, "Champs manquants", "Veuillez remplir tous les champs.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost", user="root", password="", database="smartFace"
            )
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO employees (nom, prenom, poste, department_id) VALUES (%s, %s, %s, %s)",
                (nom, prenom, poste, department_id)
            )
            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(None, "Succès", "Employé ajouté avec succès.")
            self.afficher_liste_employes()
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Erreur de base de données", str(err))

    def chercher_employe(self):
        self.clear_content()
        self.title_text.setHtml("<p align='center' style='font-size:16pt; font-weight:700;'>Recherche</p>")

        layout = QVBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nom, prénom ou ID...")
        search_btn = QPushButton("Rechercher")
        search_btn.clicked.connect(self.executer_recherche)
        layout.addWidget(self.search_input)
        layout.addWidget(search_btn)

        self.search_results = QTableWidget()
        self.search_results.setColumnCount(5)
        self.search_results.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Poste", "Département"])
        self.search_results.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.search_results)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.verticalLayout.addWidget(widget)

    def executer_recherche(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            QMessageBox.warning(None, "Vide", "Entrez un terme.")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost", user="root", password="", database="smartFace"
            )
            cursor = connection.cursor()
            query = """
                SELECT employee_id, nom, prenom, poste, department_id
                FROM employees
                WHERE nom LIKE %s OR prenom LIKE %s OR employee_id = %s
            """
            cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", search_term))
            results = cursor.fetchall()
            cursor.close()
            connection.close()

            self.search_results.setRowCount(len(results))
            for row, emp in enumerate(results):
                for col, data in enumerate(emp):
                    self.search_results.setItem(row, col, QTableWidgetItem(str(data)))
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Erreur", str(err))

    def consulter_presence(self):
        self.clear_content()
        self.title_text.setHtml("<p align='center' style='font-size:16pt; font-weight:700;'>Présences</p>")

        layout = QVBoxLayout()
        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.afficher_presences_date)
        layout.addWidget(self.calendar)

        self.presence_table = QTableWidget()
        self.presence_table.setColumnCount(4)
        self.presence_table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Présence"])
        layout.addWidget(self.presence_table)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.verticalLayout.addWidget(widget)

    def afficher_presences_date(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")

        try:
            connection = mysql.connector.connect(
                host="localhost", user="root", password="", database="smartFace"
            )
            cursor = connection.cursor()
            cursor.execute("""
                SELECT e.employee_id, e.nom, e.prenom,
                IF(a.attendance_id IS NOT NULL, 'Présent', 'Absent') AS presence
                FROM employees e
                LEFT JOIN attendance a ON e.employee_id = a.employee_id AND DATE(a.date) = %s
            """, (selected_date,))
            results = cursor.fetchall()
            cursor.close()
            connection.close()

            self.presence_table.setRowCount(len(results))
            for row, data in enumerate(results):
                for col, val in enumerate(data):
                    self.presence_table.setItem(row, col, QTableWidgetItem(str(val)))
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Erreur", str(err))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Gestion des Employés"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
