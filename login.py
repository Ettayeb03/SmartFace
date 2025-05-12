from PyQt5 import QtCore, QtGui, QtWidgets
from dashboard import DashboardWindow
from database import check_login  # import déplacé ici


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("LoginWindow")
        self.resize(800, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout principal
        layout = QtWidgets.QVBoxLayout(self.central_widget)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # Titre de l'application
        self.title = QtWidgets.QLabel("SmartFace - Connexion")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(self.title, alignment=QtCore.Qt.AlignCenter)

        # Formulaire utilisateur/mot de passe
        form_layout = QtWidgets.QFormLayout()

        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setMinimumWidth(300)
        form_layout.addRow("Utilisateur:", self.username_input)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        form_layout.addRow("Mot de passe:", self.password_input)

        layout.addLayout(form_layout)

        # Bouton de connexion
        self.login_btn = QtWidgets.QPushButton("Se connecter")
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2f89ff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1a73e8;
            }
        """)
        self.login_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn, alignment=QtCore.Qt.AlignCenter)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
            return

        if check_login(username, password):
            self.dashboard = DashboardWindow()  # garder une référence pour éviter suppression
            self.dashboard.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Identifiants incorrects")


# Lancer l'application si ce fichier est exécuté directement
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
