from worker import get_historical_klines, process_klines
import pandas as pd
from datetime import datetime, timedelta
import logging
import sys
import os

filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'btc_app.log')
logging.basicConfig(filename=filename, filemode='a', level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def main():
    
    try:
        logging.info('Getting BTC price data.')
        klines = get_historical_klines('BTCUSDT', '1d', '15.2.2022')
        df = process_klines(klines)
        df = df[["open_time", "c", "h", "l", "o"]]
        df.rename(columns={'open_time': 'time',
                           'c': 'close',
                           'h': 'high',
                           'l': 'low',
                           'o': 'open',}, inplace=True)
        df['time'] = df['time'].values.astype(float)/1000
        df['time'] = df['time'].astype(int)
        
        df.to_csv('/app/misc_files/btcusdt.csv', index=False)
        logging.info('BTC price data successfully saved.')
    except Exception as e:
        logging.error(f'Could not save BTC data: {e}')

if __name__ == '__main__':
    
    main()

