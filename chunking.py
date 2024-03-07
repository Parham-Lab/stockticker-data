from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
import pandas as pd
from datetime import datetime, timedelta
import time

#from nordvpn_connect import initialize_vpn, rotate_VPN, close_vpn_connection



def generate_3_month_intervals(start_date, end_date):
    current_date = start_date
    intervals = []
    while current_date < end_date:
        next_interval_end = current_date + timedelta(days=90)
        overlap_date = next_interval_end - timedelta(days=30) 
        if next_interval_end > end_date:
            next_interval_end = end_date
        intervals.append((current_date, next_interval_end))
        current_date = overlap_date if overlap_date < end_date else end_date
    return intervals


def fetch_google_trends_data_batched(stock_ticker, start_year, end_year):
    # English language, time zone
    pytrends = TrendReq(hl='en-US', tz=360)
    
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    
    # Generate 3-month intervals
    intervals = generate_3_month_intervals(start_date, end_date)

    countries = [
        "US", "Canada", "Brazil", "Argentina", "Mexico",
        "Costa Rica", "Chile", "Colombia", "United Kingdom", "Germany",
        "Netherlands", "France", "Sweden", "Switzerland", "Belgium",
        "Denmark", "Norway", "Poland", "Ireland", "Czech Republic",
        "Italy", "Spain", "Finland", "Serbia", "Austria",
        "Slovakia", "Slovenia", "Bulgaria", "Hungary", "Latvia",
        "Romania", "Portugal", "Luxembourg", "Ukraine", "Greece",
        "Estonia", "Iceland", "Albania", "Cyprus", "Croatia",
        "Moldova", "Bosnia and Herzegovina", "Georgia", "North Macedonia", "Lithuania",
        "Australia", "Singapore", "Japan", "Hong Kong", "New Zealand",
        "Taiwan", "Vietnam", "Indonesia", "Malaysia", "South Korea",
        "Thailand", "South Africa", "United Arab Emirates", "Israel", "Türkiye"
    ]

    i = 0
    
    all_data = []
    
    for start, end in intervals:
        timeframe = f"{start.strftime('%Y-%m-%d')} {end.strftime('%Y-%m-%d')}"
        pytrends.build_payload([stock_ticker], cat=0, timeframe=timeframe, geo='', gprop='')
        try:
            data = pytrends.interest_over_time()
            if not data.empty:
                data.reset_index(inplace=True)
                data['Ticker'] = stock_ticker
                data['Interval'] = timeframe
                
                all_data.append(data)
                time.sleep(5)  
        except TooManyRequestsError:
            print("Hit rate limit, adding more time")
            time.sleep(10)


            '''
            settings = initialize_vpn(countries[i])
            rotate_VPN(settings)
            print("server switched!")
            if i == len(countries) - 1:
                i = 0
            else:
                i += 1  

            '''

    if all_data:
        final_data = pd.concat(all_data, ignore_index=True)
        
        final_data = final_data[['Ticker', stock_ticker, 'date', 'Interval']]
        final_data.columns = ['Stock Ticker', 'SVI', 'Date Recorded', 'Time Interval']
        
        csv_file_name = f"{stock_ticker}_google_trends_2004_2022.csv"
        final_data.to_csv(csv_file_name, index=False)
        print(f"Data successfully saved to {csv_file_name}")
    else:
        print("No data found for the given keyword and time interval.")

'''
settings = initialize_vpn("France")
rotate_VPN(settings) 

'''

fetch_google_trends_data_batched('MSFT', 2004, 2010)
