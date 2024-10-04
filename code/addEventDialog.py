from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from geopy.geocoders import Nominatim
from event import Event
from mysql.connector import Error
from PyQt5.QtCore import QDateTime

class Ui_AddEventDialog(object):
    def setupUi(self, AddEventDialog, user):
        AddEventDialog.setObjectName("AddEventDialog")
        AddEventDialog.setFixedSize(340, 345)
        AddEventDialog.setWindowTitle("Добавление события")
        self.AddEventDialog = AddEventDialog
        self.edit = False
        self.user = user

        self.eventNameLabel = QtWidgets.QLabel(AddEventDialog)
        self.eventNameLabel.setGeometry(QtCore.QRect(20, 10, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.eventNameLabel.setFont(font)
        self.eventNameLabel.setObjectName("eventNameLabel")
        self.eventNameLabel.setText("Название события:")

        self.eventNameLine = QtWidgets.QLineEdit(AddEventDialog)
        self.eventNameLine.setGeometry(QtCore.QRect(20, 40, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.eventNameLine.setFont(font)
        self.eventNameLine.setObjectName("eventNameLine")

        self.descriptionLabel = QtWidgets.QLabel(AddEventDialog)
        self.descriptionLabel.setGeometry(QtCore.QRect(20, 80, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.descriptionLabel.setFont(font)
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.descriptionLabel.setText("Описание события:")

        self.descriptionLine = QtWidgets.QLineEdit(AddEventDialog)
        self.descriptionLine.setGeometry(QtCore.QRect(20, 110, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.descriptionLine.setFont(font)
        self.descriptionLine.setObjectName("descriptionLine")

        self.dateTimeLabel = QtWidgets.QLabel(AddEventDialog)
        self.dateTimeLabel.setGeometry(QtCore.QRect(20, 150, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.dateTimeLabel.setFont(font)
        self.dateTimeLabel.setObjectName("dateTimeLabel")
        self.dateTimeLabel.setText("Дата и время:")

        self.dateTimeEdit = QtWidgets.QDateTimeEdit(AddEventDialog)
        self.dateTimeEdit.setGeometry(QtCore.QRect(20, 180, 300, 30))
        self.dateTimeEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.dateTimeEdit.setFont(font)
        self.dateTimeEdit.setObjectName("dateTimeEdit")

        self.addressLine = QtWidgets.QLineEdit(AddEventDialog)
        self.addressLine.setGeometry(QtCore.QRect(20, 250, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.addressLine.setFont(font)
        self.addressLine.setObjectName("addressLine")

        self.addressLabel = QtWidgets.QLabel(AddEventDialog)
        self.addressLabel.setGeometry(QtCore.QRect(20, 220, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.addressLabel.setFont(font)
        self.addressLabel.setObjectName("addressLabel")
        self.addressLabel.setText("Адрес события:")

        self.addButton = QtWidgets.QPushButton(AddEventDialog)
        self.addButton.setGeometry(QtCore.QRect(30, 295, 130, 35))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")
        self.addButton.setText("Добавить")
        self.addButton.clicked.connect(self.onAddButtonClicked)

        self.cancelButton = QtWidgets.QPushButton(AddEventDialog)
        self.cancelButton.setGeometry(QtCore.QRect(180, 295, 130, 35))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.cancelButton.setFont(font)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText("Отмена")
        self.cancelButton.clicked.connect(AddEventDialog.close)

    def enableEdit(self, name, description, datetime, address):
        self.enableEdit = True
        self.eventNameLine.setText(name)
        self.descriptionLine.setText(description)
        self.dateTimeEdit.setDateTime(QDateTime.fromString(datetime, "yyyy-MM-dd HH:mm"))
        self.addressLine.setText(address)

    def onAddButtonClicked(self):
        try:
            if self.dateTimeEdit.dateTime() < QDateTime.currentDateTime():
                raise ValueError("Событие не может быть в прошлом")
            if self.eventNameLine.text().strip() == "":
                raise ValueError("Укажите название события")
            if self.descriptionLine.text().strip() == "":
                raise ValueError("Укажите описание события")
            if self.addressLine.text().strip == "":
                raise ValueError("Укажите адрес события")

            geolocator = Nominatim(user_agent="alla123425")
            location = geolocator.geocode(self.addressLine.text())

            if location:
                if self.edit:
                    self.currentEvent = Event(self.eventNameLine.text(), self.descriptionLine.text(), self.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm"), self.addressLine.text(), location.latitude, location.longitude)
                else:
                    self.currentEvent = Event(self.eventNameLine.text(), self.descriptionLine.text(), self.user, self.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm"), self.addressLine.text(), location.latitude, location.longitude)
                self.AddEventDialog.accept()
            else:
                raise ValueError("Адрес не найден")
        except ValueError as e:
            QMessageBox.warning(self.AddEventDialog, "Неверный адрес", str(e), QMessageBox.Ok)
        except Error as e:
            QMessageBox.warning(self.AddEventDialog, "Ошибка при соединении с БД", e, QMessageBox.Ok)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddEventDialog = QtWidgets.QDialog()
    ui = Ui_AddEventDialog()
    ui.setupUi(AddEventDialog)
    AddEventDialog.show()
    sys.exit(app.exec_())
