from PyQt5 import QtCore, QtGui, QtWidgets
from user import User
from PyQt5.QtWidgets import QMessageBox
from mysql.connector import Error

class Ui_inProfileDialog(object):
    def setupUi(self, inProfileDialog):
        inProfileDialog.setObjectName("inProfileDialog")
        inProfileDialog.resize(340, 205)
        inProfileDialog.setWindowTitle("Войти")
        self.inProfileDialog = inProfileDialog

        self.nameLabel = QtWidgets.QLabel(inProfileDialog)
        self.nameLabel.setGeometry(QtCore.QRect(20, 10, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Введите имя:")

        self.passwordLine = QtWidgets.QLineEdit(inProfileDialog)
        self.passwordLine.setGeometry(QtCore.QRect(20, 110, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.passwordLine.setFont(font)
        self.passwordLine.setObjectName("passwordLine")

        self.nameLine = QtWidgets.QLineEdit(inProfileDialog)
        self.nameLine.setGeometry(QtCore.QRect(20, 40, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nameLine.setFont(font)
        self.nameLine.setObjectName("nameLine")

        self.passwordLabel = QtWidgets.QLabel(inProfileDialog)
        self.passwordLabel.setGeometry(QtCore.QRect(20, 80, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName("passwordLabel")
        self.passwordLabel.setText("Введите пароль:")

        self.createButton = QtWidgets.QPushButton(inProfileDialog)
        self.createButton.setGeometry(QtCore.QRect(30, 155, 130, 35))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.createButton.setFont(font)
        self.createButton.setObjectName("createButton")
        self.createButton.setText("Войти")
        self.createButton.clicked.connect(self.onInButtonClicked)
        
        self.cancelButton = QtWidgets.QPushButton(inProfileDialog)
        self.cancelButton.setGeometry(QtCore.QRect(180, 155, 130, 35))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.cancelButton.setFont(font)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText("Отмена")
        self.cancelButton.clicked.connect(self.inProfileDialog.close)

    def onInButtonClicked(self):
        try:
            if self.nameLine.text().strip() == "":
                raise ValueError("Введите имя")
            if self.passwordLine.text().strip() == "":
                raise ValueError("Введите пароль")

            self.currentUser = User(self.nameLine.text(), self.passwordLine.text())
            self.inProfileDialog.accept()
        except ValueError as e:
            QMessageBox.warning(self.inProfileDialog, "Ошибка при вводе данных", str(e), QMessageBox.Ok)
        except Error as e:
            QMessageBox.warning(self.inProfileDialog, "Ошибка при соединении с БД", e, QMessageBox.Ok)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    inProfileDialog = QtWidgets.QDialog()
    ui = Ui_inProfileDialog()
    ui.setupUi(inProfileDialog)
    inProfileDialog.show()
    sys.exit(app.exec_())
