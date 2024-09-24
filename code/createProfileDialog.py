from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateProfileDialog(object):
    def setupUi(self, CreateProfileDialog):
        CreateProfileDialog.setObjectName("CreateProfileDialog")
        CreateProfileDialog.resize(400, 270)
        self.CreateProfileDialog = CreateProfileDialog
        self.createButton = QtWidgets.QPushButton(CreateProfileDialog)
        self.createButton.setGeometry(QtCore.QRect(70, 210, 120, 40))
        self.createButton.setAutoDefault(False)
        self.createButton.setObjectName("createButton")
        self.createButton.clicked.connect(self.createClicked)
        self.cancelButton = QtWidgets.QPushButton(CreateProfileDialog)
        self.cancelButton.setGeometry(QtCore.QRect(210, 210, 120, 40))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(CreateProfileDialog.close)
        self.nameLine = QtWidgets.QLineEdit(CreateProfileDialog)
        self.nameLine.setGeometry(QtCore.QRect(50, 60, 300, 40))
        self.nameLine.setObjectName("nameLine")
        self.passwordLine = QtWidgets.QLineEdit(CreateProfileDialog)
        self.passwordLine.setGeometry(QtCore.QRect(50, 150, 300, 40))
        self.passwordLine.setObjectName("passwordLine")
        self.nameLabel = QtWidgets.QLabel(CreateProfileDialog)
        self.nameLabel.setGeometry(QtCore.QRect(50, 20, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")
        self.passwordLabel = QtWidgets.QLabel(CreateProfileDialog)
        self.passwordLabel.setGeometry(QtCore.QRect(50, 110, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName("passwordLabel")

        self.retranslateUi(CreateProfileDialog)
        QtCore.QMetaObject.connectSlotsByName(CreateProfileDialog)

    def retranslateUi(self, CreateProfileDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateProfileDialog.setWindowTitle(_translate("CreateProfileDialog", "Создать профиль"))
        self.createButton.setText(_translate("CreateProfileDialog", "Создать"))
        self.cancelButton.setText(_translate("CreateProfileDialog", "Отмена"))
        self.nameLabel.setText(_translate("CreateProfileDialog", "Введите имя:"))
        self.passwordLabel.setText(_translate("CreateProfileDialog", "Введите пароль:"))

    def createClicked(self):
        print("created")
        self.CreateProfileDialog.accept()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CreateProfileDialog = QtWidgets.QDialog()
    ui = Ui_CreateProfileDialog()
    ui.setupUi(CreateProfileDialog)
    CreateProfileDialog.show()
    sys.exit(app.exec_())
