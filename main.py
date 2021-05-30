"""
Kwic Trader trading system
Created by:
Robert (Alex) Spangler
Plant City, FL, USA
Spring of 2021
"""
"""
Title: main module 
The main part of the system which contains the logic for the system GUI.
"""
import sys, requests, sqlite3, webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import QDateTime, pyqtSlot, QTimer
import backTest, environmentVars, broker
import alpaca_trade_api as tradeapi
from PyQt5 import QtWidgets


"""
NOTE: 
After further research I have come to realize that the following methods
can either be replaced with other library methods. 

these methods include the following:

main.displayBackTestHistory(),
main.displayStream(),
backtest.historyData()


"""

"""
NOTE: 
For now the GUI is a simple design
consisting of multiple tables 
"""





class DataTablesWindow(QWidget):
    """
    This "window" gives the user the ability to
    view data.
    """

    def __init__(self, parent=None):
        super(DataTablesWindow, self).__init__(parent)

        # positions window when opened
        qtRectangle = self.frameGeometry()
        centerPointDBW = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPointDBW)
        self.move(qtRectangle.topLeft())

        DBTitle = QLabel("Data Tables")
        DBTitle.setFont(QFont('Arial', 15))

        self.originalPalette = QApplication.palette()

        self.tablesWidget()

        topLayout = QHBoxLayout()

        topLayout.addWidget(DBTitle)

        topLayout.addStretch(1)

        mainLayout = QGridLayout()

        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.tablesWidget, 1, 0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(0, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Kwic Trader - Data Tables")




    def tablesWidget(self):
        """
        Creates the table widgets
        for the DataTables class
        :param: self
        :return: void
        """
        self.tablesWidget = QTabWidget()

        tab1 = QWidget()
        self.table1Widget = QTableWidget(0, 10)
        self.table1Widget.setHorizontalHeaderLabels(["Market Symbol", "Start Date", "End Date", "Total Net Profit",
                                                     "Gross Profit", "Gross Loss", "Profit Factor", "Annual Return",
                                                     "DrawDown", "Sharpe Ratio"])

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(self.table1Widget)
        tab1.setLayout(tab1hbox)
        # call method to display backTestStats table
        DataTablesWindow.displayBackTestStats(self)


        tab2 = QWidget()
        self.table2Widget = QTableWidget(0, 10)
        self.table2Widget.setHorizontalHeaderLabels(["Market Symbol", "Cost/Share", "Profit&Loss/Share", "Profit&Loss",
                                                     "Quantity", "Price", "Position $ Value", "Day Change Profit&Loss",
                                                     "Cost", "P&L %"])

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(self.table2Widget)
        tab2.setLayout(tab2hbox)
        # call method to display backTestStats table
        DataTablesWindow.displayBrokerStats(self)

        self.tablesWidget.addTab(tab1, "BackTest Statistics")
        self.tablesWidget.addTab(tab2, "Portfolio Statistics")

    def displayBackTestStats(self):
        """
        Displays records from the backtestStats table
        in the table1Widget
        :param: self
        :return: void
        """
        connection = sqlite3.connect('kwicTrader.db')
        cur = connection.cursor()

        cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='backtestStats' ''')

        # if the count is 1, then table exists
        if cur.fetchone()[0] == 1:

            # if table exists, create a row for each record.
            results = cur.execute('SELECT * FROM backtestStats')
            self.table1Widget.setRowCount(0)
            for row, form in enumerate(results):
                self.table1Widget.insertRow(row)
                for column, item in enumerate(form):
                    self.table1Widget.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))
        else:
            # else return 0 rows in table.
            self.table1Widget.setRowCount(0)
        # updates table after one second
        QtCore.QTimer.singleShot(1000, self.displayBackTestStats)


    def displayBrokerStats(self):
        """
        Displays records from the brokerStats table
        in table1Widget
        :param: self
        :return: void
        """
        connection = sqlite3.connect('kwicTrader.db')
        cur = connection.cursor()

        cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='brokerStats' ''')

        # if the count is 1, then table exists.
        if cur.fetchone()[0] == 1:
            # if table exists, create a row for each record.
            # --------------------
            # get all necessary values
            costPerShareDict = broker.costPerShare()
            shareProfitDict = broker.shareProfit()
            profitAndLossDict = broker.positionProfit()
            quantityDict = broker.numShares()
            priceDict = broker.currentPrice()
            valueDict = broker.currValue()
            dayChangeDict = broker.dayChange()
            costDict = broker.totalCost()
            pLPercentDict = broker.positionPctProfit()

            # empty list to store market symbol.
            symList = []

            # gets market symbols from quantityDict
            for key in quantityDict:
                symList.append(key)
            # print("passed line 285")
            for mS in symList:

                # updates all BrokerStats table
                cur.execute(f'''UPDATE brokerStats SET Cost_share = {costPerShareDict[mS]},
                                         PnL_share = {round(shareProfitDict[mS], 2)},
                                          PnL = {round(profitAndLossDict[mS], 2)},
                                          Quantity = {quantityDict[mS]}, Price = {priceDict[mS]},
                                          PostionDollarValue = {valueDict[mS]},
                                         DayChange = {round(dayChangeDict[mS], 2)}, Cost = {costDict[mS]},
                                          PnLPercent = {round(pLPercentDict[mS], 2)}
                                         WHERE Market_Symbol = '{mS}';''')


                # ---------------------
                results = cur.execute('SELECT * FROM brokerStats')

                self.table2Widget.setRowCount(0)
                for row, form in enumerate(results):
                    self.table2Widget.insertRow(row)
                    for column, item in enumerate(form):
                        self.table2Widget.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))
                        # self.table2Widget.setItem(row, column, QtWidgets.QTableWidgetItem(cellDict[item]))
        else:
            # else return 0 rows in table.
            self.table2Widget.setRowCount(0)
        # updates table after 10 seconds
        QtCore.QTimer.singleShot(10000, self.displayBrokerStats)


