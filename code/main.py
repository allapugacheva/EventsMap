from PyQt5 import QtCore, QtGui, QtWidgets
from createProfileDialog import Ui_CreateProfileDialog
from addEventDialog import Ui_AddEventDialog
import folium
import io
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMessageBox, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from user import User
from PyQt5.QtCore import Qt
from mysql.connector import connect, Error
from event import Event

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(900, 600)
        MainWindow.setWindowTitle("Карта событий")

        self.userIn = False
        self.currentEvents = []

        try:
            with connect(
                    host="localhost",
                    user="root",
                    password="13579",
                    port="3307",
                    database="eventsmapdb"
                ) as connection:
                    with connection.cursor() as cursor:

                        select_events_query = f""" 
                        SELECT idevent, name, description, organizer, datetime, city, street, house, latitude, longitude
                        FROM event
                        """
                        cursor.execute(select_events_query)
                        events = cursor.fetchall()
                        if events:
                            for event in events:
                                self.currentEvents.append(Event(event[0], event[1], event[2], event[3], event[4], event[5], event[6], event[7], event[8], event[9]))
        except Error:
            raise
        finally:
            connection.close()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.dataFrame = QtWidgets.QFrame(self.centralwidget)
        self.dataFrame.setGeometry(QtCore.QRect(600, 0, 300, 600))
        self.dataFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.dataFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.dataFrame.setObjectName("dataFrame")

        self.mapFrame = QtWidgets.QFrame(self.centralwidget)
        self.mapFrame.setGeometry(QtCore.QRect(0, 0, 600, 600))
        self.mapFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.mapFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.mapFrame.setObjectName("mapFrame")

        self.eventsList = QtWidgets.QListView(self.centralwidget)
        self.eventsList.setGeometry(QtCore.QRect(600, 40, 300, 520))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.eventsList.setFont(font)
        self.eventsList.setObjectName("eventsList")
        self.eventsList.clicked.connect(self.onItemClicked)

        self.refreshEventsOnMap()

        self.inoutButton = QtWidgets.QPushButton(self.centralwidget)
        self.inoutButton.setGeometry(QtCore.QRect(600, 0, 150, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.inoutButton.setFont(font)
        self.inoutButton.setObjectName("inoutButton")
        self.inoutButton.setText("Войти в профиль")
        self.inoutButton.clicked.connect(self.onInoutButtonClicked)

        self.profileStatsButton = QtWidgets.QPushButton(self.centralwidget)
        self.profileStatsButton.setGeometry(QtCore.QRect(750, 0, 150, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.profileStatsButton.setFont(font)
        self.profileStatsButton.setObjectName("profileStatsButton")
        self.profileStatsButton.setText("Гость")
        self.profileStatsButton.clicked.connect(self.onProfileStatisticsButtonClicked)
        self.profileStatsButton.setEnabled(False)

        self.addEventButton = QtWidgets.QPushButton(self.centralwidget)
        self.addEventButton.setGeometry(QtCore.QRect(600, 560, 150, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.addEventButton.setFont(font)
        self.addEventButton.setObjectName("addEventButton")
        self.addEventButton.setText("Добавить")
        self.addEventButton.clicked.connect(self.onAddEventButtonClicked)
        self.addEventButton.setEnabled(False)

        self.deleteEventButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteEventButton.setGeometry(QtCore.QRect(750, 560, 150, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.deleteEventButton.setFont(font)
        self.deleteEventButton.setObjectName("deleteEventButton")
        self.deleteEventButton.setText("Удалить")
        self.deleteEventButton.setEnabled(False)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 601, 601))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.mapLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.mapLayout.setContentsMargins(0, 0, 0, 0)
        self.mapLayout.setObjectName("mapLayout")

        coordinate = (53.84553075, 27.467035687537987)
        m = folium.Map(zoom_start=15, location=coordinate)

        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        self.mapLayout.addWidget(webView)

        MainWindow.setCentralWidget(self.centralwidget)

    def onInoutButtonClicked(self):
        if(self.userIn == False):
            self.userIn = True
            dialogProfile = QtWidgets.QDialog()
            dialogProfileUi = Ui_CreateProfileDialog()
            dialogProfileUi.setupUi(dialogProfile)
            dialogProfile.setModal(True)
            if dialogProfile.exec_() == QMessageBox.Accepted:
                self.user = dialogProfileUi.currentUser
                self.inoutButton.setText("Выйти из профиля")
                self.profileStatsButton.setText(self.user.name)
                self.profileStatsButton.setEnabled(True)
                self.addEventButton.setEnabled(True)
                self.deleteEventButton.setEnabled(True)
        else:
            self.userIn = False
            self.inoutButton.setText("Войти в профиль")
            self.profileStatsButton.setText("Аноним")
            self.profileStatsButton.setEnabled(False)
            self.addEventButton.setEnabled(False)
            self.deleteEventButton.setEnabled(False)
            self.refreshEventsOnMap()
        
    def onProfileStatisticsButtonClicked(self):
        self.model = QStandardItemModel()
        item = QStandardItem("Запланированные посещения:")
        item.setFlags(Qt.ItemIsEnabled)
        self.model.appendRow(item)
        for futureEvent in self.user.plannedEvents.values():
            item = QStandardItem(futureEvent)
            self.model.appendRow(item)
        self.eventsList.setModel(self.model)

    def onAddEventButtonClicked(self):
        dialogEvent = QtWidgets.QDialog()
        dialogEventUi = Ui_AddEventDialog()
        dialogEventUi.setupUi(dialogEvent)
        dialogEvent.setModal(True)
        if dialogEvent.exec_() == QMessageBox.Accepted:
            self.currentEvents.append(dialogEventUi.currentEvent)
            self.refreshEventsOnMap()

    def onItemClicked(self, index):
        selectedItem = self.model.itemFromIdex(index)
        if selectedItem:
            self.showEventInfo(selectedItem.text())

    def refreshEventsOnMap(self):
        pass

    def showEventInfo(self, eventName):
        for event in self.currentEvents:
            if event.name == eventName:
                self.model = QStandardItemModel()
                item = QStandardItem(event.name)
                self.model.appendRow(item)
                item.setFlags(Qt.ItemIsEnabled)
                item = QStandardItem(event.description)
                self.model.appendRow(item)
                item.setFlags(Qt.ItemIsEnabled)
                item = QStandardItem(f"Организатор: {event.organizer}")
                self.model.appendRow(item)
                item.setFlags(Qt.ItemIsEnabled)
                item = QStandardItem(f"Когда: {event.datetime}")
                self.model.appendRow(item)
                item.setFlags(Qt.ItemIsEnabled)
                item = QStandardItem("Где: " + ",".join(filter(None, [event.city, event.street, event.house])))
                self.model.appendRow(item)
                item.setFlags(Qt.ItemIsEnabled)
                item = QStandardItem("Посетители:")
                item.setFlags(Qt.ItemIsEnabled)
                self.model.appendRow(item)
                for visitor in event.visitors.values():
                    item = QStandardItem(visitor)
                    item.setFlags(Qt.ItemIsEnabled)
                    self.model.appendRow(item)

                self.eventsList.setModel(self.model)
                item = QStandardItem("Button")
                self.model.appendRow(item)

                button = QPushButton()
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(True)
                font.setWeight(75)
                button.setFont(font)

                if self.user.plannedEvents[event.id] == event.name:
                    button.setText("Посещение запланировано")
                    button.setEnabled(False)
                else:
                    button.setText("Посетить событие")
                    button.clicked.connect(lambda: self.onAddVisitButtonClicked(event, button) )
                
                self.eventsList.setIndexWidget(self.model.index(6 + len(event.visitors), 0), button)
                break
    
    def onAddVisitButtonClicked(self, event, button):
        self.user.addEvent(event)
        button.setText("Посещение запланировано")
        button.setEnabled(False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
