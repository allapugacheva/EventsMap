from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from mysql.connector import Error
from user import User
from PyQt5.QtWidgets import QMessageBox
from geopy.geocoders import Nominatim

class Ui_CreateProfileDialog(object):
    def setupUi(self, CreateProfileDialog):
        CreateProfileDialog.setObjectName("CreateProfileDialog")
        CreateProfileDialog.setFixedSize(340, 275)
        CreateProfileDialog.setWindowTitle("Вход в профиль")
        self.CreateProfileDialog = CreateProfileDialog

        self.createButton = QtWidgets.QPushButton(CreateProfileDialog)
        self.createButton.setGeometry(QtCore.QRect(30, 225, 130, 35))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.createButton.setFont(font)
        self.createButton.setObjectName("createButton")
        self.createButton.setText("Войти")
        self.createButton.clicked.connect(self.onCreateButtonClicked)

        self.cancelButton = QtWidgets.QPushButton(CreateProfileDialog)
        self.cancelButton.setGeometry(QtCore.QRect(180, 225, 130, 35))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.cancelButton.setFont(font)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText("Отмена")
        self.cancelButton.clicked.connect(self.CreateProfileDialog.close)

        self.nameLine = QtWidgets.QLineEdit(CreateProfileDialog)
        self.nameLine.setGeometry(QtCore.QRect(20, 40, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nameLine.setFont(font)
        self.nameLine.setObjectName("nameLine")
    
        self.passwordLine = QtWidgets.QLineEdit(CreateProfileDialog)
        self.passwordLine.setGeometry(QtCore.QRect(20, 110, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.passwordLine.setFont(font)
        self.passwordLine.setObjectName("passwordLine")

        self.nameLabel = QtWidgets.QLabel(CreateProfileDialog)
        self.nameLabel.setGeometry(QtCore.QRect(20, 10, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Введите имя:")

        self.passwordLabel = QtWidgets.QLabel(CreateProfileDialog)
        self.passwordLabel.setGeometry(QtCore.QRect(20, 80, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName("passwordLabel")
        self.passwordLabel.setText("Введите пароль:")

        self.addressLine = QtWidgets.QLineEdit(CreateProfileDialog)
        self.addressLine.setGeometry(QtCore.QRect(20, 180, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.addressLine.setFont(font)
        self.addressLine.setObjectName("cityLine")
        self.addressLabel = QtWidgets.QLabel(CreateProfileDialog)
        self.addressLabel.setGeometry(QtCore.QRect(20, 150, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.addressLabel.setFont(font)
        self.addressLabel.setObjectName("addressLabel")
        self.addressLabel.setText("Область поиска:")

    def onCreateButtonClicked(self):
        try:
            if self.nameLine.text().strip() == "":
                raise ValueError("Укажите имя")
            if self.passwordLine.text().strip == "":
                raise ValueError("Укажите пароль")
            if self.addressLine.text().strip() == "":
                raise ValueError("Укажите область поиска")

            geolocator = Nominatim(user_agent="alla123425")
            location = geolocator.geocode(self.addressLine.text())

            if location:
                self.currentUser = User(self.nameLine.text(), self.passwordLine.text(), location.latitude, location.longitude)
                self.CreateProfileDialog.accept()
            else:
                raise ValueError("Адрес не найден")
        except ValueError as e:
            QMessageBox.warning(self.CreateProfileDialog, "Ошибка при вводе данных", str(e), QMessageBox.Ok)
        except Error as e:
            QMessageBox.warning(self.CreateProfileDialog, "Ошибка при соединении с БД", e, QMessageBox.Ok)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CreateProfileDialog = QtWidgets.QDialog()
    ui = Ui_CreateProfileDialog()
    ui.setupUi(CreateProfileDialog)
    CreateProfileDialog.show()
    sys.exit(app.exec_())
