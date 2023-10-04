import csv
import os
from pathlib import Path

import pandas as pd
from tqdm import tqdm
import datetime

import ccxt
from mike_config import TFrame
from mike_config import crypto_lst

INTEREST_RATE = 1 + 0.001 * 2 + 0.003
STOP_LOSS_RATE = 1 - 0.002
ex = ccxt.binance()


def PredictResult(flag: dict):
    if flag['RISE']:
        if flag['DROP']:
            return 0 # RISE_DROP
        else:
            return 3 # RISE_NODROP
    else:
        if flag['DROP']:
            return 1 # NORISE_DROP
        else:
            return 2 # NORISE_NODROP


def predict(data: pd.DataFrame) -> int:
    buy_price = data.iloc[data.shape[0]//5*4 - 1, 4] # the last timestamp close price for the 2 hr
    flag = {'RISE': False, 'DROP': False}
    for idx in range(data.shape[0]//5*4, data.shape[0]):
        if data.iloc[idx, 2] > buy_price * INTEREST_RATE:
            flag['RISE'] = True
        if data.iloc[idx, 3] < buy_price * STOP_LOSS_RATE:
            flag['DROP'] = True
    return PredictResult(flag)


def get_project_root_path() -> Path:
    """
    get the root path of this project
    :return: path of the root dir
    """
    return Path(__file__).parent


def create_csv(symbol: str, tframe: TFrame, num: int):
    """
    create the csv file, write the header
    :param symbol: crypto name as parent folder name
    :param tframe: timeframe as sub-folder name
    :param num: the order number of files
    :return: path
    """
    symbol_name = symbol.replace("/", "")

    # create folder
    folder_path = 'data/' + symbol_name + '/' + tframe.name
    actual_path = get_project_root_path().joinpath(folder_path)
    if not os.path.exists(actual_path):
        os.makedirs(actual_path)
        print("Folder created successfully.")
    else:
        print("Folder already exists.")

    # create file
    csv_file_path = folder_path + '/data' + str(num) + '.csv'
    actual_path = get_project_root_path().joinpath(csv_file_path)

    if os.path.isfile(actual_path):
        print("CSV file already exists.")
    else:
        with open(actual_path, 'w', newline='') as f:
            csv_write = csv.writer(f)
            header = []
            structure = ['date', 'open', 'high', 'low', 'close', 'volume']
            for i in range(tframe.size):
                header.extend([elem + str(i) for elem in structure])
            header.extend(["prediction"])
            csv_write.writerow(header)
        print("CSV file created successfully.")
    return actual_path


def write_csv(path, data: pd.DataFrame):
    data.to_csv(get_project_root_path().joinpath(path), mode='a', header=False, index=False)


def count_data(symbol: str, timestamp: str, file_num: int):
    # 读取 Excel 文件
    df = pd.read_csv('D:/GitHub/tryStock/data/' + symbol.replace("/", "") + '/' + timestamp + '/data' + file_num.__str__() + '.csv')

    print(f"time: {timestamp}")
    # 统计值等于 3 的数量
    count0 = df[df['prediction'] == 0].shape[0]
    count1 = df[df['prediction'] == 1].shape[0]
    count2 = df[df['prediction'] == 2].shape[0]
    count3 = df[df['prediction'] == 3].shape[0]

    print("RISE_DROP: " + str(count0))
    print("NORISE_DROP: " + str(count1))
    print("NORISE_NODROP: " + count2.__str__())
    print("RISE_NODROP: " + count3.__str__())


def get_usd_crypto():
    """
    GET USD crypto list
    :return: symbol list
    """
    symbol_list = []
    markets = ex.load_markets()
    symbol_df = pd.DataFrame.from_dict(markets, orient='index', columns=['symbol', 'quote'])
    filtered_df = symbol_df[symbol_df['quote'] == 'USD']
    for row in filtered_df.itertuples(index=False):
        symbol_list.append(row.symbol)
    return symbol_df


def get_history_data(symbol: str, timeframe: TFrame):
    ohlcv_list = []
    file_counter = 0
    row_counter = 100000
    file_path = ''
    limit = 1000
    from_ts = ex.parse8601('2018-01-01 00:00:00')
    while True:
        if row_counter >= 100000:
            if file_counter > 0:
                count_data(symbol, timeframe.name, file_counter)
            row_counter = 1
            file_counter += 1
            file_path = create_csv(symbol, timeframe, file_counter)
        if len(ohlcv_list) > 0:
            from_ts = ohlcv[-1][0]
            new_ohlcv = ex.fetch_ohlcv(symbol, timeframe=timeframe.name, limit=timeframe.size - 1, since=from_ts)
            ohlcv_list.extend(new_ohlcv)

            # make and store data, clear list
            df = pd.DataFrame(ohlcv_list, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
            df['date'] = pd.to_datetime(df['date'], unit='ms')
            for i in tqdm(range(df.shape[0] - timeframe.size), desc="Processing"):
                datum = df.loc[i: i + timeframe.size - 1] # (150, 6)
                prediction = predict(datum)
                datum = pd.DataFrame(datum.stack().T).transpose()
                datum['prediction']=prediction
                write_csv(file_path, datum)
                row_counter += 1

            datetime_obj = datetime.datetime.fromtimestamp(ohlcv_list[-1][0] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{symbol} : {timeframe.name} ==> FILE #{file_counter} --- ROW #{row_counter}  |  current date: {datetime_obj}")
            # clear memory
            del df
            del ohlcv_list
            ohlcv_list = []

        ohlcv = ex.fetch_ohlcv(symbol, timeframe=timeframe.name, limit=limit, since=from_ts)
        ohlcv_list.extend(ohlcv)
        if len(ohlcv) != 1000:
            return


def load_data():
    for sbl in crypto_lst:
        for item in TFrame:
            get_history_data(sbl, item)


if __name__ == "__main__":
    load_data()
# get_history_data('BTC/USDT', TFrame.t1M)
# get_history_data('BTC/USDT', TFrame.t5M)
# get_history_data('BTC/USDT', TFrame.t15M)
# get_history_data('BTC/USDT', TFrame.t30M)