class BackTestWindow(QWidget):
    """
    This window gives the user the ability to
    backtest data from a market they wish to trade in.
    """

    def __init__(self):
        super().__init__()

        # positions window when opened
        qtRectangle = self.frameGeometry()
        centerPointBTW = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPointBTW)
        self.move(qtRectangle.topLeft())

        btTitle = QLabel("BackTest")
        btTitle.setFont(QFont('Arial', 18))

        # Label for market symbol
        mrktBTLabel = QLabel()
        mrktBTLabel.setText("Market Symbol:")

        # Label for start date
        label3 = QLabel()
        label3.setText("Start Date:")

        # Label for stop date
        label4 = QLabel()
        label4.setText("End Date:")


        # textbox for market symbol
        self.mrktBTEtry = QLineEdit()
        startBackTest = QPushButton("Start BackTest", self)
        startBackTest.setDefault(True)
        startBackTest.clicked.connect(self.on_click)

        # Start date for back test
        self.startDate = QDateTimeEdit()
        self.startDate.setDisplayFormat("yyyy-MM-dd")
        self.startDate.setDateTime(QDateTime.currentDateTime().addYears(-1))

        # end date for back test
        self.endDate = QDateTimeEdit()
        self.endDate.setDisplayFormat("yyyy-MM-dd")
        self.endDate.setDateTime(QDateTime.currentDateTime())

        # Set Position of widgets
        btLayout = QGridLayout()

        btLayout.addWidget(btTitle, 0, 1, 1, 2)
        btLayout.addWidget(mrktBTLabel, 1, 0, 1, 2)
        btLayout.addWidget(self.mrktBTEtry, 1, 2, 1, 2)
        btLayout.addWidget(label3, 3, 0, 1, 2)
        btLayout.addWidget(self.startDate, 3, 2, 1, 2)
        btLayout.addWidget(label4, 4, 0, 1, 2)
        btLayout.addWidget(self.endDate, 4, 2, 1, 2)
        btLayout.addWidget(startBackTest, 5, 1, 1, 2)

        self.setLayout(btLayout)
        self.setWindowTitle("Kwic Trader - BackTest")

    # used to call backTest.displayBackTest method
    # link to info: https://pythonspot.com/pyqt5-buttons/
    @pyqtSlot()
    def on_click(self):
        # Checks if market symbol ('alpaca_trade_api.entity.Asset') is valid.
        try:
            apiRest = tradeapi.REST(environmentVars.API_KEY, environmentVars.SECRET_KEY)

            apiRest.get_asset(self.mrktBTEtry.text().upper())

        except:
            # show error message
            return QMessageBox.critical(self, "ERROR!", "INVALID MARKET SYMBOL!!"
                                                 "\n\nPlease reenter a valid market symbol (e.g TSLA for Tesla).")

        backTest.runBackTest(self.mrktBTEtry.text().upper(), self.startDate.text(), self.endDate.text())


class MainWindow(QMainWindow):
    """
    contains logic for the home window
    """

    def __init__(self):
        super().__init__()
        # Check internet connection
        try:
            # Makes a request to a set url
            requests.get("https://www.google.com/", timeout=5)
        except (requests.ConnectionError, requests.Timeout):
            # Displays error message if request fails
            QMessageBox.critical(self, "ERROR!", "NO INTERNET CONNECTION!!"
                                                 "\n\nPlease check your network connection.")
            # exit application if there's no internet
            exit()



        self.BackTestWindow = BackTestWindow()
        self.DataTablesWindow = DataTablesWindow()

        # centers window when opened
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.setWindowTitle("Kwic Trader")

        layoutMain = QVBoxLayout()

        # creating title
        self.title = QLabel("Kwic Trader")
        self.title.setFont(QFont('Arial', 20))
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        layoutMain.addWidget(self.title)

        streamButton = QPushButton("Stream Live Market Data")
        streamButton.clicked.connect(self.tradeDataStream)
        # streamButton.clicked.connect(self.toggle_streamWindow)
        layoutMain.addWidget(streamButton)

        backTestButton = QPushButton("BackTest")
        backTestButton.clicked.connect(self.toggle_BackTestWindow)
        layoutMain.addWidget(backTestButton)

        viewDataButton = QPushButton("View Data")
        viewDataButton.clicked.connect(self.toggle_DBTablesWindow)
        layoutMain.addWidget(viewDataButton)

        mainWidget = QWidget()
        mainWidget.setLayout(layoutMain)
        self.setCentralWidget(mainWidget)

    # used to toggle on BackTestWindow
    def toggle_BackTestWindow(self, checked):
        if self.BackTestWindow.isVisible():
            self.BackTestWindow.hide()

        else:
            self.BackTestWindow.show()

    # used to toggle on DBTablesWindow
    def toggle_DBTablesWindow(self, checked):
        if self.DataTablesWindow.isVisible():
            self.DataTablesWindow.hide()

        else:
            self.DataTablesWindow.show()

    # used for Streaming Live market data
    def tradeDataStream(self, checked):
        """
        Launches users default web browser and connects
        to the url for TradingView.
        :return: void
        """
        webbrowser.open("https://www.tradingview.com/")


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()


