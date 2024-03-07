import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import time

def fetch_trends(search_term, start, end):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([search_term], timeframe=f'{start} {end}')
    return pytrends.interest_over_time()

def sliding_window_trends(search_term, start_year=2004, call_limit=4):
    start_date = datetime(start_year, 1, 1)
    end_date = start_date + timedelta(days=90)
    all_data = pd.DataFrame()

    for _ in range(call_limit):
        try:
            data = fetch_trends(search_term, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            all_data = pd.concat([all_data, data])

            start_date += timedelta(days=91)  # Move to next interval
            end_date = start_date + timedelta(days=90)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    all_data.to_csv('google_trends_data.csv')

# Example Usage
sliding_window_trends('Python Programming')
