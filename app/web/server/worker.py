import time
import dateparser
import pytz
from datetime import datetime
from binance.client import Client
import datetime as dt
from stockstats import StockDataFrame
import pandas as pd
import os


def date_to_milliseconds(date_str):
    # get epoch value in UTC
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


def interval_to_milliseconds(interval):
    ms = None
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }

    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            pass
    return ms


def get_historical_klines(symbol, interval, start_str, end_str=None):
    # create the Binance client, no need for api key
    client = Client("", "")

    # init our list
    output_data = []

    # setup the max limit
    limit = 500

    # convert interval to useful value in seconds
    timeframe = interval_to_milliseconds(interval)

    # convert our date strings to milliseconds
    start_ts = date_to_milliseconds(start_str)

    # if an end time was passed convert it
    end_ts = None
    if end_str:
        end_ts = date_to_milliseconds(end_str)

    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        # fetch the klines from start_ts up to max 500 entries or the end_ts if set
        temp_data = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts
        )

        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            # append this loops data to our output data
            output_data += temp_data

            # update our start timestamp using the last value in the array and add the interval timeframe
            start_ts = temp_data[len(temp_data) - 1][0] + timeframe
        else:
            # it wasn't listed yet, increment our start date
            start_ts += timeframe

        idx += 1
        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break

        # sleep after every 3rd call to be kind to the API
        if idx % 3 == 0:
            time.sleep(1)

    return output_data


def uixtoutc(x):
    return datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S')


def getday(x):
    x = datetime.utcfromtimestamp(x / 1000)
    return x.day


def process_klines(klines):
    df = pd.DataFrame(klines)
    df.columns = ['open_time',
                  'o', 'h', 'l', 'c', 'v',
                  'close_time', 'qav', 'num_trades',
                  'taker_base_vol', 'taker_quote_vol', 'ignore']
    df['o'] = df['o'].astype(float)
    df['h'] = df['h'].astype(float)
    df['l'] = df['l'].astype(float)
    df['c'] = df['c'].astype(float)
    df['v'] = df['v'].astype(float)
    df['qav'] = df['qav'].astype(float)
    df['taker_base_vol'] = df['taker_base_vol'].astype(float)

    df = df.fillna(0)
    return df


def return_file(inputs, tgt_dir):
    dir_to_return = '/cryptodata/'

    X = inputs
    print('Inputs: ' + str(X))

    symbol = str(X[0])
    start = str(X[1])
    end = str(X[2])
    interval = str(X[3])
    file_format = str(X[4])

    try:
        klines = get_historical_klines(symbol, interval, start, end)
        klines_ok = True
    except:
        klines_ok = False
        # return render_template('binance_api_tool.html', form_inputs='Binance API Error. Pravděpodobně byl zadán špatný Ticker.')
        return ('Binance API Error. Pravděpodobně byl zadán špatný Ticker.')

    if klines_ok:
        df = process_klines(klines)
        df['d'] = df['open_time'].apply(getday)
        df['open_time'] = df['open_time'].apply(uixtoutc)
        df['close_time'] = df['close_time'].apply(uixtoutc)

        stock = df.rename(
            columns={'o': 'open', 'c': 'close', 'h': 'high', 'l': 'low', 'v': 'volume', 'num_trades': 'amount'})

        stock = StockDataFrame.retype(stock)
        stock['macd'] = stock.get('macd')
        stock['rsi_12'] = stock.get('rsi_12')
        stock['volume_delta'] = stock.get('volume_delta')
        stock['dma'] = stock.get('dma')
        stock['open_2_sma'] = stock.get('open_2_sma')
        stock['macds'] = stock.get('macds')

        header_list = ['close_time', 'open', 'close', 'high', 'low', 'volume', 'amount', 'macd', 'rsi_12',
                       'volume_delta', 'dma', 'open_2_sma', 'macds', 'close_10_sma', 'close_50_sma']
        stock = stock.reindex(columns=header_list)
        stock = stock.fillna(0)

        if file_format == 'csv':
            filename_ = symbol + '_' + interval + '_' + start + '_' + end + '.csv'
            stock.to_csv(os.path.join(tgt_dir, filename_), index=False)
            print(f'CSV saved to: {tgt_dir}')

        elif file_format == 'excel':
            filename_ = symbol + '_' + interval + '_' + start + '_' + end + '.xlsx'
            stock.to_excel(os.path.join(tgt_dir, filename_), index=False)
            print(f'CSV saved to: {tgt_dir}')

        return (os.path.join(dir_to_return, filename_))
