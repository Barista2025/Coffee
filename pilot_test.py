import yfinance as yf
import numpy as np
import pandas as pd
import sys
import os
import math
import requests
from bs4 import BeautifulSoup
import matplotlib as mpl
import matplotlib.pyplot as plt
import re
import datetime
from importlib.machinery import SourceFileLoader
from transaction import *
import json
import datetime
np.set_printoptions(legacy='1.25')

input_file = open ('accounts.json')
json_array = json.load(input_file)

access_token = obtain_access_token()
hash_value = obtain_hash_value(access_token)

#price,share = place_limit_order('AMBA',60,access_token,hash_value,"BUY")
#print(str(price)+" "+str(share))
price,share = place_limit_order('NVDA',150,access_token,hash_value,"BUY")
print(str(price)+" "+str(share))
#price,share = place_limit_order('NVDA',150,access_token,hash_value,"BUY")
#print(str(price)+" "+str(share))
#price,share = place_sell_order('VOO',1,access_token,hash_value)
#print(str(price)+" "+str(share))
