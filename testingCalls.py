from pytrends.request import TrendReq
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

import pandas as pd


def testLimit(term):

    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = [term]
    
    numCalls = 0
    try:
        while True:
            pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')
            pytrends.interest_over_time()
            numCalls += 1

            print(f"num calls: {numCalls}", end="\r")
            # this will break
            # time.sleep(0.2) 
            
    # error catch
    except Exception as e:

        print({e})
        print(f"max num calls {numCalls}")
        return numCalls


def initialCall(term):

    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = [term]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')
    data = pytrends.interest_over_time()

    print(data)


def graph(term, start, end):
    pytrend = TrendReq()

    pytrend.build_payload(kw_list=[term], timeframe=f'{start} {end}')

    data = pytrend.interest_over_time()

    if data.empty:
        print("null data")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(data[term], label=term)
    plt.title(f'Google Searches for "{term}" Over Time')
    plt.xlabel('Date')
    plt.ylabel('Relative Search Volume')
    plt.legend()
    plt.show()

graph('hello', '2020-01-01', '2023-01-01')

#initialCall("hello")

#testLimit("hello")

