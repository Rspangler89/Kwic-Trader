"""
Kwic Trader trading system
Created by:
Robert (Alex) Spangler
Plant City, FL, USA
Spring of 2021
"""


"""
Title: broker module 
contains the logic for connecting to the broker.

From : https://alpaca.markets/docs/api-documentation/api-v2/positions/
"The positions API provides information about an account’s current open positions.
Information such as cost basis, shares traded, and market value, updated live as price 
information is updated. Once a position is closed, it will no longer be queryable 
through this API."

Position JSON Object/Entity Example:
{
  "asset_id": "904837e3-3b76-47ec-b432-046db621571b",
  "symbol": "AAPL",
  "exchange": "NASDAQ",
  "asset_class": "us_equity",
  "avg_entry_price": "100.0",
  "qty": "5",
  "side": "long",
  "market_value": "600.0",
  "cost_basis": "500.0",
  "unrealized_pl": "100.0",
  "unrealized_plpc": "0.20",
  "unrealized_intraday_pl": "10.0",
  "unrealized_intraday_plpc": "0.0084",
  "current_price": "120.0",
  "lastday_price": "119.0",
  "change_today": "0.0084"
}

"""

import alpaca_trade_api as tradeapi
import environmentVars, dataStorage
import sqlite3


MY_API_KEY = environmentVars.API_KEY
MY_SECRET_KEY = environmentVars.SECRET_KEY
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(MY_API_KEY, MY_SECRET_KEY, BASE_URL, api_version='v2')


# Get a list of all positions.
portfolio = api.list_positions()



#Portfolio methods are below.
#These methods/functions return values and most return and store values in
#dictionaries keyed by the asset symbol.The dictionaries are accessed
#in the "main" module to populate the brokerage table for display to the user.
#NOTE: a "position" is the collection of identical shares/contracts
#of a single financial asset, such as a stock,bond, or futures contract.
#For development purposes, only stocks are used.


def numShares():
    """
    Number of Shares
    Stores the number of shares comprising each position in a dictionary
    with the market symbol as the key.
    :return: dictionary
    """
    numshares = dict()
    for position in portfolio:
        numshares[position.symbol] = position.qty
    return numshares


def currentPrice():
    """
    Current Price
    Stores the current price for each share in a position in a dictionary
    with the market symbol as the key.
    :return: dictionary
    """
    currentprice = dict()
    for position in portfolio:
        currentprice[position.symbol] = position.current_price
    return currentprice


def costPerShare( ):
    """
    Cost per Share
    The amount paid at entry per share
    :return: dictionary
    """
    cstshare = dict()
    for position in portfolio:
        # Strings are returned from API; convert to floating point type
        cost = float(position.avg_entry_price)
        cstshare[position.symbol] = cost
    return cstshare


def currValue():
    """
    Current Position Value
    Store the current total market value of each portfolio position
    in a dictionary with the market symbol as the key.This is market_value
    from the Alpaca API and is equal to the current_price * qty (number of shares)
    of each asset position.
    :return: dictionary
    """
    currvalue = dict()
    for position in portfolio:
        # Strings are returned from API; convert to floating point type
        mktvalue = float(position.market_value)
        currvalue[position.symbol] = mktvalue
    return currvalue


def totalCost():
    """
    Total Cost
    This method returns a dictionary of the total price paid for each asset,
    which is cost_basis from the Alpaca API.
    :return: dictionary
    """
    totalcost = dict()
    for position in portfolio:
        # Strings are returned from API; convert to floating point type
        cost = float(position.cost_basis)
        totalcost[position.symbol] = cost
    return totalcost


def shareChange():
    """
    Share Change
    Calculates and stores in a dictionary the current change in asset
    price per share since yesterday, which is current_price - lastday_price
    :return: dictionary
    """
    sharechange = dict()
    for position in portfolio:
        # Strings are returned from API; convert to floating point type
        current = float(position.current_price)
        last = float(position.lastday_price)
        sharechange[position.symbol] = current - last
    return sharechange


