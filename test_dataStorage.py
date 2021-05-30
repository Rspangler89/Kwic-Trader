"""
Kwic Trader trading system
Created by:
Robert (Alex) Spangler
Plant City, FL, USA
Spring of 2021
"""

"""
NOTE: 
Due to time constraints I only had time to write a few Unit tests for the new methods created,
 although there are not as many as before. 
"""


"""
pytests created for functions
in the dataStorage module

To set up pytest in pycharm follow the directions below:

 1.) Go to File>Settings.
 2.) Click on the dropdown menu "Project: Kwic Trader".
 3.) Click on "Project Interpreter"
 4.) Click on the + sign in the lower left hand corner.
 5.) search for pytest in the searchbar.
 6.) select pytest then click "Install Package" in the lower left hand corner.
 7.) After it states that it's successfully installed, close the "Available Packages" window.
 8.) In the settings window select the "Tools" dropdown menu.
 9.) Click on "Python Integrated Tools"
10.) Under "Testing" go to the "Default Test Runner" dropdown menu and select "Pytest".
11.) Under "reStructuredText" go to the textbox labeled "Sphinx Working Directory"
     and click on the folder icon in the right hand corner.
12.) Select "Kwic Trader" and click okay.
13.) Back in the Settings window click the "Apply" button in the lower right hand corner
     then click okay.
14.) Now in the top menu bar go to Run>"Edit Configurations..."
15.) click the + sign in the upper left hand corner and go to the Pytest drop menu.
16.) Under Pytest select "pytest".
17.) Under the "Python Test" menu select "Pytest in Kwic Trader".
18.) Go to the textbox labeled "Working Directory" and click on the folder icon in the right hand corner
     and select "Kwic Trader".
19.) In the same menu go to "target" and make sure "Script path" is selected.
20.) In the textbox under "target" click on the folder icon in the right hand corner and select "Kwic Trader".
21.) Click the "Apply" button in the lower right hand corner then click okay.
22.) To run Pytest go to the dropdown menu in the upper right hand corner next to the green ">" run button
     and select "pytest in Kwic Trader" the run button.

for more info click the link to the youtube video below

youtube video: https://www.youtube.com/watch?v=WJKLjFwRHIY


"""
import dataStorage
import pytest
import sqlite3


"""
NOTE:
The test methods encryptData() and decryptData() have been omitted
due to none of the data in persistent storage being sensitive enough 
for any type of encryption to be needed. 
"""

"""
Tests for  backtestStatRecord() method below
"""


# check if record is created in the table
# Reference Link: https://medium.com/@geoffreykoh/fun-with-fixtures-for-database-applications-8253eaf1a6d
@pytest.fixture
def setup_backtestStatsRecord():
    """ Fixture to set up the in-memory database with test data """
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
           CREATE TABLE backtestStats
           (Market_Symbol, Start_Data, End_Date, Total_Net_Profit, Gross_Profit, Gross_Loss, Profit_Factor,
                   Annual_Return, Draw_Down, Sharpe_Ratio)''')
    sample_data = [
        ('IBM', "2020-04-23", "2021-04-23", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00)
    ]
    cursor.executemany('INSERT INTO backtestStats VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', sample_data)
    yield conn


def test_backtestStatRecord_checkForInsertedRecord(backtestStatsRecord):
    cursor = backtestStatsRecord
    assert len(list(cursor.execute('SELECT * FROM backtestStatistics'))) == 1


"""
Tests for  realTimeStatRecord() method below
"""


# check if record is created in the table
# Reference Link: https://medium.com/@geoffreykoh/fun-with-fixtures-for-database-applications-8253eaf1a6d
@pytest.fixture
def setup_brokerStatRecord():
    """ Fixture to set up the in-memory database with test data """
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
               CREATE TABLE brokerStats
               (Market_Symbol, Cost_share, PnL_share, PnL, Quantity, Price, PostionDollarValue, 
                       DayChange, Cost, PnLPercent)''')
    sample_data = [
        ('IBM', 0.00, 0.00, 0.00, 0, 0.00, 0.00, 0.00, 0.00, 0.00)
    ]
    cursor.executemany('INSERT INTO brokerStats VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', sample_data)
    yield conn


def test_brokerStatRecord_checkForInsertedRecord(brokerStatsRecord):
    cursor = brokerStatsRecord
    assert len(list(cursor.execute('SELECT * FROM realTimeStatistics'))) == 1


