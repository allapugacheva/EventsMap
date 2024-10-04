from PyQt5 import QtCore, QtGui, QtWidgets
from createProfileDialog import Ui_CreateProfileDialog
from addEventDialog import Ui_AddEventDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMessageBox, QPushButton, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QUrl
from mysql.connector import connect, Error
from event import Event
from map import Map
from inProfileDialog import Ui_inProfileDialog
from findDialog import Ui_FindDialog
from datetime import datetime

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(900, 600)
        MainWindow.setWindowTitle("Карта событий")

        self.lastCoordinates = None
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
                        SELECT name, description, organizer, datetime, place, latitude, longitude
                        FROM event
                        """
                        cursor.execute(select_events_query)
                        events = cursor.fetchall()
                        if events:
                            for event in events:
                                if datetime.strptime(event[3], "%Y-%m-%d %H:%M") > datetime.now().replace(second=0, microsecond=0):
                                    self.currentEvents.append(Event(event[0], event[1], event[2], event[3], event[4], event[5], event[6], True))
                                else:
                                    delete_event_query = f"""
                                    DELETE FROM event
                                    WHERE name = '{event[0]}';
                                    """
                                    cursor.execute(delete_event_query)
                                    connection.commit()
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

        self.inoutButton = QtWidgets.QPushButton(self.centralwidget)
        self.inoutButton.setGeometry(QtCore.QRect(600, 0, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.inoutButton.setFont(font)
        self.inoutButton.setObjectName("inoutButton")
        self.inoutButton.setText("Вход")
        self.inoutButton.clicked.connect(self.onInOutButtonClicked)

        self.registerButton = QtWidgets.QPushButton(self.centralwidget)
        self.registerButton.setGeometry(QtCore.QRect(700, 0, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.registerButton.setFont(font)
        self.registerButton.setObjectName("registerButton")
        self.registerButton.setText("Регистрация")
        self.registerButton.clicked.connect(self.onRegisterButtonClicked)

        self.profileStatsButton = QtWidgets.QPushButton(self.centralwidget)
        self.profileStatsButton.setGeometry(QtCore.QRect(800, 0, 100, 40))
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
        self.addEventButton.setGeometry(QtCore.QRect(600, 560, 100, 40))
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
        self.deleteEventButton.setGeometry(QtCore.QRect(800, 560, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.deleteEventButton.setFont(font)
        self.deleteEventButton.setObjectName("deleteEventButton")
        self.deleteEventButton.setText("Удалить")
        self.deleteEventButton.setEnabled(False)
        self.deleteEventButton.clicked.connect(self.onDeleteEventButtonClicked)

        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.editButton.setGeometry(QtCore.QRect(700, 560, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.editButton.setFont(font)
        self.editButton.setObjectName("editButton")
        self.editButton.setText("Изменить")
        self.editButton.setEnabled(False)
        self.editButton.clicked.connect(lambda: self.onAddEventButtonClicked(True))

        self.findButton = QtWidgets.QPushButton(self.centralwidget)
        self.findButton.setGeometry(QtCore.QRect(600, 525, 35, 35))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.findButton.setFont(font)
        self.findButton.setObjectName("findButton")  
        self.findButton.setText("🔍") 
        self.findButton.clicked.connect(self.onFindButtonClicked)
        self.findButton.raise_()  

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 600, 600))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.mapLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.mapLayout.setContentsMargins(0, 0, 0, 0)
        self.mapLayout.setObjectName("mapLayout")

        self.webView = QWebEngineView()
        self.mapLayout.addWidget(self.webView)
        self.reloadMap()
        self.webView.loadFinished.connect(lambda: self.webView.page().runJavaScript(f"{self.map.map_variable_name}.fire('moveend');") )

        MainWindow.setCentralWidget(self.centralwidget)         

    def onFindButtonClicked(self):
        dialogFind = QtWidgets.QDialog()
        dialogFindUi = Ui_FindDialog()
        dialogFindUi.setupUi(dialogFind, self.currentEvents)
        dialogFind.setModal(True)
        if dialogFind.exec_() == QMessageBox.Accepted:
            if dialogFindUi.location:
                self.lastCoordinates = dialogFindUi.location
                self.webView.loadFinished.connect(lambda: self.webView.page().runJavaScript(f"{self.map.map_variable_name}.fire('moveend');") )                
                self.reloadMap()
            else:
                for event in self.currentEvents:
                    if event.name == dialogFindUi.name:
                        self.lastCoordinates = (event.latitude, event.longitude)
                        self.webView.loadFinished.connect(lambda: self.webView.page().runJavaScript(f"{self.map.markers[event.name]}.fireEvent('click');") )
                        self.reloadMap()
                        break

    def onInOutButtonClicked(self):
        if(self.userIn == False):
            self.userIn = True
            dialogProfile = QtWidgets.QDialog()
            dialogProfileUi = Ui_inProfileDialog()
            dialogProfileUi.setupUi(dialogProfile)
            dialogProfile.setModal(True)
            if dialogProfile.exec_() == QMessageBox.Accepted:
                self.user = dialogProfileUi.currentUser
                self.inoutButton.setText("Выход")
                self.profileStatsButton.setText(self.user.name)
                self.profileStatsButton.setEnabled(True)
                self.registerButton.setText("Изменить")
                self.addEventButton.setEnabled(True)
                self.reloadMap()   
        else:
            self.userIn = False
            self.inoutButton.setText("Вход")
            self.registerButton.setText("Регистрация")
            self.profileStatsButton.setText("Аноним")
            self.profileStatsButton.setEnabled(False)
            self.addEventButton.setEnabled(False)
            self.deleteEventButton.setEnabled(False)
            self.editButton.setEnabled(False)

    def onRegisterButtonClicked(self):
        if self.userIn == False:
            dialogProfile = QtWidgets.QDialog()
            dialogProfileUi = Ui_CreateProfileDialog()
            dialogProfileUi.setupUi(dialogProfile)
            dialogProfile.setModal(True)
            if dialogProfile.exec_() == QMessageBox.Accepted:
                self.userIn = True
                self.user = dialogProfileUi.currentUser
                self.inoutButton.setText("Выход")
                self.profileStatsButton.setText(self.user.name)
                self.profileStatsButton.setEnabled(True)
                self.registerButton.setText("Изменить")
                self.addEventButton.setEnabled(True)
                self.reloadMap()   
        else:
            dialogProfile = QtWidgets.QDialog()
            dialogProfileUi = Ui_CreateProfileDialog() # params
            dialogProfileUi.setupUi(dialogProfile)
            dialogProfile.setModal(True)
            if dialogProfile.exec_() == QMessageBox.Accepted:
                self.userIn = True
                self.user = dialogProfileUi.currentUser  
        
    def onProfileStatisticsButtonClicked(self):
        self.eventsList.setSelectionMode(QListView.NoSelection)
        self.eventsList.clicked.disconnect()
        self.model = QStandardItemModel()
        item = QStandardItem("Запланированные посещения:")
        self.model.appendRow(item)
        for futureEvent in self.user.plannedEvents:
            item = QStandardItem(futureEvent)
            self.model.appendRow(item)
        self.eventsList.setModel(self.model)

        item = QStandardItem("Exit")
        item.setFlags(Qt.ItemIsEnabled)
        self.model.appendRow(item)

        button = QPushButton()
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        button.setFont(font)
        button.setText("Выход в список")
        button.clicked.connect(lambda: self.webView.page().runJavaScript(f"{self.map.map_variable_name}.fire('click');"))
        self.eventsList.setIndexWidget(self.model.index(1 + len(self.user.plannedEvents), 0), button)

    def reloadMap(self):
        coordinates = None
        if self.lastCoordinates != None:
            coordinates = self.lastCoordinates
            self.lastCoordinates = None
        elif self.userIn:
            coordinates = (self.user.defaultLatitude, self.user.defaultLongitude)
        else:
            coordinates = (53.902287, 27.561824)

        self.map = Map(r"code\folium-map.html", coordinates, self.currentEvents)
        self.map.position_changed.connect(self.refreshEventsOnMap)
        self.map.marker_clicked.connect(self.showEventInfo)
        self.webView.load(QUrl.fromLocalFile(r"D:\EventsMap\code\folium-map.html"))

    def selectionChangedHandler(self):
        selected_indexes = self.eventsList.selectedIndexes()

        if selected_indexes and self.userIn:
            for event in self.currentEvents:
                if event.name == selected_indexes[0].data():
                    if event.organizer == self.user.name:
                        self.editButton.setEnabled(True)
                        self.deleteEventButton.setEnabled(True)
                        break
        else:
            self.editButton.setEnabled(True)
            self.deleteEventButton.setEnabled(True)

    def handleCoordinates(self, result):
        self.lastCoordinates = tuple(map(float, result.split(',')))

    def onAddEventButtonClicked(self, edit = False):
        self.webView.page().runJavaScript("getCenterCoordinates()", self.handleCoordinates)

        dialogEvent = QtWidgets.QDialog()
        dialogEventUi = Ui_AddEventDialog()
        dialogEventUi.setupUi(dialogEvent, self.user.name)
        if edit:
            selected_indexes = self.eventsList.selectedIndexes()
            if selected_indexes:
                selected_item = selected_indexes[0].data()
                for event in self.currentEvents:
                    if event.name == selected_item:
                        dialogEventUi.enableEdit(event.name, event.description, event.datetime, event.address)
                        break
        dialogEvent.setModal(True)
        if dialogEvent.exec_() == QMessageBox.Accepted:
            self.currentEvents.append(dialogEventUi.currentEvent)
            self.reloadMap()

    def onDeleteEventButtonClicked(self):
        selected_indexes = self.eventsList.selectedIndexes()
        if selected_indexes:
            selected_item = selected_indexes[0].data()

            try:
                with connect(
                        host="localhost",
                        user="root",
                        password="13579",
                        port="3307",
                        database="eventsmapdb"
                    ) as connection:
                        with connection.cursor() as cursor:

                            delete_event_query = f"""
                            DELETE FROM event
                            WHERE name = '{selected_item}';
                            """
                            cursor.execute(delete_event_query)
                            connection.commit()
            except Error:
                raise
            finally:
                connection.close()


    def onItemClicked(self, index):
        selectedItem = self.model.itemFromIndex(index)
        if selectedItem:
            self.eventsList.setSelectionMode(QListView.NoSelection)
            self.eventsList.clicked.disconnect()
            self.webView.page().runJavaScript(f'''
                {self.map.markers[selectedItem.text()]}.fireEvent('click');
            ''')

    def refreshEventsOnMap(self, rdlat, rdlng, lulat, lulng):
        self.eventsList.clicked.connect(self.onItemClicked)
        self.eventsList.setSelectionMode(QListView.SingleSelection)
        self.model = QStandardItemModel()

        for event in self.currentEvents:
            if (rdlat >= event.latitude >= lulat) and (rdlng <= event.longitude <= lulng):
                item = QStandardItem(event.name)
                self.model.appendRow(item)
            
        self.eventsList.setModel(self.model)
        selection_model = self.eventsList.selectionModel()
        selection_model.selectionChanged.connect(self.selectionChangedHandler)

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
                item = QStandardItem(f"Где: {event.place}")
                self.model.appendRow(item)
                item.setFlags(Qt.ItemIsEnabled)
                item = QStandardItem("Посетители:")
                item.setFlags(Qt.ItemIsEnabled)
                self.model.appendRow(item)
                for visitor in event.visitors:
                    item = QStandardItem(visitor)
                    item.setFlags(Qt.ItemIsEnabled)
                    self.model.appendRow(item)

                self.eventsList.setModel(self.model)

                if self.userIn:
                    item = QStandardItem("Button")
                    self.model.appendRow(item)

                    button = QPushButton()
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    font.setBold(True)
                    font.setWeight(75)
                    button.setFont(font)

                    if event.name in self.user.plannedEvents:
                        button.setText("Посещение запланировано")
                        button.setEnabled(False)
                    else:
                        button.setText("Посетить событие")
                        button.clicked.connect(lambda: self.onAddVisitButtonClicked(event))
                    
                    self.eventsList.setIndexWidget(self.model.index(6 + len(event.visitors), 0), button)

                item = QStandardItem("Exit")
                self.model.appendRow(item)

                bbutton = QPushButton()
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(True)
                font.setWeight(75)
                bbutton.setFont(font)
                bbutton.setText("Выход в список")
                bbutton.clicked.connect(lambda: self.webView.page().runJavaScript(f"{self.map.map_variable_name}.fire('click');"))
                self.eventsList.setIndexWidget(self.model.index((7 if self.userIn else 6) + len(event.visitors), 0), bbutton)
                break
    
    def onAddVisitButtonClicked(self, event):
        self.user.addEvent(event)
        self.webView.page().runJavaScript(f'''
                {self.map.markers[event.name]}.fireEvent('click');
            ''')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
