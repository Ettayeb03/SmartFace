from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QVBoxLayout, QCalendarWidget, QFormLayout, QLineEdit, \
    QComboBox, QDateEdit, QPushButton


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(925, 600)
        MainWindow.setStyleSheet("background-color:#fff; border:none;")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # --- Barre de navigation latérale ---
        nav_button_style = """
            QPushButton {
                border: none;
                color: white;
                background-color: #2f89ff;
                border-radius: 5px;
                font-size: 15px;
                padding: 10px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #1a73e8;
            }
        """

        self.navbar = QtWidgets.QFrame(self.centralwidget)
        self.navbar.setGeometry(QtCore.QRect(0, 0, 200, 600))
        self.navbar.setStyleSheet("background-color: #2f89ff;")

        self.btn_list = QtWidgets.QPushButton("Liste Employés", self.navbar)
        self.btn_list.setGeometry(QtCore.QRect(10, 100, 180, 40))
        self.btn_list.setStyleSheet(nav_button_style)
        self.btn_list.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.btn_add = QtWidgets.QPushButton("Ajouter Employé", self.navbar)
        self.btn_add.setGeometry(QtCore.QRect(10, 150, 180, 40))
        self.btn_add.setStyleSheet(nav_button_style)
        self.btn_add.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.btn_search = QtWidgets.QPushButton("Chercher Employé", self.navbar)
        self.btn_search.setGeometry(QtCore.QRect(10, 200, 180, 40))
        self.btn_search.setStyleSheet(nav_button_style)
        self.btn_search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.btn_presence = QtWidgets.QPushButton("Consulter la présence", self.navbar)
        self.btn_presence.setGeometry(QtCore.QRect(10, 250, 180, 40))
        self.btn_presence.setStyleSheet(nav_button_style)
        self.btn_presence.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # --- Zone de contenu principal ---
        self.title_text = QtWidgets.QTextEdit(self.centralwidget)
        self.title_text.setGeometry(QtCore.QRect(250, 10, 600, 60))
        self.title_text.setStyleSheet("border: none; background-color: white;")
        self.title_text.setReadOnly(True)

        # --- Formulaire de connexion ---
        self.login_frame = QtWidgets.QFrame(self.centralwidget)
        self.login_frame.setGeometry(QtCore.QRect(300, 100, 300, 200))
        self.login_frame.setStyleSheet("background-color: #f0f0f0; border-radius: 10px;")

        self.label_username = QtWidgets.QLabel("Utilisateur :", self.login_frame)
        self.label_username.setGeometry(QtCore.QRect(30, 40, 100, 20))

        self.input_username = QtWidgets.QLineEdit(self.login_frame)
        self.input_username.setGeometry(QtCore.QRect(140, 40, 120, 24))
        self.input_username.setPlaceholderText("Nom d'utilisateur")

        self.label_password = QtWidgets.QLabel("Mot de passe :", self.login_frame)
        self.label_password.setGeometry(QtCore.QRect(30, 80, 100, 20))

        self.input_password = QtWidgets.QLineEdit(self.login_frame)
        self.input_password.setGeometry(QtCore.QRect(140, 80, 120, 24))
        self.input_password.setPlaceholderText("Mot de passe")
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.btn_login = QtWidgets.QPushButton("Connexion", self.login_frame)
        self.btn_login.setGeometry(QtCore.QRect(100, 130, 100, 30))
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #2f89ff;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1a73e8;
            }
        """)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 925, 21))
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Gestion du Profil"))
        self.title_text.setHtml(_translate("MainWindow", """
            <p align="center" style="font-size:16pt; font-weight:700;">Connexion</p>
        """))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connexion des boutons
        self.ui.btn_login.clicked.connect(self.verifier_connexion)
        self.ui.btn_list.clicked.connect(self.afficher_liste_employes)
        self.ui.btn_add.clicked.connect(self.ajouter_employe)
        self.ui.btn_search.clicked.connect(self.chercher_employe)
        self.ui.btn_presence.clicked.connect(self.consulter_presence)

    def verifier_connexion(self):
        username = self.ui.input_username.text()
        password = self.ui.input_password.text()

        if username == "admin" and password == "admin":
            QtWidgets.QMessageBox.information(self, "Succès", "Connexion réussie !")
            self.afficher_page_principale()
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Identifiants incorrects")

    def afficher_page_principale(self):
        self.ui.login_frame.hide()
        self.ui.title_text.setHtml("""
            <p align="center" style="font-size:16pt; font-weight:700;">Bienvenue dans l'application</p>
        """)

    def afficher_liste_employes(self):
        self.ui.title_text.setHtml("""
            <p align="center" style="font-size:16pt; font-weight:700;">Liste des employés</p>
        """)
        # Create QTableWidget
        self.table_employes = QTableWidget()
        self.table_employes.setColumnCount(5)
        self.table_employes.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Poste", "Département"])
        self.table_employes.horizontalHeader().setStretchLastSection(True)

        # Sample data - replace with actual data from your database
        employes = [
            (1, "Dupont", "Jean", "Développeur", "IT"),
            (2, "Martin", "Sophie", "RH", "Ressources Humaines")
        ]

        self.table_employes.setRowCount(len(employes))
        for row, emp in enumerate(employes):
            for col, data in enumerate(emp):
                self.table_employes.setItem(row, col, QTableWidgetItem(str(data)))

        # Add table to layout
        self.ui.scrollAreaWidgetContents.layout().addWidget(self.table_employes)

    def ajouter_employe(self):
        self.ui.title_text.setHtml("""
            <p align="center" style="font-size:16pt; font-weight:700;">Ajouter un employé</p>
        """)
        # Create form widgets
        form_layout = QFormLayout()

        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.poste_input = QLineEdit()
        self.departement_input = QComboBox()
        self.departement_input.addItems(["IT", "Ressources Humaines", "Finance", "Marketing"])
        self.date_embauche_input = QDateEdit()
        self.date_embauche_input.setCalendarPopup(True)

        form_layout.addRow("Nom:", self.nom_input)
        form_layout.addRow("Prénom:", self.prenom_input)
        form_layout.addRow("Poste:", self.poste_input)
        form_layout.addRow("Département:", self.departement_input)
        form_layout.addRow("Date d'embauche:", self.date_embauche_input)

        submit_btn = QPushButton("Ajouter")
        submit_btn.clicked.connect(self.enregistrer_employe)
        form_layout.addRow(submit_btn)

        # Clear previous widgets and add form
        self.clear_layout()
        self.ui.scrollAreaWidgetContents.layout().addLayout(form_layout)

    def chercher_employe(self):
        self.ui.title_text.setHtml("""
            <p align="center" style="font-size:16pt; font-weight:700;">Rechercher un employé</p>
        """)
        # Create search widgets
        search_layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher par nom, prénom ou ID...")
        search_btn = QPushButton("Rechercher")
        search_btn.clicked.connect(self.executer_recherche)

        self.search_results = QTableWidget()
        self.search_results.setColumnCount(5)
        self.search_results.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Poste", "Département"])

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(self.search_results)

        # Clear previous widgets and add search
        self.clear_layout()
        self.ui.scrollAreaWidgetContents.layout().addLayout(search_layout)

    def consulter_presence(self):
        self.ui.title_text.setHtml("""
            <p align="center" style="font-size:16pt; font-weight:700;">Consulter les présences</p>
        """)
        # Create calendar and presence table
        main_layout = QVBoxLayout()

        # Calendar for date selection
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.afficher_presences_date)
        main_layout.addWidget(self.calendar)

        # Presence table
        self.presence_table = QTableWidget()
        self.presence_table.setColumnCount(4)
        self.presence_table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Présence"])

        main_layout.addWidget(self.presence_table)

        # Clear previous widgets and add new ones
        self.clear_layout()
        self.ui.scrollAreaWidgetContents.layout().addLayout(main_layout)

    def clear_layout(self):
        # Helper method to clear the scroll area contents
        layout = self.ui.scrollAreaWidgetContents.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def enregistrer_employe(self):
        # Method to handle employee form submission
        nom = self.nom_input.text()
        prenom = self.prenom_input.text()
        poste = self.poste_input.text()
        departement = self.departement_input.currentText()
        date_embauche = self.date_embauche_input.date().toString("yyyy-MM-dd")

        # TODO: Add code to save employee to database
        print(f"Employé ajouté: {nom} {prenom}, {poste}, {departement}, {date_embauche}")

    def executer_recherche(self):
        # Method to handle employee search
        search_term = self.search_input.text()

        # TODO: Add code to search employees in database
        # This is just sample data
        results = [
            (1, "Dupont", "Jean", "Développeur", "IT"),
            (2, "Martin", "Sophie", "RH", "Ressources Humaines")
        ]

        self.search_results.setRowCount(len(results))
        for row, emp in enumerate(results):
            for col, data in enumerate(emp):
                self.search_results.setItem(row, col, QTableWidgetItem(str(data)))

    def afficher_presences_date(self, date):
        # Method to show attendance for selected date
        selected_date = date.toString("yyyy-MM-dd")

        # TODO: Add code to fetch attendance for selected date
        # This is just sample data
        presences = [
            (1, "Dupont", "Jean", "Présent"),
            (2, "Martin", "Sophie", "Absent")
        ]

        self.presence_table.setRowCount(len(presences))
        for row, pres in enumerate(presences):
            for col, data in enumerate(pres):
                self.presence_table.setItem(row, col, QTableWidgetItem(str(data)))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
