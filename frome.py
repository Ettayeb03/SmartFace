from PyQt5 import QtCore, QtGui, QtWidgets
from database import get_dep, insert_employee
import dashboard
import chercher
import presence


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 600)
        MainWindow.setStyleSheet("background-color:#fff;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.file_path = ""

        # Navigation bar
        self.navbar = QtWidgets.QGraphicsView(self.centralwidget)
        self.navbar.setGeometry(QtCore.QRect(0, 0, 161, 591))
        self.navbar.setStyleSheet("border:none")
        self.navbar.setObjectName("navbar")

        # Buttons
        self.pushButton = QtWidgets.QPushButton("Liste Employées", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 100, 201, 41))
        self.pushButton.setStyleSheet(self.button_style())
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.pushButton_2 = QtWidgets.QPushButton("Ajouter Employées", self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 180, 201, 41))
        self.pushButton_2.setStyleSheet(self.button_style())
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.pushButton_3 = QtWidgets.QPushButton("Chercher Employé", self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 270, 201, 41))
        self.pushButton_3.setStyleSheet(self.button_style())
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.pushButton_4 = QtWidgets.QPushButton("Consulter la présence", self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 360, 201, 41))
        self.pushButton_4.setStyleSheet(self.button_style())
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Title
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(400, 0, 361, 51))
        self.textBrowser.setHtml("<p align='center'><span style=' font-size:18pt; font-weight:700;'>Ajouter Employé</span></p>")

        # Labels and input fields
        self.create_label("Nom", 238, 110)
        self.lineEdit = self.create_line_edit(330, 110)

        self.create_label("Email", 238, 160)
        self.lineEdit_3 = self.create_line_edit(330, 160)

        self.create_label("Prenom", 538, 110)
        self.lineEdit_2 = self.create_line_edit(620, 110)

        self.create_label("Poste", 538, 160)
        self.lineEdit_4 = self.create_line_edit(620, 160)

        self.create_label("Département", 238, 210)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(330, 210, 181, 24))
        self.comboBox.setStyleSheet("QComboBox { border: 2px solid black; border-radius: 5px; }")

        self.create_label("Image", 540, 210)
        self.pushButton_5 = QtWidgets.QPushButton("Parcourir", self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(630, 210, 211, 24))
        self.pushButton_5.setStyleSheet("QPushButton { border: none; background-color: #2ecc71; color: white; border-radius: 5px; }")
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(630, 240, 300, 20))
        self.image_label.setText("")
        self.image_label.setStyleSheet("color: gray;")

        self.pushButton_6 = QtWidgets.QPushButton("Ajouter", self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(500, 290, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet("color: white; background-color: rgb(52, 235, 225); border: none;")
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        MainWindow.setCentralWidget(self.centralwidget)

    def button_style(self):
        return "border:none; color:white; background-color: #2f89ff; border-radius:10px; font-size:15px;"

    def create_label(self, text, x, y):
        label = QtWidgets.QLabel(text, self.centralwidget)
        label.setGeometry(QtCore.QRect(x, y, 91, 20))
        font = QtGui.QFont()
        font.setBold(True)
        label.setFont(font)
        label.setStyleSheet("color: black; font-size:14px")
        return label

    def create_line_edit(self, x, y):
        line_edit = QtWidgets.QLineEdit(self.centralwidget)
        line_edit.setGeometry(QtCore.QRect(x, y, 181, 24))
        line_edit.setStyleSheet("QLineEdit { border: 2px solid black; border-radius: 5px; }")
        return line_edit

    def populate_departments(self):
        try:
            departments = get_dep()
            self.comboBox.clear()
            for dep_id, dep_name in departments:
                self.comboBox.addItem(f"{dep_id}: {dep_name}")
        except Exception as e:
            print("Erreur chargement départements:", e)

    def browse_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Choisir une image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.file_path = file_path
            self.image_label.setText(file_path.split("/")[-1])

    def ajouter_employe(self):
        nom = self.lineEdit.text()
        prenom = self.lineEdit_2.text()
        email = self.lineEdit_3.text()
        poste = self.lineEdit_4.text()
        departement_text = self.comboBox.currentText()

        if not all([nom, prenom, email, poste]):
            self.show_message("Tous les champs doivent être remplis.", QtWidgets.QMessageBox.Warning)
            return

        if not departement_text:
            self.show_message("Veuillez sélectionner un département.", QtWidgets.QMessageBox.Warning)
            return

        try:
            departement_id = int(departement_text.split(':')[0])
        except (IndexError, ValueError):
            self.show_message("Département invalide.", QtWidgets.QMessageBox.Warning)
            return

        if not self.file_path:
            self.show_message("Veuillez sélectionner une image.", QtWidgets.QMessageBox.Warning)
            return

        try:
            with open(self.file_path, 'rb') as f:
                image_data = f.read()
            insert_employee(nom, prenom, email, poste, departement_id, image_data)
        except Exception as e:
            self.show_message(f"Erreur lors de l'ajout: {e}", QtWidgets.QMessageBox.Critical)
            return

        self.clear_form()
        self.show_message("Employé ajouté avec succès.", QtWidgets.QMessageBox.Information)

    def clear_form(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.comboBox.setCurrentIndex(0)
        self.image_label.setText("")
        self.file_path = ""

    def show_message(self, text, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle("Message")
        msg_box.setText(text)
        msg_box.exec_()

    def redirect_to_dashboard(self):
        if not hasattr(self, 'dashboard_window'):
            self.dashboard_window = QtWidgets.QMainWindow()
            ui = dashboard.Ui_MainWindow()
            ui.setupUi(self.dashboard_window)
        self.dashboard_window.show()

    def redirect_to_chercher(self):
        if not hasattr(self, 'chercher_window'):
            self.chercher_window = QtWidgets.QMainWindow()
            ui = chercher.Ui_MainWindow()
            ui.setupUi(self.chercher_window)
        self.chercher_window.show()

    def redirect_to_presence(self):
        if not hasattr(self, 'presence_window'):
            self.presence_window = QtWidgets.QMainWindow()
            ui = presence.Ui_MainWindow()
            ui.setupUi(self.presence_window)
        self.presence_window.show()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_6.clicked.connect(self.ajouter_employe)
        self.pushButton_5.clicked.connect(self.browse_file)
        self.pushButton.clicked.connect(self.redirect_to_dashboard)
        self.pushButton_3.clicked.connect(self.redirect_to_chercher)
        self.pushButton_4.clicked.connect(self.redirect_to_presence)
        self.pushButton_2.clicked.connect(self.clear_form)
        self.populate_departments()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


class AddEmployeeWindow:
    pass