from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Classes.TCPThread import TCPThread
from Classes.TCPObserver import TCPObserver


class Ui_MainWindow(TCPObserver):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(798, 447)
        font = QtGui.QFont()
        font.setFamily("Quicksand")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 140, 579, 259))
        self.scrollArea.setStyleSheet("font: 8pt \"Quicksand\";")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 560, 257))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 561, 261))
        self.tableWidget.setMaximumSize(QtCore.QSize(561, 16777215))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(1)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Quicksand")
        item.setFont(font)
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Quicksand")
        font.setPointSize(14)
        item.setFont(font)
        item.setBackground(QtGui.QColor(114, 236, 124))
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 781, 131))
        font = QtGui.QFont()
        font.setFamily("Quicksand")
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(580, 140, 211, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Quicksand")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 798, 24))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.actionListen_options = QtWidgets.QAction(MainWindow)
        self.actionListen_options.setObjectName("actionListen_options")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.menuMenu.addAction(self.actionListen_options)
        self.menuMenu.addAction(self.actionImport)
        self.menuMenu.addAction(self.actionExport)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionExit)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.bindFunctions()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Data"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("MainWindow", "Reading from socket..."))
        self.pushButton.setText(_translate("MainWindow", "Copy new data to clipboard"))
        self.menuMenu.setTitle(_translate("MainWindow", "File"))
        self.actionListen_options.setText(_translate("MainWindow", "Server options"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionImport.setText(_translate("MainWindow", "Import"))

    def bindFunctions(self):
        print("Good joke")

    def notify(self, data):
        self.addItems(str(data))

    def addItems(self, data):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        next = ''
        for x in range(self.tableWidget.rowCount()):
            if x == self.tableWidget.rowCount()-1:
                break
            if x == 0:
                next = self.tableWidget.item(x,0).text()
                print(next)
                self.tableWidget.setItem(x, 0, QtWidgets.QTableWidgetItem(str(data)[2:-1]))
                continue
            try:
                current = self.tableWidget.item(x, 0).text()
                self.tableWidget.setItem(x, 0, QtWidgets.QTableWidgetItem(next))
                next = current
                print(current)
            except:
                self.tableWidget.setItem(x, 0, QtWidgets.QTableWidgetItem(next))

      # self.tableWidget.setItem(self.tableWidget.rowCount() - 2, 1, QtWidgets.QTableWidgetItem(data))

