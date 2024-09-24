from PyQt5 import QtCore, QtWidgets
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtCore import QUrl
from createProfileDialog import Ui_CreateProfileDialog
from PyQt5.QtWidgets import QMessageBox
from geopy.geocoders import Nominatim
from addEventDialog import Ui_AddEventDialog

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.eventsList = QtWidgets.QListView(self.centralwidget)
        self.eventsList.setGeometry(QtCore.QRect(600, 30, 300, 540))
        self.eventsList.setObjectName("eventsList")
        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(600, 0, 150, 30))
        self.loginButton.setStyleSheet("alternate-background-color: qradialgradient(spread:repeat, cx:0.5, cy:0.5, radius:0.077, fx:0.5, fy:0.5, stop:0 rgba(0, 169, 255, 147), stop:0.497326 rgba(0, 0, 0, 147), stop:1 rgba(0, 169, 255, 147));")
        self.loginButton.setObjectName("loginButton")
        self.unloginButton = QtWidgets.QPushButton(self.centralwidget)
        self.unloginButton.setGeometry(QtCore.QRect(750, 0, 150, 30))
        self.unloginButton.setObjectName("unloginButton")
        self.addEventButton = QtWidgets.QPushButton(self.centralwidget)
        self.addEventButton.setGeometry(QtCore.QRect(600, 570, 150, 30))
        self.addEventButton.setObjectName("addEventButton")
        self.deleteEventButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteEventButton.setGeometry(QtCore.QRect(750, 570, 150, 30))
        self.deleteEventButton.setObjectName("deleteEventButton")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 601, 601))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.mapLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.mapLayout.setContentsMargins(0, 0, 0, 0)
        self.mapLayout.setObjectName("mapLayout")
        self.view = QQuickWidget()
        self.view.setSource(QUrl("code/map.qml"))
        self.view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.view.setFixedSize(600, 600)
        self.mapLayout.addWidget(self.view)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EventsMap"))
        self.loginButton.setText(_translate("MainWindow", "Войти в профиль"))
        self.loginButton.clicked.connect(self.enterProfile)
        self.unloginButton.setText(_translate("MainWindow", "Выйти из профиля"))
        self.addEventButton.setText(_translate("MainWindow", "Добавить событие"))
        self.addEventButton.clicked.connect(self.addEvent)
        self.deleteEventButton.setText(_translate("MainWindow", "Удалить событие"))

    def enterProfile(self):
        dialogProfile = QtWidgets.QDialog()
        dialogProfileUi = Ui_CreateProfileDialog()
        dialogProfileUi.setupUi(dialogProfile)
        dialogProfile.setModal(True)
        dialogProfile.exec_()

    def addEvent(self):
        dialogEvent = QtWidgets.QDialog()
        dialogEventUi = Ui_AddEventDialog()
        dialogEventUi.setupUi(dialogEvent)
        dialogEvent.setModal(True)
        dialogEvent.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # address = "Минск, ул. Гикало, д. 9"
    # geolocator = Nominatim(user_agent="alla123425")
    # location = geolocator.geocode(address)

    # if location:
    #     coords = f"Широта: {location.latitude}, Долгота: {location.longitude}"
    #     QMessageBox.information(MainWindow, "Координаты", coords)
    # else:
    #     QMessageBox.warning(MainWindow, "Ошибка", "Адрес не найден.")

    MainWindow.show()
    sys.exit(app.exec_())