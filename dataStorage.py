"""
Kwic Trader trading system
Created by:
Robert (Alex) Spangler
Plant City, FL, USA
Spring of 2021
"""
import sqlite3

"""
Title: dataStorage module 
Contains the logic to store data and encrypt sensitive data.
"""

"""
NOTE:
The methods encryptData() and decryptData() have been omitted
due to none of the data in persistent storage being sensitive enough 
for any type of encryption to be needed. 
"""


# create connection to DB
conn = sqlite3.connect('kwicTrader.db')
cursor = conn.cursor()


# backtestStatRecord method under construct
def backtestStatsRecord(mrktSym, startDate, endDate, netPrft, grssPrft, grssLoss, prftFactr,
                        annRtrn, drwDown, shrpRatio):
    """
    Creates a record for the back test statistics table.
    :param: mrktSym: String
    :param: startDate: String
    :param: endDate: String
    :param: netPrft: float
    :param: grssPrft: float
    :param: grssLoss: float
    :param: prftFactr: float
    :param: annRtrn: float
    :param: drwDown: float
    :param: shrpRatio: float
    :return: void
    """

    # get the count of tables with the name
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='backtestStats' ''')

    # if the count is 1, then table exists
    if cursor.fetchone()[0] == 1:
        print('The backtestStats table exists.')
    else:
        # Create Table
        cursor.execute('''CREATE TABLE backtestStats
                   (Market_Symbol, Start_Data, End_Date, Total_Net_Profit, Gross_Profit, Gross_Loss, Profit_Factor,
                   Annual_Return, Draw_Down, Sharpe_Ratio)''')

    # Insert a row of data
    cursor.execute(f'''INSERT INTO backtestStats VALUES ('{mrktSym}', '{startDate}', '{endDate}',
    {netPrft}, {grssPrft}, {grssLoss}, {prftFactr},{annRtrn}, {drwDown}, {shrpRatio})''')

    # Save (commit) the changes
    conn.commit()

    # TODO: remove test code below
    # Select a record from DB - TEST CODE
    # ---------Testing---------------------
    t = (mrktSym,)
    cursor.execute('SELECT * FROM backtestStats WHERE Market_Symbol=?', t)
    # Prints record - TEST CODE
    print("New Record:")
    print(cursor.fetchone())
    # ---------Testing---------------------


"""
NOTE:
realTimeStatsRecord has been changed to brokerStatRecord
"""


# brokerStatRecord method under construct
def brokerStatsRecord(mrktSym, cost_share, profLossShare, profit_Loss, quantity, price, postionDollarVal,
                      dayChange, cost, profitLossPercent):
    """
    Creates a record for the broker Statistics
    table in persistent storage.
    :param: mrktSym: String
    :param: cost_share: float
    :param: profLossShare: float
    :param: profit_Loss: float
    :param: quantity: int
    :param: price: float
    :param: postionDollarVal: float
    :param: dayChange: float
    :param: cost: float
    :param: profitLossPercent: float
    :return: void
    """
    # get the count of tables with the name
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='brokerStats' ''')

    # if the count is 1, then table exists
    if cursor.fetchone()[0] == 1:
        print('The brokerStats table exists.')
    else:
        # Create Table
        cursor.execute('''CREATE TABLE brokerStats
                       (Market_Symbol, Cost_share, PnL_share, PnL, Quantity, Price, PostionDollarValue, 
                       DayChange, Cost, PnLPercent)''')

    # Insert a row of data
    cursor.execute(f'''INSERT INTO brokerStats VALUES ('{mrktSym}', {cost_share}, {profLossShare},{profit_Loss},
        {quantity}, {price}, {postionDollarVal}, {dayChange}, {cost}, {profitLossPercent})''')

    # Save (commit) the changes
    conn.commit()

    # TODO: remove test code below
    # Select a record from DB - TEST CODE
    # ---------Testing---------------------

    t = (mrktSym,)
    cursor.execute('SELECT * FROM brokerStats WHERE Market_Symbol=?', t)
    # Prints record - TEST CODE
    print("New Record:")
    print(cursor.fetchone())

    # ---------Testing---------------------



