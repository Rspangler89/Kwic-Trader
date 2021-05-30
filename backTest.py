"""
Kwic Trader trading system
Created by:
Robert (Alex) Spangler
Plant City, FL, USA
Spring of 2021
"""
"""
NOTE: 
cerebro.plot() only works with matplotlib 3.2.0
be sure to have this version installed.
"""
import backtrader as bt
import alpaca_backtrader_api as api
import pandas as pd
import environmentVars
import dataStorage


"""
Title: backTest module 
contains the logic for back testing.
"""
"""
NOTE: 
After further research I have come to realize that the following methods
can either be replaced with other library methods. 

These methods include the following:

main.displayBackTestHistory(),
main.displayStream(),
backTest.historyData()
backTest.sharpRatio()

This has lead to the deletion of the following test files:

test_backTest.py
test_main.py

"""


# Variables used
MY_API_KEY = environmentVars.API_KEY
MY_SECRET_KEY = environmentVars.SECRET_KEY
PAPER_TRADE = True


# Trade Strategy
class SmaCross(bt.SignalStrategy):
    """
    SmaCross() class gets the cross over of two simple moving average strategy.
    This is the only strategy used for back-testing as of this version. However,
    many others will be created in future iterations of the program.
    """
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)


def runBackTest(mrktSym, strtDate, endDate):

    """
    Plots and displays historical results from back-test.
    :param: mrktSym: string
    :param: strtDate: Date
    :param: endDate: Date
    :return: void
    """

    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)

    info = api.AlpacaStore(
        key_id=MY_API_KEY,
        secret_key=MY_SECRET_KEY,
        paper=PAPER_TRADE
    )

    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.0)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=20)

    DataFactory = info.getdata

    data = DataFactory(
            dataname=mrktSym,
            timeframe=bt.TimeFrame.TFrame("Days"),
            fromdate=pd.Timestamp(strtDate),
            todate=pd.Timestamp(endDate),
            historical=True)

    cerebro.adddata(data)

    # Add the analyzers needed

    # --------------------vvv-Analyzers Added-vvv-----------------------#
    # Add TradeAnalyzer
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")

    # Add SharpeRatio
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharperatio')

    # Add Returns (for AnnualReturn)
    cerebro.addanalyzer(bt.analyzers.Returns, _name='AnnReturn')

    # Add DrawDown
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')

    # -------------------^^^-Analyzers Added-^^^------------------------#

    # Run over everything
    strategies = cerebro.run()
    firstStrat = strategies[0]

    """
    GET ALL FIELDS FOR backtestStats table BELOW
    """

    # ------------------------Sharpe Ratio-------------------------#
    shObj = firstStrat.analyzers.sharperatio.get_analysis()
    # above = OrderedDict([('sharperatio', <number>)])
    sharpeRatio = round(shObj['sharperatio'], 2)

    # Object made from TradeAnalyzer for Gross profit and Gross loss
    taObj = firstStrat.analyzers.ta

    # -------------------------Gross Profit-----------------------#
    gProfObj = taObj.get_analysis().won.pnl.total

    grossProfit = round(gProfObj, 2)

    # --------------------------Gross Loss------------------------#
    gLossObj = taObj.get_analysis().lost.pnl.total

    grossLoss = abs(round(gLossObj, 2))

    # --------------------------Annual Return------------------------#
    arObj = firstStrat.analyzers.AnnReturn.get_analysis()

    annualReturn = round(arObj['rnorm100'], 2)

    # --------------------------Total Net Profit---------------------#
    totalNetProfit = round(grossProfit - grossLoss, 2)

    # --------------------------Profit Factor------------------------#
    profitFactor = round(grossProfit / grossLoss, 2)

    # --------------------------DrawDown-----------------------------#
    drwDwnObj = firstStrat.analyzers.DrawDown.get_analysis().drawdown

    drawDown = round(drwDwnObj, 2)

    #  insert data into data storage
    dataStorage.backtestStatsRecord(mrktSym, strtDate, endDate, totalNetProfit, grossProfit, grossLoss,
                                    profitFactor, annualReturn, drawDown, sharpeRatio)
    """
    NOTE: 
    cerebro.plot() only works with matplotlib 3.2.0
    """
    cerebro.plot()
