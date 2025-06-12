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

#price,share = place_buy_order('VOO',600,access_token,hash_value)
#print(str(price)+" "+str(share))
price,share = place_limit_order('NVDA',3,access_token,hash_value,"SELL")
print(str(price)+" "+str(share))
#price,share = place_limit_order('CRCL',1,access_token,hash_value,"SELL")
#print(str(price)+" "+str(share))