def dayChange():
    """
    Day Change
    Calculates and stores in a dictionary the total current change in position
    value since yesterday, which is (current_price - lastday_price)* qty.
    :return: dictionary
    """
    daychange = dict()
    for position in portfolio:
        # Strings are returned from API; convert to floating point type
        current = float(position.current_price)
        last = float(position.lastday_price)
        quant = float(position.qty)
        daychange[position.symbol] = (current - last) * quant
    return daychange


def shareProfit():
    """
    Share Profit
    Calculates the total current amount of profit/loss per share of each asset
    which is current_price - avg_entry_price
    :return: dictionary
    """
    shareprofit = dict()
    for position in portfolio:
        # Strings are returned from API; convert to floating point type
        current = float(position.current_price)
        entry = float(position.avg_entry_price)
        shareprofit[position.symbol] = (current - entry )
    return shareprofit


def positionProfit():
    """
    Position Profit
    Calculates the current position profit of each asset which is
    (current_price - avg_entry_price) * qty
    :return: python dictionary
    """
    psnprofit = dict()
    for position in portfolio:
        # Strings are returned from API; convert to floating point type
        quant = float(position.qty)
        current = float(position.current_price)
        entry = float(position.avg_entry_price)
        psnprofit[position.symbol] = (current - entry) * quant
    return psnprofit


# Place portfolioValue method here
def portfolioValue():
    """
    Portfolio Value
    Calculates the current total portfolio value, the sum of value of all shares owned.
    This function returns a single total portfolio value.
    :return: float
    """
    portvalue = (sum(currValue().values()))
    return round(portvalue, 2)


def portDayChng():
    """
    Portfolio Day Change
    Calculates the change of the total portfolio value since yesterday
    This function returns single portfolio value change.
    :return: float
    """
    portdychng = (sum(dayChange().values()))
    return round(portdychng, 2)


def positionPctProfit():
    """
    Position Percent Profit
    The percentage profit/loss of each position. Returns a dictionary with
    market symbol keys and percent values.
    :return: dictionary
    """
    psnpct = dict()
    for position in portfolio:
        # Strings are returned from API; convert to floating point type
        current = float(position.current_price)
        entry = float(position.avg_entry_price)
        psnpct[position.symbol] = ((current - entry) / entry) * 100
    return psnpct


def portPctProfit():
    """
    Portfolio Percentage Profit
    The percentage profit/loss of the entire portfolio. Returns a single valued percentage
    :return: float
    """
    totcost = (sum(totalCost().values()))
    totvalue = portfolioValue()
    portpct = ((totvalue - totcost)/totcost) * 100
    return round(portpct, 2)


def portProfit():
    """
    Portfolio Total Profit
    The total profit/loss of the entire portfolio. Returns a single valued number
    :return: float
    """
    totcost = (sum(totalCost().values()))
    totvalue = portfolioValue()
    portprof = (totvalue - totcost)
    return round(portprof, 2)


# Todo: figure out how to integrate logic into main
#  for calling this method and inserting new markets
#  user has bought into table.
#  ( NOTE: THIS Will be DONE in later version)
def dataForBrokerageTable():
    """
    Creates records in brokerStats DB table
    :return: Void
    """

    # get all necessary values
    costPerShareDict = costPerShare()
    shareProfitDict = shareProfit()
    profitAndLossDict = positionProfit()   
    quantityDict = numShares()
    priceDict = currentPrice()
    valueDict = currValue()
    dayChangeDict = dayChange()
    costDict = totalCost()
    pLPercentDict = positionPctProfit()

    # empty list to store market symbol.
    symList = []

    # get market symbols
    for key in quantityDict:
      symList.append(key)

    for mS in symList:

      dataStorage.brokerStatsRecord(mS, costPerShareDict[mS], round(shareProfitDict[mS], 2),
                                    round(profitAndLossDict[mS], 2), quantityDict[mS], priceDict[mS], valueDict[mS],
                                    round(dayChangeDict[mS], 2), costDict[mS], round(pLPercentDict[mS], 2))


# calls method to insert data into brokerStats table
# dataForBrokerageTable()
