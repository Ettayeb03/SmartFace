import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets
from database import DatabaseManager


class ProjectWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_projects()
        self.load_employees()

    def setup_ui(self):
        self.setWindowTitle("Gestion des Projets")
        self.resize(1000, 700)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.setup_project_form()
        self.setup_project_table()
        self.setup_assignment_section()

    def setup_project_form(self):
        form_layout = QtWidgets.QFormLayout()

        # Nom du projet
        self.project_name = QtWidgets.QLineEdit()
        self.project_name.setPlaceholderText("Nom du projet")
        form_layout.addRow("Nom:", self.project_name)

        # Description
        self.project_desc = QtWidgets.QTextEdit()
        self.project_desc.setMaximumHeight(100)
        form_layout.addRow("Description:", self.project_desc)

        # Date de début
        self.date_debut = QtWidgets.QDateEdit()
        self.date_debut.setCalendarPopup(True)
        self.date_debut.setDate(QtCore.QDate.currentDate())
        form_layout.addRow("Date début:", self.date_debut)

        # Date de fin
        self.date_fin = QtWidgets.QDateEdit()
        self.date_fin.setCalendarPopup(True)
        self.date_fin.setDate(QtCore.QDate.currentDate().addDays(30))
        form_layout.addRow("Date fin:", self.date_fin)

        # Bouton Ajouter Projet
        add_btn = QtWidgets.QPushButton("Ajouter Projet")
        add_btn.setStyleSheet("background-color: #2f89ff; color: white;")
        add_btn.clicked.connect(self.add_project)
        form_layout.addRow(add_btn)

        self.main_layout.addLayout(form_layout)

    def setup_project_table(self):
        self.project_table = QtWidgets.QTableWidget()
        self.project_table.setColumnCount(6)
        self.project_table.setHorizontalHeaderLabels(["ID", "Nom", "Description", "Date de début", "Date de fin", "Statut"])
        self.project_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.project_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.project_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.project_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.main_layout.addWidget(self.project_table)

    def setup_assignment_section(self):
        assignment_layout = QtWidgets.QHBoxLayout()

        # Liste employés
        self.employee_combo = QtWidgets.QComboBox()
        self.employee_combo.setPlaceholderText("Sélectionner un employé")
        assignment_layout.addWidget(self.employee_combo)

        # Liste projets
        self.project_combo = QtWidgets.QComboBox()
        self.project_combo.setPlaceholderText("Sélectionner un projet")
        assignment_layout.addWidget(self.project_combo)

        # Bouton Affecter
        assign_btn = QtWidgets.QPushButton("Affecter")
        assign_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        assign_btn.clicked.connect(self.assign_employee)
        assignment_layout.addWidget(assign_btn)

        self.main_layout.addLayout(assignment_layout)

    def load_projects(self):
        db = DatabaseManager.get_instance()
        projects = db.execute_query("SELECT * FROM projet", fetch='all') or []

        self.project_table.setRowCount(len(projects))
        self.project_combo.clear()
        self.project_combo.addItem("-- Sélectionner un projet --", None)

        for row, project in enumerate(projects):
            self.project_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(project['projet_id'])))
            self.project_table.setItem(row, 1, QtWidgets.QTableWidgetItem(project['nom']))
            self.project_table.setItem(row, 2, QtWidgets.QTableWidgetItem(project['description']))
            self.project_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(project['date_debut'])))
            self.project_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(project['date_fin'])))
            self.project_table.setItem(row, 5, QtWidgets.QTableWidgetItem(project['statut']))
            self.project_combo.addItem(project['nom'], project['projet_id'])

    def load_employees(self):
        db = DatabaseManager.get_instance()
        employees = db.execute_query("SELECT employee_id, nom, prenom FROM employees", fetch='all') or []

        self.employee_combo.clear()
        self.employee_combo.addItem("-- Sélectionner un employé --", None)
        for emp in employees:
            self.employee_combo.addItem(f"{emp['nom']} {emp['prenom']}", emp['employee_id'])

    def add_project(self):
        name = self.project_name.text().strip()
        desc = self.project_desc.toPlainText().strip()
        date_debut = self.date_debut.date().toString("yyyy-MM-dd")
        date_fin = self.date_fin.date().toString("yyyy-MM-dd")

        if not name:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom de projet")
            return

        db = DatabaseManager.get_instance()
        try:
            db.execute_query(
                "INSERT INTO projet (nom, description, date_debut, date_fin, statut) VALUES (%s, %s, %s, %s, %s)",
                (name, desc, date_debut, date_fin, 'En cours')
            )
            self.project_name.clear()
            self.project_desc.clear()
            self.load_projects()
            QtWidgets.QMessageBox.information(self, "Succès", "Projet ajouté avec succès")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout du projet: {str(e)}")

    def assign_employee(self):
        employee_id = self.employee_combo.currentData()
        project_id = self.project_combo.currentData()

        if not employee_id or not project_id:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un employé et un projet")
            return

        db = DatabaseManager.get_instance()
        try:
            # Vérifier si l'affectation existe déjà
            existing = db.execute_query(
                "SELECT 1 FROM affectation WHERE employee_id = %s AND projet_id = %s",
                (employee_id, project_id),
                fetch='one'
            )

            if existing:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Cet employé est déjà affecté à ce projet")
                return

            db.execute_query(
                "INSERT INTO affectation (employee_id, projet_id) VALUES (%s, %s)",
                (employee_id, project_id)
            )
            QtWidgets.QMessageBox.information(self, "Succès", "Affectation réussie")
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur de base de données: {err}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ProjectWindow()
    window.show()
    sys.exit(app.exec_())
