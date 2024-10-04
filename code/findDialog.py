from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from geopy.geocoders import Nominatim
from PyQt5.QtCore import QDate

class Ui_FindDialog(object):
    def setupUi(self, FindDialog, events):
        FindDialog.setObjectName("FindDialog")
        FindDialog.resize(340, 300)
        FindDialog.setWindowTitle("Поиск")
        self.FindDialog = FindDialog

        self.location = None
        self.name = None
        self.events = events

        self.tabWidget = QtWidgets.QTabWidget(FindDialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 340, 235))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")

        self.placeFind = QtWidgets.QWidget()
        self.placeFind.setObjectName("placeFind")

        self.addressLine = QtWidgets.QLineEdit(self.placeFind)
        self.addressLine.setGeometry(QtCore.QRect(20, 40, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.addressLine.setFont(font)
        self.addressLine.setObjectName("addressLine")

        self.addressLabel = QtWidgets.QLabel(self.placeFind)
        self.addressLabel.setGeometry(QtCore.QRect(20, 10, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.addressLabel.setFont(font)
        self.addressLabel.setObjectName("addressLabel")
        self.addressLabel.setText("Область поиска:")

        self.nameFind = QtWidgets.QWidget()
        self.nameFind.setObjectName("nameFind")

        self.nameLine = QtWidgets.QLineEdit(self.nameFind)
        self.nameLine.setGeometry(QtCore.QRect(20, 40, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nameLine.setFont(font)
        self.nameLine.setObjectName("nameLine")
        self.nameLine.textChanged.connect(self.onNameChanged)

        self.nameLabel = QtWidgets.QLabel(self.nameFind)
        self.nameLabel.setGeometry(QtCore.QRect(20, 10, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Название события:")

        self.eventsList = QtWidgets.QListView(self.nameFind)
        self.eventsList.setGeometry(QtCore.QRect(20, 70, 300, 140))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.eventsList.setFont(font)
        self.eventsList.setObjectName("eventsList")

        model = QStandardItemModel()
        for event in self.events:
            item = QStandardItem(event.name)
            model.appendRow(item)
        self.eventsList.setModel(model)


        self.dateFind = QtWidgets.QWidget()
        self.dateFind.setObjectName("dateFind")

        self.dateLabel = QtWidgets.QLabel(self.dateFind)
        self.dateLabel.setGeometry(QtCore.QRect(20, 10, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.dateLabel.setFont(font)
        self.dateLabel.setObjectName("dateLabel")
        self.dateLabel.setText("Дата события:")

        self.dateEdit = QtWidgets.QDateEdit(self.dateFind)
        self.dateEdit.setGeometry(QtCore.QRect(20, 40, 300, 30))
        self.dateEdit.setDate(QDate.currentDate())
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.dateEdit.setFont(font)
        self.dateEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.dateChanged.connect(self.onDateChanged)

        self.eventsDateList = QtWidgets.QListView(self.dateFind)
        self.eventsDateList.setGeometry(QtCore.QRect(20, 70, 300, 140))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.eventsDateList.setFont(font)
        self.eventsDateList.setObjectName("eventsDateList")
        
        self.findButton = QtWidgets.QPushButton(FindDialog)
        self.findButton.setGeometry(QtCore.QRect(30, 250, 130, 35))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.findButton.setFont(font)
        self.findButton.setObjectName("findButton")
        self.findButton.setText("Найти")
        self.findButton.clicked.connect(self.onFindButtonClicked)

        self.cancelButton = QtWidgets.QPushButton(FindDialog)
        self.cancelButton.setGeometry(QtCore.QRect(180, 250, 130, 35))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.cancelButton.setFont(font)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText("Отмена")

        self.tabWidget.addTab(self.placeFind, "")
        self.tabWidget.addTab(self.nameFind, "")
        self.tabWidget.addTab(self.dateFind, "")
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.placeFind), "По месту")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.nameFind), "По названию")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dateFind), "По дате")

    def onNameChanged(self, text):
        model = QStandardItemModel()
        for event in self.events:
            if text in event.name or text == "":
                item = QStandardItem(event.name)
                model.appendRow(item)
        self.eventsList.setModel(model) 

    def onDateChanged(self):
        model = QStandardItemModel()
        for event in self.events:
            if self.dateEdit.date().toString("yyyy-MM-dd") == event.datetime.split(" ")[0]:
                item = QStandardItem(event.name)
                model.appendRow(item)
        self.eventsDateList.setModel(model)

    def onFindButtonClicked(self):
        try: 
            if self.tabWidget.currentIndex() == 0:
                if self.addressLine.text().strip() == "":
                    raise ValueError("Введите область поиска")
                
                geolocator = Nominatim(user_agent="alla123425")
                location = geolocator.geocode(self.addressLine.text())

                if location:
                    self.location = (location.latitude, location.longitude)
                    self.FindDialog.accept()
                else:
                    raise ValueError("Адрес не найден")

            elif self.tabWidget.currentIndex() == 1:
                selected_items = self.eventsList.selectedIndexes()
                if selected_items:
                    self.name = selected_items[0].data()
                    self.FindDialog.accept()
                else:
                    raise ValueError("Введите название события и выберите интересующее")
            else:
                selected_items = self.eventsDateList.selectedIndexes()
                if selected_items:
                    self.name = selected_items[0].data()
                    self.FindDialog.accept()
                else:
                    raise ValueError("Введите дату события и выберите интересующее")
        except ValueError as e:
            QMessageBox.warning(self.FindDialog, "Недостаточно данных", str(e), QMessageBox.Ok)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FindDialog = QtWidgets.QDialog()
    ui = Ui_FindDialog()
    ui.setupUi(FindDialog)
    FindDialog.show()
    sys.exit(app.exec_())
