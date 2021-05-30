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
Tests for the portfolioDayChange() method

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

"""
pytests created for functions
in the broker module
"""

import broker


"""
Tests for the currentPositionValue() method
"""


"""
Tests for the portfolioValue() method
"""


# checks if return type for portfolioValue() is a dictionary
def test_portfolioValue_checkReturnType():
    assert type(broker.portfolioValue()) is dict



"""
Tests for the dayChange() method
"""
# checks if return type for dayChange() is a dictionary
def test_dayChange_checkReturnType():
    assert type(broker.dayChange()) is dict


"""
Tests for shareChange()
"""

def test_shareChange_checkReturnType():
    assert type(broker.shareChange()) is dict


"""
Tests for the totalCost() method
"""
# checks if return type for totalCost() is a float
def test_totalCost_checkReturnType():
    assert type(broker.totalCost()) is dict


"""
Tests for the portPctProfit() method
"""


# checks if return type for portPctProfit() is a float
def test_portfolioValue_checkReturnType():
    assert type(broker.portPctProfit()) is float


"""
Tests for the portProfit() method
"""


# checks if return type for portfolioValue() is a float
def test_portProfit_checkReturnType():
    assert type(broker.portProfit()) is float


"""
Tests for the portPctProfit() method
"""


# checks if return type for portPctProfit() is a float
def test_portPctProfit_checkReturnType():
    assert type(broker.portPctProfit()) is float
