"""
Kwic Trader trading system
Created by:
Robert (Alex) Spangler
Plant City, FL, USA
Spring of 2021
"""

"""
Title: environmentVars module 
Contains the variables that store the keys to the brokerage API (Alpaca).

"""
import os

# environment variables to connect to brokerage API

API_KEY = os.environ.get('ALPACA_API_KEY')
SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
