from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from mysql.connector import Error
from user import User

class Ui_CreateProfileDialog(object):
    def setupUi(self, CreateProfileDialog):
        CreateProfileDialog.setObjectName("CreateProfileDialog")
        CreateProfileDialog.setFixedSize(340, 200)
        CreateProfileDialog.setWindowTitle("Вход в профиль")
        self.CreateProfileDialog = CreateProfileDialog

        self.createButton = QtWidgets.QPushButton(CreateProfileDialog)
        self.createButton.setGeometry(QtCore.QRect(30, 155, 130, 35))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.createButton.setFont(font)
        self.createButton.setAutoDefault(False)
        self.createButton.setObjectName("createButton")
        self.createButton.setText("Войти")
        self.createButton.clicked.connect(self.onCreateButtonClicked)

        self.cancelButton = QtWidgets.QPushButton(CreateProfileDialog)
        self.cancelButton.setGeometry(QtCore.QRect(180, 155, 130, 35))
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

    def onCreateButtonClicked(self):
        try:
            self.currentUser = User(self.nameLine.text(), self.passwordLine.text())
            self.CreateProfileDialog.accept()
        except ValueError as e:
            QMessageBox.warning(CreateProfileDialog, "Неверный пароль", e, QMessageBox.Ok)
        except Error as e:
            QMessageBox.warning(CreateProfileDialog, "Ошибка при соединении с БД", e, QMessageBox.Ok)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CreateProfileDialog = QtWidgets.QDialog()
    ui = Ui_CreateProfileDialog()
    ui.setupUi(CreateProfileDialog)
    CreateProfileDialog.show()
    sys.exit(app.exec_())
